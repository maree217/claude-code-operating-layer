import json
import os
import tempfile
import unittest

from helpers import run_hook

TOTAL_CHAR_CAP = 2000


class TestSessionBrief(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        with open(os.path.join(self.root, "guardrails.json"), "w") as f:
            json.dump({}, f)
        os.makedirs(os.path.join(self.root, "operating-layer"), exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, name, content):
        with open(os.path.join(self.root, "operating-layer", name), "w") as f:
            f.write(content)

    def test_brief_within_char_cap_and_contains_sections(self):
        self._write(
            "OPERATING-RULES.md",
            "# Operating rules\n\n## Agents may\n\n- draft\n\n"
            "## Agents may not\n\n- push to main\n- approve own work\n\n"
            "## Escalate to a person\n\n- anything irreversible\n",
        )
        self._write(
            "BETS-REGISTER.md",
            "# Bets register\n\n## Live bets\n\n| Bet | Owner |\n|---|---|\n"
            "| triage | Sales Ops |\n\n## Recently decided\n\n- none\n",
        )
        rc, out, err = run_hook("session_brief.py", {"cwd": self.root}, project_dir=self.root)
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")
        self.assertTrue(out.strip(), "expected additionalContext JSON on stdout")
        payload = json.loads(out)
        brief = payload["hookSpecificOutput"]["additionalContext"]
        self.assertLessEqual(len(brief), TOTAL_CHAR_CAP)
        self.assertIn("push to main", brief)
        self.assertIn("triage", brief)
        self.assertNotIn("Escalate to a person", brief)  # stops before the NEXT ## header

    def test_oversized_section_is_truncated_not_dropped(self):
        huge_rules = "# Operating rules\n\n## Agents may not\n\n" + "\n".join(
            f"- rule number {i}" for i in range(500)
        )
        self._write("OPERATING-RULES.md", huge_rules)
        self._write("BETS-REGISTER.md", "# Bets register\n\n## Live bets\n\n- none\n")
        rc, out, err = run_hook("session_brief.py", {"cwd": self.root}, project_dir=self.root)
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        brief = payload["hookSpecificOutput"]["additionalContext"]
        self.assertLessEqual(len(brief), TOTAL_CHAR_CAP)
        self.assertIn("truncated", brief.lower())

    def test_missing_files_stays_silent(self):
        rc, out, err = run_hook("session_brief.py", {"cwd": self.root}, project_dir=self.root)
        self.assertEqual(rc, 0)
        self.assertEqual(out.strip(), "")


if __name__ == "__main__":
    unittest.main()
