#!/usr/bin/env python3
"""SessionStart hook — forces recall of the two sections that matter most
on arrival: OPERATING-RULES.md's "Agents may not" list and BETS-REGISTER's
"Live bets" list. Pattern borrowed from a personal brain-recall hook: make
recall deterministic (injected every session) rather than hoping the agent
reads the operating layer on its own.

Hard-capped in characters (SessionStart context is not free) — if either
section runs long, it's truncated with a note rather than silently
dropped, and truncation is a signal to prune the sheet (see
layer_budget.py / LEARNING-LOOP.md), not to raise the cap.

Section markers this hook looks for (exact, case-sensitive):
  OPERATING-RULES.md : "## Agents may not"
  BETS-REGISTER.md   : "## Live bets"
Each section runs from its header to the next line starting with "## ",
or end of file.

Always exits 0 — a recall hook must never block a session.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_stdin_json, find_project_root  # noqa: E402

TOTAL_CHAR_CAP = 2000
PER_SECTION_CAP = 1200

FILES = (
    ("operating-layer/OPERATING-RULES.md", "## Agents may not", "OPERATING-RULES.md — Agents may not"),
    ("operating-layer/BETS-REGISTER.md", "## Live bets", "BETS-REGISTER.md — Live bets"),
)


def extract_section(path: str, header: str):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return None
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == header.strip())
    except StopIteration:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    section = "\n".join(lines[start:end]).strip()
    if len(section) > PER_SECTION_CAP:
        section = section[:PER_SECTION_CAP].rstrip() + "\n… [truncated — prune this sheet]"
    return section


def build_brief(root: str) -> str:
    blocks = []
    for relative, header, label in FILES:
        section = extract_section(os.path.join(root, relative), header)
        if section:
            blocks.append(f"[{label}]\n{section}")
    if not blocks:
        return ""
    brief = (
        "Operating layer — forced recall at session start (this is memory "
        "architecture, not a suggestion: OPERATING-RULES.md and "
        "BETS-REGISTER.md outrank guesswork about what agents may do here).\n\n"
        + "\n\n".join(blocks)
    )
    if len(brief) > TOTAL_CHAR_CAP:
        brief = brief[:TOTAL_CHAR_CAP].rstrip() + "\n… [truncated at the session-brief char cap]"
    return brief


def main():
    data = read_stdin_json()
    root = find_project_root(data.get("cwd"))
    brief = build_brief(root)
    if not brief:
        return
    import json
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": brief,
        }
    }))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
