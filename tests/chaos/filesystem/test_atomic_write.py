# 🔥 Test de résilience écriture atomique sous charge
import time
from pathlib import Path

import toml

from tests.chaos.chaos_common import ChaosTestConfig, ChaosTester
from utils.io_safe import atomic_write


class TestFileSystemChaos:
    def setup_method(self) -> None:
        self.config = ChaosTestConfig()
        self.chaos = ChaosTester(self.config)

    def teardown_method(self) -> None:
        self.chaos.cleanup()

    def test_atomic_write_resilience(self):
        """🔥 Test résilience écriture atomique sous charge"""
        test_file = Path("test_atomic_chaos.toml")
        try:
            test_data = {"test": True, "timestamp": time.time()}
            self.chaos.simulate_high_load(duration=2)
            atomic_write(test_file, toml.dumps(test_data))
            assert test_file.exists()
            content = toml.load(test_file)
            assert content["test"] is True
        finally:
            if test_file.exists():
                test_file.unlink()
