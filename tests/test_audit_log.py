import json
import os
import tempfile
import unittest

from helpers import run_hook


class TestAuditLog(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        with open(os.path.join(self.root, "guardrails.json"), "w") as f:
            json.dump({}, f)
        self.log_path = os.path.join(self.root, ".claude", "audit", "actions.jsonl")

    def tearDown(self):
        self.tmp.cleanup()

    def _read_last_entry(self):
        with open(self.log_path, encoding="utf-8") as f:
            lines = [l for l in f.read().splitlines() if l.strip()]
        return json.loads(lines[-1])

    def test_line_written_for_bash(self):
        payload = {
            "session_id": "abc123",
            "tool_name": "Bash",
            "tool_input": {"command": "npm test"},
        }
        rc, out, err = run_hook("audit_log.py", payload, project_dir=self.root)
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")
        self.assertTrue(os.path.isfile(self.log_path))
        entry = self._read_last_entry()
        self.assertEqual(entry["tool"], "Bash")
        self.assertEqual(entry["session_id"], "abc123")
        self.assertIn("npm test", entry["summary"])
        self.assertIn("ts", entry)

    def test_long_command_truncated(self):
        long_command = "echo " + ("x" * 500)
        payload = {"session_id": "s2", "tool_name": "Bash", "tool_input": {"command": long_command}}
        run_hook("audit_log.py", payload, project_dir=self.root)
        entry = self._read_last_entry()
        self.assertLessEqual(len(entry["summary"]), 220)  # tool prefix + 200-char cap
        self.assertTrue(entry["summary"].endswith("..."))

    def test_never_dumps_full_file_content(self):
        payload = {
            "session_id": "s3",
            "tool_name": "Write",
            "tool_input": {"file_path": "/tmp/secret.txt", "content": "API_KEY=super-secret-value-do-not-log"},
        }
        run_hook("audit_log.py", payload, project_dir=self.root)
        entry = self._read_last_entry()
        self.assertNotIn("super-secret-value-do-not-log", entry["summary"])
        self.assertIn("/tmp/secret.txt", entry["summary"])

    def test_multiple_calls_append(self):
        for i in range(3):
            run_hook("audit_log.py", {"session_id": f"s{i}", "tool_name": "Bash",
                                       "tool_input": {"command": f"echo {i}"}}, project_dir=self.root)
        with open(self.log_path) as f:
            lines = [l for l in f.read().splitlines() if l.strip()]
        self.assertEqual(len(lines), 3)


if __name__ == "__main__":
    unittest.main()
