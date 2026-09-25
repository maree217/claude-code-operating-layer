import unittest

from helpers import run_hook, write_payload, edit_payload, REPO_ROOT
import os


class TestGuardPaths(unittest.TestCase):
    def test_write_to_infra_blocked(self):
        payload = write_payload(os.path.join(REPO_ROOT, "infra", "main.tf"), "resource {}\n")
        rc, out, err = run_hook("guard_paths.py", payload)
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")
        self.assertIn("protected path", err)

    def test_write_to_deploy_blocked(self):
        payload = write_payload(os.path.join(REPO_ROOT, "deploy", "prod.yaml"), "x: 1\n")
        rc, out, err = run_hook("guard_paths.py", payload)
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_write_to_workflows_blocked(self):
        payload = write_payload(
            os.path.join(REPO_ROOT, ".github", "workflows", "new.yml"), "on: push\n"
        )
        rc, out, err = run_hook("guard_paths.py", payload)
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_write_to_src_allowed(self):
        payload = write_payload(os.path.join(REPO_ROOT, "src", "app.py"), "print('hi')\n")
        rc, out, err = run_hook("guard_paths.py", payload)
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")

    def test_edit_infra_blocked(self):
        payload = edit_payload(
            os.path.join(REPO_ROOT, "infra", "main.tf"), "old", "new"
        )
        rc, out, err = run_hook("guard_paths.py", payload)
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_operating_layer_not_protected_by_this_hook(self):
        # operating-layer/** is deliberately not in protected_paths — its
        # control is layer_budget.py, not guard_paths.py.
        payload = write_payload(
            os.path.join(REPO_ROOT, "operating-layer", "COMPANY-BRAIN.md"), "# ok\n"
        )
        rc, out, err = run_hook("guard_paths.py", payload)
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")

    def test_non_watched_tool_ignored(self):
        payload = {"tool_name": "Bash", "tool_input": {"command": "ls infra/"}}
        rc, out, err = run_hook("guard_paths.py", payload)
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
