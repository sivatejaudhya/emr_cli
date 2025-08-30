"""Smoke tests for EMR CLI."""

import os
import sys
import unittest
import subprocess

BASE_DIR = os.path.dirname(__file__)
EMR_PATH = os.path.join(BASE_DIR, "emr_cli.py")


class SmokeTest(unittest.TestCase):
    """Basic smoke tests for the EMR CLI."""

    def test_list_patients(self):
        """Test 'list' command returns expected output."""
        process = subprocess.run(
            [sys.executable, EMR_PATH, "list", "--limit", "5"],
            capture_output=True,
            check=True,
            text=True,
        )
        self.assertEqual(process.returncode, 0)
        self.assertIn("Asha Kumari", process.stdout)


if __name__ == "__main__":
    unittest.main()
