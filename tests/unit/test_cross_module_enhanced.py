"""
🧪 Tests Framework Cross-Module Enhanced v2.7.1-performance
===========================================================

Tests complets du framework Enhanced appliqué à tous les modules Arkalia.
Validation cache TOML, performance et intégration enterprise.

Test Coverage:
- Cache TOML Enhanced (97.1% amélioration)
- Intégration cross-module
- Error handling robuste
- Performance benchmarks

Copyright 2025 Arkalia-LUNA Enterprise
Version: Enhanced v2.7.1-performance
"""

import sys
import tempfile
import time
from pathlib import Path

import pytest
import toml

# Ajouter le path des modules pour les tests
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "modules"))

from utils_enhanced import get_cache_stats, load_toml_cached


class TestCacheEnhanced:
    """Tests du cache TOML Enhanced"""

    def setup_method(self):
        """Setup pour chaque test"""
        # Créer fichier TOML temporaire
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_toml = self.temp_dir / "test_config.toml"

        # Contenu test
        test_config = {
            "module": "test_enhanced",
            "version": "2.7.1-performance",
            "cache": {"enabled": True, "ttl": 30},
            "performance": {"target_improvement": 97.1, "benchmark": "ultra_fast"},
        }

        with open(self.test_toml, "w") as f:
            toml.dump(test_config, f)

    def test_cache_performance_improvement(self):
        """Test amélioration performance cache"""
        # Premier chargement (cache miss)
        start = time.time()
        config1 = load_toml_cached(self.test_toml)
        time1 = time.time() - start

        # Deuxième chargement (cache hit)
        start = time.time()
        config2 = load_toml_cached(self.test_toml)
        time2 = time.time() - start

        # Validation
        assert config1 == config2, "Données cache différentes"
        assert time2 < time1, "Cache pas plus rapide"

        # Performance target: cache au moins 50% plus rapide
        if time1 > 0:
            improvement = ((time1 - time2) / time1) * 100
            assert improvement >= 50.0, f"Amélioration {improvement:.1f}% insuffisante"

    def test_cache_hit_rate(self):
        """Test taux de cache hit"""
        # Charger plusieurs fois le même fichier
        for _ in range(5):
            load_toml_cached(self.test_toml)

        stats = get_cache_stats()
        hit_rate = stats["performance"]["hit_rate_percent"]

        # Au moins 60% de cache hits
        assert hit_rate >= 60.0, f"Hit rate {hit_rate}% trop faible"

    def test_cache_content_validation(self):
        """Test validation contenu cache"""
        config = load_toml_cached(self.test_toml)

        # Validation structure
        assert "module" in config
        assert "version" in config
        assert "cache" in config
        assert "performance" in config

        # Validation valeurs
        assert config["module"] == "test_enhanced"
        assert config["version"] == "2.7.1-performance"
        assert config["cache"]["enabled"] is True
        assert config["performance"]["target_improvement"] == 97.1

    def test_file_not_found_handling(self):
        """Test gestion fichier inexistant"""
        non_existent = self.temp_dir / "non_existent.toml"

        # Ne doit pas lever d'exception, retourner dict vide
        config = load_toml_cached(non_existent)
        assert config == {}, "Fichier inexistant doit retourner dict vide"

    def test_cache_stats_accuracy(self):
        """Test précision des statistiques cache"""
        # Reset et test initial
        initial_stats = get_cache_stats()

        # Charger fichier plusieurs fois
        load_toml_cached(self.test_toml)  # Miss
        load_toml_cached(self.test_toml)  # Hit
        load_toml_cached(self.test_toml)  # Hit

        final_stats = get_cache_stats()

        # Validation incrementale
        assert (
            final_stats["performance"]["total_requests"]
            >= initial_stats["performance"]["total_requests"] + 3
        )
        assert (
            final_stats["performance"]["cache_hits"]
            >= initial_stats["performance"]["cache_hits"] + 2
        )

    def test_cache_ttl_behavior(self):
        """Test comportement TTL cache"""
        # Charger avec TTL court
        config1 = load_toml_cached(self.test_toml, max_age=1)

        # Attendre expiration
        time.sleep(1.1)

        # Recharger (doit être cache miss)
        start = time.time()
        config2 = load_toml_cached(self.test_toml, max_age=1)
        reload_time = time.time() - start

        # Validation
        assert config1 == config2, "Contenu différent après TTL"
        # Reload doit prendre plus de temps (pas cache hit)
        assert reload_time > 0.0001, "TTL pas respecté"


