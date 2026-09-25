import tempfile
import unittest

from helpers import run_hook, bash_payload, make_git_repo


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

    def test_git_C_dot_push_origin_main_blocked(self):
        # git global options (-C, -c, --git-dir=, etc.) sit between `git`
        # and the subcommand — a naive `\bgit\s+push\b` pattern doesn't
        # see past them without normalization.
        rc, out, err = run_hook("guard_commands.py", bash_payload("git -C . push origin main"))
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_git_config_option_then_push_main_blocked(self):
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("git -c core.pager=cat push origin main")
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_bash_dash_c_wrapped_push_blocked(self):
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload('bash -c "git push origin main"')
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_sh_dash_c_wrapped_push_blocked(self):
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("sh -c 'git push origin main'")
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_semicolon_chained_push_blocked(self):
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("git status; git push origin main")
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_or_chained_push_blocked(self):
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("git push origin main || true")
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_pipe_chained_push_blocked(self):
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("git push origin main | cat")
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_newline_chained_push_blocked(self):
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("git status\ngit push origin main")
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_colon_refspec_dest_main_blocked(self):
        # `git push origin HEAD:main` — the DESTINATION (after the colon)
        # is what matters, regardless of the source or current branch.
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("git push origin HEAD:main")
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_colon_refspec_dest_non_protected_allowed(self):
        rc, out, err = run_hook(
            "guard_commands.py",
            bash_payload("git push origin HEAD:refs/heads/feature-review"),
        )
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")


class TestPushCurrentBranchResolution(unittest.TestCase):
    """These are the gaps flagged in review: a push with no explicit,
    named destination branch has to be resolved against the real current
    branch of the repo the command would run in — via a real git repo in
    a temp dir, not a mock."""

    def setUp(self):
        self.main_tmp = tempfile.TemporaryDirectory()
        self.feature_tmp = tempfile.TemporaryDirectory()
        make_git_repo(self.main_tmp.name, branch="main")
        make_git_repo(self.feature_tmp.name, branch="feature-x")

    def tearDown(self):
        self.main_tmp.cleanup()
        self.feature_tmp.cleanup()

    def test_bare_git_push_on_main_blocked(self):
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("git push", cwd=self.main_tmp.name)
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")
        self.assertIn("main", err)

    def test_bare_git_push_on_feature_branch_allowed(self):
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("git push", cwd=self.feature_tmp.name)
        )
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")

    def test_git_push_remote_only_on_main_blocked(self):
        # `git push origin` — a remote with no refspec pushes the current
        # branch, same as a bare `git push`.
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("git push origin", cwd=self.main_tmp.name)
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_git_push_remote_only_on_feature_allowed(self):
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("git push origin", cwd=self.feature_tmp.name)
        )
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")

    def test_push_dash_u_origin_head_on_main_blocked(self):
        rc, out, err = run_hook(
            "guard_commands.py",
            bash_payload("git push -u origin HEAD", cwd=self.main_tmp.name),
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_push_dash_u_origin_head_on_feature_allowed(self):
        rc, out, err = run_hook(
            "guard_commands.py",
            bash_payload("git push -u origin HEAD", cwd=self.feature_tmp.name),
        )
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")

    def test_git_C_dot_push_origin_main_resolved_against_real_repo(self):
        # Combine both gaps: global option before the subcommand, on a
        # real repo whose current branch is main.
        rc, out, err = run_hook(
            "guard_commands.py",
            bash_payload("git -C . push origin main", cwd=self.main_tmp.name),
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_push_all_on_main_blocked(self):
        rc, out, err = run_hook(
            "guard_commands.py", bash_payload("git push --all", cwd=self.main_tmp.name)
        )
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_bare_push_outside_any_repo_fails_open(self):
        # Not a git repo at all — current-branch resolution can't succeed,
        # so this fails open (same fail-open contract as every other hook
        # in this kit) rather than blocking on a guessed branch name.
        with tempfile.TemporaryDirectory() as not_a_repo:
            rc, out, err = run_hook(
                "guard_commands.py", bash_payload("git push", cwd=not_a_repo)
            )
            self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")


if __name__ == "__main__":
    unittest.main()
