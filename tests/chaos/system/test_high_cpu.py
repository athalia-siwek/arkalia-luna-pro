# 🔥 Test de charge CPU élevée
from tests.chaos.common import ChaosTestConfig, ChaosTester


class TestSystemLoadChaos:
    def setup_method(self):
        self.config = ChaosTestConfig()
        self.chaos = ChaosTester(self.config)

    def teardown_method(self):
        self.chaos.cleanup()

    def test_system_under_high_cpu_load(self):
        """Test système sous forte charge CPU"""
        process = self.chaos.simulate_high_load(duration=3)
        assert process is not None
        process.terminate()
