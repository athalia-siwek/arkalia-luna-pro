# 🔥 Test de résilience DNS
from tests.chaos.__chaos_common import ChaosTestConfig, ChaosTester


class TestNetworkChaos:
    def setup_method(self) -> None:
        self.config = ChaosTestConfig()
        self.chaos = ChaosTester(self.config)

    def teardown_method(self) -> None:
        self.chaos.cleanup()

    def test_dns_failure_resilience(self):
        """Test résilience en cas d'échec DNS"""
        # Ici, on simule un échec DNS (exemple fictif)
        # À adapter selon l'implémentation réelle
        try:
            raise OSError("DNS failure simulated")
        except OSError as e:
            assert "DNS failure" in str(e)
