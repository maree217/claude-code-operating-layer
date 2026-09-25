import unittest

from helpers import run_hook, bash_payload


class TestGuardCommands(unittest.TestCase):
    def test_force_push_blocked(self):
        rc, out, err = run_hook("guard_commands.py", bash_payload("git push --force origin main"))
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")
        self.assertIn("OPERATING-RULES.md", err)

    def test_force_push_short_flag_blocked(self):
        rc, out, err = run_hook("guard_commands.py", bash_payload("git push -f origin main"))
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_push_to_main_blocked(self):
        rc, out, err = run_hook("guard_commands.py", bash_payload("git push origin main"))
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")
        self.assertIn("Escalate to", err)

    def test_push_to_feature_branch_allowed(self):
        rc, out, err = run_hook("guard_commands.py", bash_payload("git push origin feature/triage-draft"))
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")

    def test_gh_pr_merge_blocked(self):
        rc, out, err = run_hook("guard_commands.py", bash_payload("gh pr merge 42 --squash"))
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_gh_pr_review_approve_blocked(self):
        rc, out, err = run_hook("guard_commands.py", bash_payload("gh pr review 42 --approve"))
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_benign_git_status_allowed(self):
        rc, out, err = run_hook("guard_commands.py", bash_payload("git status"))
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")

    def test_destructive_rm_rf_blocked(self):
        rc, out, err = run_hook("guard_commands.py", bash_payload("rm -rf src/important"))
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_rm_rf_in_tmp_allowed(self):
        rc, out, err = run_hook("guard_commands.py", bash_payload("rm -rf /tmp/scratch-build"))
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")

    def test_terraform_apply_blocked(self):
        rc, out, err = run_hook("guard_commands.py", bash_payload("terraform apply -auto-approve"))
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_kubectl_apply_blocked(self):
        rc, out, err = run_hook("guard_commands.py", bash_payload("kubectl apply -f deploy.yaml"))
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_non_bash_tool_ignored(self):
        payload = {"tool_name": "Read", "tool_input": {"file_path": "/tmp/x"}}
        rc, out, err = run_hook("guard_commands.py", payload)
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
