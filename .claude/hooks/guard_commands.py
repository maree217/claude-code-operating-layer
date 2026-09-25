#!/usr/bin/env python3
"""PreToolUse hook on Bash — enforces the OPERATING-RULES.md "Agents may
not" list in code, not prose.

Blocks (via guardrails.json's blocked_command_patterns, plus the two
protected-branch checks below): force pushes, pushes to a protected
branch, `gh pr merge`, `gh pr review --approve` (an agent approving or
merging its own work), destructive `rm -rf` outside a tmp path, and
deploy/infra-apply commands (terraform apply, kubectl apply, prod db
writes).

This is a floor, not a security boundary — a Bash permission rule matches
the command text Claude Code sends, not every way the same program could
be invoked (see the Claude Code permissions docs). The point is to stop
the agent's own straightforward attempt and say, plainly, which rule
stopped it and who to escalate to — same contract as guard_paths.py and
layer_budget.py.

Blocks with exit code 2 (always blocks; stderr is the reason shown to
Claude), per the Claude Code hooks docs.
"""
import re
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _common import read_stdin_json, load_guardrails, block, allow  # noqa: E402

ESCALATE = (
    "Escalate to: the named owner in OPERATING-RULES.md's "
    "'Who approves what' table (or the repo's default owner if this "
    "specific action has no named owner yet)."
)


def branch_push_pattern(branches):
    if not branches:
        return None
    alt = "|".join(re.escape(b) for b in branches)
    return r"\bgit\s+push\b[^|;&\n]*\b(origin\s+)?(" + alt + r")\b"


def main():
    data = read_stdin_json()
    if data.get("tool_name") != "Bash":
        allow()

    command = (data.get("tool_input") or {}).get("command", "") or ""
    if not command:
        allow()

    guardrails = load_guardrails()
    patterns = list(guardrails.get("blocked_command_patterns", []))

    branch_pattern = branch_push_pattern(guardrails.get("protected_branches", []))
    if branch_pattern:
        patterns.append(branch_pattern)

    for pattern in patterns:
        try:
            if re.search(pattern, command, re.IGNORECASE):
                block(
                    "Blocked by guard_commands.py: this command matches a rule "
                    "in OPERATING-RULES.md's 'Agents may not' list "
                    f"(pattern: {pattern}).\n"
                    f"Command: {command}\n"
                    f"{ESCALATE}\n"
                    "See guardrails.json (blocked_command_patterns / "
                    "protected_branches) for the exact rule."
                )
        except re.error:
            continue  # a malformed pattern in guardrails.json must not crash the hook

    allow()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        # Fail open: a crashing PreToolUse hook is treated as a silent
        # allow anyway (non-zero-but-not-2), so exit 0 explicitly rather
        # than leave an unhandled traceback.
        sys.exit(0)
