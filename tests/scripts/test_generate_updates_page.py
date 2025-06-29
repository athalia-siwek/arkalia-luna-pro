import subprocess
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts.generate_updates_page import main as run


class TestGenerateUpdatesPage(unittest.TestCase):
    @patch("subprocess.run")
    def test_run_success(self, mock_subprocess_run) -> None:
        # Mock the subprocess.run to simulate git log output
        mock_result = MagicMock()
        mock_result.stdout = "abc123 - Fix bug (2023-10-01)\n"
        mock_subprocess_run.return_value = mock_result

        # Run the function
        run()

        # Check that the file was created with the expected content
        output_file = Path("docs/releases/dernieres_updates.md")
        self.assertTrue(output_file.exists())
        with output_file.open("r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("# 🕒 Dernières Updates", content)
            self.assertIn("abc123 - Fix bug (2023-10-01)", content)

    @patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(1, "git log", "Error"),
    )
    def test_run_failure(self, mock_subprocess_run) -> None:
        # Run the function and capture the output
        with self.assertLogs(level="INFO") as log:
            run()
            self.assertIn("❌ Erreur lors de l'exécution de git log", log.output[0])


if __name__ == "__main__":
    unittest.main()
