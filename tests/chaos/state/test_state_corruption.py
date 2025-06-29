# 🔥 Test de corruption d'état
from pathlib import Path

from tests.chaos.common import ChaosTestConfig, ChaosTester


class TestStatePersistenceChaos:
    def setup_method(self) -> None:
        self.config = ChaosTestConfig()
        self.chaos = ChaosTester(self.config)

    def teardown_method(self) -> None:
        self.chaos.cleanup()

    def test_state_corruption_recovery(self):
        """Test récupération après corruption d'état"""
        state_file = Path("state/zeroia_state.toml")
        # Simule la corruption
        self.chaos.corrupt_file(state_file)
        # Ici, on simule la récupération (à adapter selon la logique réelle)
        self.chaos.restore_files()
        assert state_file.exists() and state_file.read_text() != ""
