import unittest
from unittest.mock import patch


class TestZeroiaHealth(unittest.TestCase):
    @patch("toml.load")
    def test_zeroia_state_ok(self, mock_toml_load) -> None:
        # Mock the toml.load to simulate successful loading
        mock_toml_load.return_value = {"key": "value"}

        # Capture the output
        with self.assertLogs(level="INFO") as log:
            exec(open("scripts/zeroia_health.py").read())
            if log.output:
                self.assertIn("✅ ZeroIA State: OK", log.output[0])
            else:
                self.fail("Aucun message de log capturé.")

    @patch("toml.load", side_effect=Exception("File not found"))
    def test_zeroia_state_error(self, mock_toml_load) -> None:
        # Capture the output
        with self.assertLogs(level="INFO") as log:
            with self.assertRaises(SystemExit):
                exec(open("scripts/zeroia_health.py").read())
            if log.output:
                self.assertIn("💥 ZeroIA State Error: File not found", log.output[0])
            else:
                self.fail("Aucun message de log capturé.")


if __name__ == "__main__":
    unittest.main()
