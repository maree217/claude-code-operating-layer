"""Shared test helpers — not a test module itself (doesn't start with
test_), so `unittest discover` won't try to collect it."""
import json
import os
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HOOKS_DIR = os.path.join(REPO_ROOT, ".claude", "hooks")


def run_hook(hook_name: str, payload: dict, project_dir: str = None):
    """Run a hook script as a real subprocess, feeding `payload` as JSON on
    stdin, exactly how Claude Code invokes it. Returns (returncode, stdout,
    stderr). `project_dir`, if given, is passed as CLAUDE_PROJECT_DIR so a
    test can point the hook at a temp guardrails.json / operating-layer
    without touching the real repo."""
    env = dict(os.environ)
    if project_dir:
        env["CLAUDE_PROJECT_DIR"] = project_dir
    else:
        env.pop("CLAUDE_PROJECT_DIR", None)  # force the walk-up fallback onto the real repo

    proc = subprocess.run(
        [sys.executable, os.path.join(HOOKS_DIR, hook_name)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        timeout=15,
    )
    return proc.returncode, proc.stdout, proc.stderr


def bash_payload(command: str, session_id: str = "test-session", cwd: str = None):
    return {
        "session_id": session_id,
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": cwd or REPO_ROOT,
    }


def make_git_repo(path: str, branch: str = "main"):
    """Create a real git repo at `path` on `branch`, with no commits (an
    "unborn" branch — the shape a freshly `git init`'d repo has). Used to
    test guard_commands.py's current-branch resolution against a real
    `git symbolic-ref`/`rev-parse`, not a mock."""
    subprocess.run(["git", "init", "-q", "-b", branch, path], check=True,
                    capture_output=True, text=True)
    subprocess.run(["git", "-C", path, "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", path, "config", "user.name", "Test"], check=True)


def write_payload(file_path: str, content: str, session_id: str = "test-session"):
    return {
        "session_id": session_id,
        "tool_name": "Write",
        "tool_input": {"file_path": file_path, "content": content},
        "cwd": REPO_ROOT,
    }


def edit_payload(file_path: str, old_string: str, new_string: str,
                  replace_all: bool = False, session_id: str = "test-session"):
    return {
        "session_id": session_id,
        "tool_name": "Edit",
        "tool_input": {
            "file_path": file_path,
            "old_string": old_string,
            "new_string": new_string,
            "replace_all": replace_all,
        },
        "cwd": REPO_ROOT,
    }
