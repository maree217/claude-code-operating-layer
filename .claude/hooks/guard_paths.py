#!/usr/bin/env python3
"""PreToolUse hook on Edit|Write|NotebookEdit — blocks writes to
guardrails.json's protected_paths (infra/**, deploy/**,
.github/workflows/** by default). This is what makes "agents may not
touch infra" an enforced rule instead of a request in a document.

Note: operating-layer/** is deliberately NOT in protected_paths — that
directory is edited via proposals, and its control is the line-budget
hook (layer_budget.py), not this one.

Blocks with exit code 2 (always blocks; stderr is the reason shown to
Claude), per the Claude Code hooks docs.
"""
import fnmatch
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_stdin_json, load_guardrails, find_project_root, block, allow  # noqa: E402

WATCHED_TOOLS = {"Edit", "Write", "NotebookEdit"}


def target_path_field(tool_name: str, tool_input: dict) -> str:
    if tool_name == "NotebookEdit":
        return tool_input.get("notebook_path", "") or ""
    return tool_input.get("file_path", "") or ""


def relative_to_root(path: str, root: str) -> str:
    """Best-effort project-relative path, forward-slashed, for glob
    matching. A path outside the project root is returned unchanged
    (it won't match a protected_paths glob, which is the safe default —
    this hook only knows how to protect paths inside the repo it lives
    in)."""
    if not path:
        return ""
    abs_path = os.path.abspath(os.path.expanduser(path))
    abs_root = os.path.abspath(root)
    try:
        rel = os.path.relpath(abs_path, abs_root)
    except ValueError:
        return abs_path
    if rel.startswith(".."):
        return abs_path
    return rel.replace(os.sep, "/")


def matches_any(rel_path: str, patterns) -> str:
    for pattern in patterns:
        if fnmatch.fnmatch(rel_path, pattern):
            return pattern
        # protected_paths entries end in /** — also catch the bare dir itself.
        if pattern.endswith("/**") and rel_path == pattern[: -len("/**")]:
            return pattern
    return ""


def main():
    data = read_stdin_json()
    tool_name = data.get("tool_name")
    if tool_name not in WATCHED_TOOLS:
        allow()

    tool_input = data.get("tool_input") or {}
    raw_path = target_path_field(tool_name, tool_input)
    if not raw_path:
        allow()

    root = find_project_root()
    rel_path = relative_to_root(raw_path, root)
    if not rel_path:
        allow()

    guardrails = load_guardrails()
    protected = guardrails.get("protected_paths", [])
    hit = matches_any(rel_path, protected)
    if hit:
        block(
            f"Blocked by guard_paths.py: '{rel_path}' matches protected path "
            f"'{hit}' in guardrails.json. OPERATING-RULES.md: agents may not "
            "edit protected paths directly.\n"
            "Escalate to: the named owner in OPERATING-RULES.md's "
            "'Who approves what' table for infra/deploy/CI changes.\n"
            "If this really is agent work, propose it via the 'propose' "
            "skill and open a PR for a person to review instead of "
            "editing the path directly."
        )

    allow()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)
