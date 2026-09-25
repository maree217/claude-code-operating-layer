"""Shared helpers for the operating-layer hooks. Stdlib only, no pip deps.

Every hook in this directory does the same two things before its own logic:
read the PreToolUse/PostToolUse/SessionStart JSON off stdin, and load
guardrails.json. This module does both, plus the two ways a PreToolUse hook
blocks a call (exit code 2 + stderr is the primary, always-blocking
mechanism per the Claude Code hooks docs; the JSON permissionDecision form
is available too and is used where a hook wants to also return
additionalContext).
"""
import json
import os
import sys


def read_stdin_json():
    """Read and parse the hook's stdin JSON payload. Returns {} on any
    failure — a hook that can't parse its input should fail open, not
    crash (a crashing PreToolUse hook exits non-zero-but-not-2, which
    Claude Code treats as a silent allow anyway)."""
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return {}
        return json.loads(raw)
    except Exception:
        return {}


def find_project_root(start_dir=None):
    """Locate the repo root: prefer $CLAUDE_PROJECT_DIR (set by the harness
    for every hook invocation), else walk up from start_dir (default: this
    file's directory) looking for guardrails.json, else fall back to two
    levels up from this file (.claude/hooks/../.. == repo root)."""
    env_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_root and os.path.isfile(os.path.join(env_root, "guardrails.json")):
        return env_root

    here = start_dir or os.path.dirname(os.path.abspath(__file__))
    cur = here
    for _ in range(6):
        if os.path.isfile(os.path.join(cur, "guardrails.json")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent

    # Last resort: this file lives in <root>/.claude/hooks/_common.py.
    return os.path.abspath(os.path.join(here, "..", ".."))


def load_guardrails():
    """Load guardrails.json from the project root. Returns a safe empty
    default (nothing blocked) if the file is missing or unparseable — a
    misconfigured guardrails file must never silently deny everything,
    it should silently protect nothing and let that absence be visible
    in review instead."""
    root = find_project_root()
    path = os.path.join(root, "guardrails.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "protected_branches": [],
            "protected_paths": [],
            "blocked_command_patterns": [],
            "outbound_allowlist": [],
            "operating_layer_line_budget": 80,
        }


def block(message: str):
    """Block the current tool call. Exit code 2 is the primary, always-
    blocking mechanism (per the hooks docs); stderr becomes the reason
    Claude sees."""
    sys.stderr.write(message.rstrip("\n") + "\n")
    sys.exit(2)


def allow():
    sys.exit(0)


def truncate(text: str, limit: int) -> str:
    if text is None:
        return ""
    text = str(text)
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)] + "..."
