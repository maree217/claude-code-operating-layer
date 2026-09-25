#!/usr/bin/env python3
"""PreToolUse hook on Edit|Write, scoped to operating-layer/*.md — enforces
the size cap from guardrails.json's operating_layer_line_budget (default
80). This is the "the layer has a size cap, because memory that only
ever grows eventually poisons every session it's loaded into" rule,
enforced instead of hoped for.

Line-count estimation:
  - Write: exact. The tool_input carries the full new file content.
  - Edit: approximate. Claude Code's Edit tool gives old_string/new_string,
    not the full resulting file, so this hook reads the file currently on
    disk, counts how many times old_string occurs (all occurrences if
    replace_all is set, else 1), and adds occurrences * (lines in
    new_string - lines in old_string) to the file's current line count.
    This is exact for the common single-occurrence case and a reasonable
    approximation otherwise; it is documented here rather than silently
    assumed. Because it estimates from the file already on disk, an Edit
    to a brand-new file this same turn (no file yet) is allowed through
    uncounted — Write is what creates new operating-layer files, and Write
    is checked exactly.

Blocks with exit code 2 (always blocks; stderr is the reason shown to
Claude), per the Claude Code hooks docs.
"""
import fnmatch
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_stdin_json, load_guardrails, find_project_root, block, allow  # noqa: E402

WATCHED_TOOLS = {"Edit", "Write"}
SCOPE_GLOB = "operating-layer/*.md"


def count_lines(text: str) -> int:
    if not text:
        return 0
    # A trailing newline shouldn't count as an extra blank line for a
    # human skimming the file; splitlines() gives the intuitive count.
    return len(text.splitlines())


def relative_to_root(path: str, root: str) -> str:
    if not path:
        return ""
    abs_path = os.path.abspath(os.path.expanduser(path))
    abs_root = os.path.abspath(root)
    try:
        rel = os.path.relpath(abs_path, abs_root)
    except ValueError:
        return ""
    if rel.startswith(".."):
        return ""
    return rel.replace(os.sep, "/")


def estimate_new_line_count(tool_name: str, tool_input: dict, abs_path: str) -> int:
    if tool_name == "Write":
        return count_lines(tool_input.get("content", ""))

    # Edit: approximate from the file currently on disk.
    try:
        with open(abs_path, encoding="utf-8") as f:
            current = f.read()
    except OSError:
        # No existing file to estimate from (e.g. Edit racing a same-turn
        # Write) — let the Write-time check be the authority instead of
        # guessing here.
        return -1

    current_lines = count_lines(current)
    old_string = tool_input.get("old_string", "") or ""
    new_string = tool_input.get("new_string", "") or ""
    replace_all = bool(tool_input.get("replace_all", False))

    occurrences = current.count(old_string) if (replace_all and old_string) else 1
    if old_string == "" and not replace_all:
        occurrences = 1  # Edit with empty old_string is a pure insertion; treat as one edit.

    delta_per_occurrence = count_lines(new_string) - count_lines(old_string)
    return current_lines + occurrences * delta_per_occurrence


def main():
    data = read_stdin_json()
    tool_name = data.get("tool_name")
    if tool_name not in WATCHED_TOOLS:
        allow()

    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path", "") or ""
    if not file_path:
        allow()

    root = find_project_root()
    rel_path = relative_to_root(file_path, root)
    if not rel_path or not fnmatch.fnmatch(rel_path, SCOPE_GLOB):
        allow()

    guardrails = load_guardrails()
    budget = int(guardrails.get("operating_layer_line_budget", 80))

    abs_path = os.path.abspath(os.path.expanduser(file_path))
    estimated = estimate_new_line_count(tool_name, tool_input, abs_path)
    if estimated < 0:
        allow()

    if estimated > budget:
        block(
            f"Blocked by layer_budget.py: {rel_path} would be ~{estimated} "
            f"lines, over the {budget}-line budget in guardrails.json "
            "(operating_layer_line_budget).\n"
            "Prune before you add — see LEARNING-LOOP.md: this sheet is "
            "meant to stay small enough that every agent can hold all of "
            "it, every session. Retire a stale line, tighten the wording, "
            "or move detail out to processes/ or examples/ before this "
            "edit lands."
        )

    allow()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)
