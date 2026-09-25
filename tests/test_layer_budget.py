import json
import os
import tempfile
import unittest

from helpers import run_hook, write_payload, edit_payload

BUDGET = 10  # small budget so the test doesn't need a 80-line fixture


class TestLayerBudget(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        with open(os.path.join(self.root, "guardrails.json"), "w") as f:
            json.dump({
                "protected_branches": [],
                "protected_paths": [],
                "blocked_command_patterns": [],
                "outbound_allowlist": [],
                "operating_layer_line_budget": BUDGET,
            }, f)
        os.makedirs(os.path.join(self.root, "operating-layer"), exist_ok=True)
        self.target = os.path.join(self.root, "operating-layer", "COMPANY-BRAIN.md")

    def tearDown(self):
        self.tmp.cleanup()

    def test_write_over_budget_blocked(self):
        content = "\n".join(f"line {i}" for i in range(BUDGET + 5))
        rc, out, err = run_hook("layer_budget.py", write_payload(self.target, content), project_dir=self.root)
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")
        self.assertIn("prune", err.lower())

    def test_write_under_budget_allowed(self):
        content = "\n".join(f"line {i}" for i in range(BUDGET - 2))
        rc, out, err = run_hook("layer_budget.py", write_payload(self.target, content), project_dir=self.root)
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")

    def test_edit_pushing_over_budget_blocked(self):
        # Seed a file already at budget - 1 lines.
        existing = "\n".join(f"line {i}" for i in range(BUDGET - 1))
        with open(self.target, "w") as f:
            f.write(existing)
        # Append several new lines via Edit — pushes it over budget.
        payload = edit_payload(
            self.target,
            old_string=f"line {BUDGET - 2}",
            new_string=f"line {BUDGET - 2}\nextra a\nextra b\nextra c",
        )
        rc, out, err = run_hook("layer_budget.py", payload, project_dir=self.root)
        self.assertEqual(rc, 2, f"stdout={out!r} stderr={err!r}")

    def test_edit_within_budget_allowed(self):
        existing = "\n".join(f"line {i}" for i in range(BUDGET - 3))
        with open(self.target, "w") as f:
            f.write(existing)
        payload = edit_payload(
            self.target,
            old_string="line 0",
            new_string="line 0 (edited)",
        )
        rc, out, err = run_hook("layer_budget.py", payload, project_dir=self.root)
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")

    def test_write_outside_operating_layer_ignored(self):
        other = os.path.join(self.root, "README.md")
        content = "\n".join(f"line {i}" for i in range(BUDGET + 20))
        rc, out, err = run_hook("layer_budget.py", write_payload(other, content), project_dir=self.root)
        self.assertEqual(rc, 0, f"stdout={out!r} stderr={err!r}")


if __name__ == "__main__":
    unittest.main()
