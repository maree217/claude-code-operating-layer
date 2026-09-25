#!/usr/bin/env python3
"""PostToolUse hook, all tools — the OBSERVABILITY layer. Appends one JSON
line per action to .claude/audit/actions.jsonl: timestamp, session id
(if present), tool, and a short summary. Never logs full file contents,
tool_response bodies, or anything that looks like a secret — summaries
are truncated and scoped to identifying fields only (file paths, command
text, subagent type), never payload content.

.claude/audit/ is gitignored: this is a local, growing log, not something
to commit. The weekly 'learn' skill reads it to propose rule changes.

Always exits 0 — an observability hook must never block or fail a turn.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_stdin_json, find_project_root, truncate  # noqa: E402

SUMMARY_LIMIT = 200
LOG_RELATIVE = os.path.join(".claude", "audit", "actions.jsonl")


def summarize(tool_name: str, tool_input: dict) -> str:
    tool_input = tool_input or {}
    if tool_name in ("Edit", "Write"):
        return f"{tool_name} {tool_input.get('file_path', '?')}"
    if tool_name == "NotebookEdit":
        return f"NotebookEdit {tool_input.get('notebook_path', '?')}"
    if tool_name == "Bash":
        return f"Bash: {truncate(tool_input.get('command', ''), SUMMARY_LIMIT)}"
    if tool_name == "Agent":
        return (
            f"Agent subagent_type={tool_input.get('subagent_type', '?')} "
            f"desc={truncate(tool_input.get('description', ''), 80)}"
        )
    if tool_name in ("Read", "Grep", "Glob"):
        key = "file_path" if tool_name == "Read" else "pattern"
        return f"{tool_name} {truncate(tool_input.get(key, tool_input.get('path', '?')), SUMMARY_LIMIT)}"
    # Generic fallback: just the tool name plus the top-level input keys,
    # never their values — keeps unknown tools (including MCP tools,
    # which may carry sensitive params) safely opaque in the log.
    keys = ",".join(sorted(tool_input.keys())) if isinstance(tool_input, dict) else ""
    return f"{tool_name} (fields: {truncate(keys, SUMMARY_LIMIT)})"


def main():
    data = read_stdin_json()
    tool_name = data.get("tool_name", "unknown")
    tool_input = data.get("tool_input") or {}

    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "session_id": data.get("session_id", ""),
        "tool": tool_name,
        "summary": summarize(tool_name, tool_input),
    }

    root = find_project_root()
    log_path = os.path.join(root, LOG_RELATIVE)
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=True) + "\n")
    except OSError:
        pass  # observability must never break the turn


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