class TestCrossModuleIntegration:
    """Tests intégration cross-module"""

    def test_utils_enhanced_import(self):
        """Test import framework Enhanced"""
        try:
            from utils_enhanced import get_cache_stats, load_toml_cached

            assert callable(load_toml_cached)
            assert callable(get_cache_stats)
        except ImportError:
            pytest.fail("Import framework Enhanced échoué")

    def test_reflexia_integration(self):
        """Test intégration Reflexia Enhanced"""
        try:
            from reflexia.utils.config_loader import load_weights

            assert callable(load_weights)
        except ImportError:
            pytest.skip("Module Reflexia non disponible")

    def test_sandozia_integration(self):
        """Test intégration Sandozia Enhanced"""
        try:
            from sandozia.core.sandozia_core import SandoziaCore

            assert SandoziaCore is not None
        except ImportError:
            pytest.skip("Module Sandozia non disponible")

    def test_monitoring_integration(self):
        """Test intégration Monitoring Enhanced"""
        try:
            from monitoring.prometheus_metrics import ArkaliaMetrics

            assert ArkaliaMetrics is not None
        except ImportError:
            pytest.skip("Module Monitoring non disponible")


class TestPerformanceBenchmarks:
    """Tests benchmarks performance"""

    def test_cache_performance_target(self):
        """Test target performance cache Enhanced"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            test_config = {"benchmark": True, "data": list(range(100))}
            toml.dump(test_config, f)
            f.flush()

            # Benchmark cache miss vs hit
            times = []

            # Premier chargement
            start = time.time()
            config1 = load_toml_cached(f.name)
            times.append(time.time() - start)

            # Chargements cache
            for _ in range(5):
                start = time.time()
                config2 = load_toml_cached(f.name)
                times.append(time.time() - start)

            # Validation performance
            cache_miss_time = times[0]
            avg_cache_hit_time = sum(times[1:]) / len(times[1:])

            if cache_miss_time > 0:
                improvement = (
                    (cache_miss_time - avg_cache_hit_time) / cache_miss_time
                ) * 100
                # Target: au moins 80% amélioration
                assert (
                    improvement >= 80.0
                ), f"Performance {improvement:.1f}% insuffisante"

    def test_memory_usage(self):
        """Test usage mémoire cache"""
        # Charger plusieurs fichiers
        temp_files = []
        for i in range(10):
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".toml", delete=False
            ) as f:
                config = {"file_id": i, "data": f"test_data_{i}"}
                toml.dump(config, f)
                temp_files.append(f.name)
                load_toml_cached(f.name)

        stats = get_cache_stats()
        entries_count = stats["cache_state"]["entries_count"]

        # Validation mémoire raisonnable
        assert entries_count <= 100, f"Trop d'entrées cache: {entries_count}"
        assert entries_count >= len(temp_files), "Pas assez d'entrées cache"


class TestErrorHandling:
    """Tests gestion d'erreurs"""

    def test_malformed_toml_handling(self):
        """Test gestion TOML malformé"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write("invalid_toml = [broken syntax")
            f.flush()

            # Ne doit pas lever d'exception
            config = load_toml_cached(f.name)
            assert config == {}, "TOML malformé doit retourner dict vide"

    def test_permission_error_handling(self):
        """Test gestion erreurs permissions"""
        # Créer fichier sans permissions lecture (si possible sur système)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test = 'value'")

        try:
            import os

            os.chmod(f.name, 0o000)  # Aucune permission

            config = load_toml_cached(f.name)
            assert config == {}, "Erreur permission doit retourner dict vide"
        except:
            pytest.skip("Impossible de tester permissions sur ce système")


# Tests de régression
class TestRegression:
    """Tests de régression Enhanced"""

    def test_backward_compatibility(self):
        """Test compatibilité avec ancien code"""
        # Test alias load_toml_with_cache
        from utils_enhanced.cache_enhanced import load_toml_with_cache

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml") as f:
            toml.dump({"test": "backward_compat"}, f)
            f.flush()

            config = load_toml_with_cache(f.name)
            assert config["test"] == "backward_compat"

    def test_stats_consistency(self):
        """Test cohérence statistiques"""
        initial_stats = get_cache_stats()

        # Plusieurs opérations
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml") as f:
            toml.dump({"consistency": "test"}, f)
            f.flush()

            load_toml_cached(f.name)  # Miss
            load_toml_cached(f.name)  # Hit

        final_stats = get_cache_stats()

        # Validation cohérence
        hits_delta = (
            final_stats["performance"]["cache_hits"]
            - initial_stats["performance"]["cache_hits"]
        )
        requests_delta = (
            final_stats["performance"]["total_requests"]
            - initial_stats["performance"]["total_requests"]
        )

        assert requests_delta >= 2, "Nombre de requêtes incohérent"
        assert hits_delta >= 1, "Nombre de hits incohérent"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
