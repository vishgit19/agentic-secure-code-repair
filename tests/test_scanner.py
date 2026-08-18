from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from secure_repair.scanner import build_patch, scan_path, scan_source


class ScannerTests(unittest.TestCase):
    def test_detects_high_risk_calls(self) -> None:
        source = """
import subprocess
import requests

subprocess.run(user_input, shell=True)
requests.get(url, verify=False)
eval(user_input)
"""
        findings = scan_source(source, "example.py")
        self.assertEqual({item.rule_id for item in findings}, {"SR001", "SR002", "SR003"})

    def test_detects_likely_secret_but_ignores_short_placeholder(self) -> None:
        source = 'api_key = "sk-live-1234567890"\npassword = "example"\n'
        findings = scan_source(source, "settings.py")
        self.assertEqual([item.rule_id for item in findings], ["SR007"])

    def test_reports_syntax_errors_without_crashing(self) -> None:
        findings = scan_source("def nope(:\n", "broken.py")
        self.assertEqual(findings[0].rule_id, "SR000")

    def test_patch_changes_only_supported_boolean_repairs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "app.py"
            path.write_text(
                "requests.get(url, verify=False)\napp.run(debug=True)\neval(payload)\n",
                encoding="utf-8",
            )
            findings = scan_path(path)
            patch = build_patch(findings)
            self.assertIn("verify=True", patch)
            self.assertIn("debug=False", patch)
            self.assertNotIn("+eval", patch)


if __name__ == "__main__":
    unittest.main()
