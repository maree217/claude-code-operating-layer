#!/usr/bin/env python3
"""PreToolUse hook on Bash — enforces the OPERATING-RULES.md "Agents may
not" list in code, not prose.

Blocks (via guardrails.json's blocked_command_patterns, plus the
protected-branch push check below): force pushes, pushes to a protected
branch (however the push is spelled — see "Protected-branch push
detection"), `gh pr merge`, `gh pr review --approve` (an agent approving
or merging its own work), destructive `rm -rf` outside a tmp path, and
deploy/infra-apply commands (terraform apply, kubectl apply, prod db
writes).

This is a floor, not a security boundary — a Bash permission rule matches
the command text Claude Code sends, not every way the same program could
be invoked (see the Claude Code permissions docs, and README.md's "What
the guardrails are — and aren't"). The point is to stop the agent's own
straightforward attempt and say, plainly, which rule stopped it and who
to escalate to — same contract as guard_paths.py and layer_budget.py.

Protected-branch push detection
--------------------------------
A literal `git push origin main` is easy to spot in the command text. Real
usage is messier, and each of these pushes to a protected branch exactly
as much as that literal form does:

  - `git push`                      (no refspec — pushes the current branch)
  - `git push origin`               (remote only, no refspec — same)
  - `git push -u origin HEAD`       (HEAD == the current branch)
  - `git push origin HEAD:main`     (colon refspec — the DESTINATION matters,
                                      not the source or the current branch)
  - `git -C . push origin main`     (git global options between `git` and
                                      the subcommand)

`normalize_git_global_options` strips known git global options (-C, -c,
--git-dir=, --work-tree=, --no-pager, -p/--paginate) so the pattern-based
checks below see `git push ...` regardless. `check_push_targets` then
parses every `git push` invocation's own arguments to work out which
remote branch name it actually writes to, resolving `HEAD`, a bare
`git push`, or `git push <remote>` with no refspec against the real
current branch via `git rev-parse --abbrev-ref HEAD` in the command's own
`cwd` — but only when a push is ambiguous enough to need it, so a plain
`git push origin feature/x` never shells out.

If the current branch can't be resolved (not a git repo, git missing,
timeout), this check fails open — same fail-open contract as the rest of
this hook and this kit. It doesn't invent a branch name to block on.

Blocks with exit code 2 (always blocks; stderr is the reason shown to
Claude), per the Claude Code hooks docs.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read_stdin_json, load_guardrails, block, allow  # noqa: E402

ESCALATE = (
    "Escalate to: the named owner in OPERATING-RULES.md's "
    "'Who approves what' table (or the repo's default owner if this "
    "specific action has no named owner yet)."
)

# Git global options that can sit between `git` and the subcommand. Each
# alternative is `<flag>` (no value), `<flag> <value>` (space-separated),
# or `<flag>=<value>` (already fused, nothing extra to strip).
_GIT_GLOBAL_OPT = r"(?:-C\s+\S+|-c\s+\S+|--git-dir=\S+|--work-tree=\S+|--no-pager|-p\b|--paginate\b)"
GIT_GLOBAL_OPTS_RE = re.compile(
    r"\bgit\b(?:\s+" + _GIT_GLOBAL_OPT + r")*\s+", re.IGNORECASE
)

# One `git push` invocation and everything after it up to a shell
# separator/newline/end-of-string — mirrors the boundary already used by
# the blocked_command_patterns entries, so a chained command never lets
# one push's args bleed into the next command.
GIT_PUSH_INVOCATION_RE = re.compile(r"\bgit\s+push\b(?P<args>[^|;&\n]*)", re.IGNORECASE)

ALL_BRANCHES_FLAGS = ("--all", "--mirror")


def normalize_git_global_options(command: str) -> str:
    """Collapse `git -C <dir> push ...` / `git -c k=v push ...` /
    `git --git-dir=... push ...` etc. down to `git push ...` for pattern
    matching. This never changes the command that actually runs — only
    the text these hooks match against."""
    return GIT_GLOBAL_OPTS_RE.sub("git ", command)


def resolve_current_branch(cwd: str):
    """Best-effort current-branch name in `cwd`. Tries `git symbolic-ref
    --short HEAD` first — unlike `rev-parse --abbrev-ref HEAD`, this
    resolves on a brand-new repo with no commits yet (an "unborn" branch),
    which is exactly the shape a freshly `git init`'d repo has. Falls back
    to `rev-parse --abbrev-ref HEAD` for anything symbolic-ref doesn't
    handle. Returns None on any failure (not a repo, git missing, timeout,
    no cwd, detached HEAD) — see the module docstring on why this fails
    open rather than guessing."""
    if not cwd:
        return None
    for args in (
        ["git", "-C", cwd, "symbolic-ref", "--short", "HEAD"],
        ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
    ):
        try:
            proc = subprocess.run(args, capture_output=True, text=True, timeout=3)
        except (OSError, subprocess.SubprocessError):
            continue
        if proc.returncode == 0:
            branch = proc.stdout.strip()
            if branch and branch != "HEAD":
                return branch
    return None


def push_targets(args_text: str, current_branch_resolver):
    """Return the set of remote branch names a `git push <args_text>`
    invocation actually writes to. `current_branch_resolver` is called at
    most once, lazily — only invocations that actually need the current
    branch (bare push, remote-only, `HEAD`) pay for the subprocess call."""
    tokens = [t for t in args_text.split() if t]
    flags = [t for t in tokens if t.startswith("-")]
    positional = [t for t in tokens if not t.startswith("-")]

    if any(f in ALL_BRANCHES_FLAGS for f in flags):
        # `--all` / `--mirror` push every local branch — can't be pinned
        # to one target, so the caller treats this as "could be any
        # protected branch" rather than this function resolving one.
        return {"*"}

    cache = {}

    def current():
        if "value" not in cache:
            cache["value"] = current_branch_resolver()
        return cache["value"]

    def branch_for(name: str):
        if name in ("", "HEAD"):
            return current()
        return name

    if len(positional) <= 1:
        # `git push`, `git push -f`, or `git push origin` (remote only, no
        # refspec) all push the current branch to its matching remote
        # branch — Git's default (push.default=simple) since Git 2.0.
        branch = current()
        return {branch} if branch else set()

    targets = set()
    for refspec in positional[1:]:
        if ":" in refspec:
            src, _, dest = refspec.partition(":")
            name = dest or src  # `src:` (unusual) falls back to src; `:dest` deletes dest
        else:
            name = refspec
        resolved = branch_for(name)
        if resolved:
            targets.add(resolved)
    return targets


def check_push_targets(command: str, protected_branches, cwd: str):
    """Return a protected branch name if `command` contains a `git push`
    that would write to it, else None. Operates on the git-global-option-
    normalized command so `git -C . push origin main` is seen the same as
    `git push origin main`."""
    if not protected_branches:
        return None
    protected_set = set(protected_branches)
    normalized = normalize_git_global_options(command)

    def resolver():
        return resolve_current_branch(cwd)

    for match in GIT_PUSH_INVOCATION_RE.finditer(normalized):
        targets = push_targets(match.group("args"), resolver)
        if "*" in targets:
            return sorted(protected_set)[0]  # --all/--mirror: any protected branch is at risk
        hit = targets & protected_set
        if hit:
            return sorted(hit)[0]
    return None


def main():
    data = read_stdin_json()
    if data.get("tool_name") != "Bash":
        allow()

    command = (data.get("tool_input") or {}).get("command", "") or ""
    if not command:
        allow()

    guardrails = load_guardrails()
    patterns = list(guardrails.get("blocked_command_patterns", []))
    normalized_command = normalize_git_global_options(command)

    for pattern in patterns:
        try:
            if re.search(pattern, normalized_command, re.IGNORECASE):
                block(
                    "Blocked by guard_commands.py: this command matches a rule "
                    "in OPERATING-RULES.md's 'Agents may not' list "
                    f"(pattern: {pattern}).\n"
                    f"Command: {command}\n"
                    f"{ESCALATE}\n"
                    "See guardrails.json (blocked_command_patterns) for the "
                    "exact rule."
                )
        except re.error:
            continue  # a malformed pattern in guardrails.json must not crash the hook

    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or ""
    hit_branch = check_push_targets(command, guardrails.get("protected_branches", []), cwd)
    if hit_branch:
        block(
            "Blocked by guard_commands.py: this `git push` resolves to "
            f"protected branch '{hit_branch}' (directly, via HEAD, via the "
            "current branch, or via --all/--mirror).\n"
            f"Command: {command}\n"
            f"{ESCALATE}\n"
            "See guardrails.json (protected_branches) for the exact rule."
        )

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
