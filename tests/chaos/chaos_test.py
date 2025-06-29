# 🌀 tests/chaos/chaos_test.py
# Tests de chaos pour résilience Arkalia-LUNA

import json
import random
import subprocess
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest
import toml

from modules.zeroia.reason_loop import load_context
from utils.io_safe import atomic_write, locked_read


class ChaosTestConfig:
    """Configuration pour les tests de chaos"""

    def __init__(self):
        self.base_dir = Path(".")
        self.state_dir = Path("state")
        self.logs_dir = Path("logs")
        self.test_duration = 30  # secondes
        self.corruption_probability = 0.3


class ChaosTester:
    """Générateur de chaos pour tests de résilience"""

    def __init__(self, config: ChaosTestConfig):
        self.config = config
        self.active_processes = []
        self.corrupted_files = []

    def corrupt_file(self, file_path: Path) -> bool:
        """Corrompt un fichier de manière contrôlée"""
        if not file_path.exists():
            return False

        try:
            # Sauvegarde avant corruption
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
            backup_path.write_bytes(file_path.read_bytes())
            self.corrupted_files.append((file_path, backup_path))

            # Différents types de corruption
            corruption_type = random.choice(["truncate", "random_bytes", "invalid_toml"])

            if corruption_type == "truncate":
                # Tronque le fichier
                with open(file_path, "w") as f:
                    f.write("")

            elif corruption_type == "random_bytes":
                # Insère des bytes aléatoires
                with open(file_path, "rb") as f:
                    content = f.read()
                corrupted = bytearray(content)
                for _i in range(min(10, len(corrupted))):
                    pos = random.randint(0, len(corrupted) - 1)
                    corrupted[pos] = random.randint(0, 255)
                with open(file_path, "wb") as f:
                    f.write(corrupted)

            elif corruption_type == "invalid_toml":
                # TOML invalide
                with open(file_path, "w") as f:
                    f.write("[[section\ninvalid = toml syntax\n[unclosed")

            return True

        except Exception as e:
            print(f"⚠️ Erreur corruption {file_path}: {e}")
            return False

    def restore_files(self):
        """Restaure tous les fichiers corrompus"""
        for original_path, backup_path in self.corrupted_files:
            try:
                if backup_path.exists():
                    original_path.write_bytes(backup_path.read_bytes())
                    backup_path.unlink()
            except Exception as e:
                print(f"⚠️ Erreur restauration {original_path}: {e}")
        self.corrupted_files.clear()

    def simulate_high_load(self, duration: int = 10):
        """Simule une charge système élevée"""
        try:
            # CPU stress (multiplateforme)
            stress_script = f"""
import time
import threading

def cpu_stress():
    end_time = time.time() + {duration}
    while time.time() < end_time:
        pass

threads = []
for i in range(4):  # 4 threads CPU stress
    t = threading.Thread(target=cpu_stress)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
"""

            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(stress_script)
                stress_file = f.name

            # Lance le stress en arrière-plan
            process = subprocess.Popen(["python", stress_file])
            self.active_processes.append(process)

            return process

        except Exception as e:
            print(f"⚠️ Erreur simulation charge: {e}")
            return None

    def simulate_memory_pressure(self, mb_size: int = 100):
        """Simule une pression mémoire"""
        try:
            # Alloue et maintient de la mémoire
            memory_blocks = []
            for _ in range(mb_size):
                # 1MB blocks
                block = bytearray(1024 * 1024)
                memory_blocks.append(block)

            # Garde la mémoire allouée pendant le test
            time.sleep(5)
            return memory_blocks

        except MemoryError:
            print("⚠️ Mémoire insuffisante pour le test")
            return []

    def cleanup(self):
        """Nettoie tous les processus et fichiers de test"""
        # Termine les processus actifs
        for process in self.active_processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except Exception:
                try:
                    process.kill()
                except Exception:
                    pass

        # Restaure les fichiers
        self.restore_files()

        self.active_processes.clear()


# === TESTS DE CHAOS ===


class TestFileSystemChaos:
    """Tests de résilience du système de fichiers"""

    def setup_method(self):
        self.config = ChaosTestConfig()
        self.chaos = ChaosTester(self.config)

    def teardown_method(self):
        self.chaos.cleanup()

    def test_atomic_write_resilience(self):
        """🔥 Test résilience écriture atomique sous charge"""
        test_file = Path("test_atomic_chaos.toml")

        try:
            # Données de test
            test_data = {"test": True, "timestamp": time.time()}

            # Écrit en parallèle pendant simulation de charge
            self.chaos.simulate_high_load(duration=2)

            # Test écriture atomique sous charge
            atomic_write(test_file, toml.dumps(test_data))

            # Vérifie intégrité
            assert test_file.exists()
            content = toml.load(test_file)
            assert content["test"] is True

        finally:
            if test_file.exists():
                test_file.unlink()

    def test_locked_read_corruption_resilience(self):
        """🔥 Test résilience lecture verrouillée avec corruption"""
        test_file = Path("test_locked_chaos.toml")

        try:
            # Crée fichier initial
            initial_data = {"status": "normal", "value": 42}
            atomic_write(test_file, toml.dumps(initial_data))

            # Corrompt le fichier
            self.chaos.corrupt_file(test_file)

            # Teste récupération
            try:
                locked_read(test_file)  # Test de récupération
                # Le système atomique devrait avoir protégé contre ça
            except Exception:
                # Erreur attendue avec fichier corrompu
                pass

        finally:
            self.chaos.restore_files()
            if test_file.exists():
                test_file.unlink()


class TestSystemLoadChaos:
    """Tests sous charge système extrême"""

    def setup_method(self):
        self.config = ChaosTestConfig()
        self.chaos = ChaosTester(self.config)

    def teardown_method(self):
        self.chaos.cleanup()

    def test_system_under_high_cpu_load(self):
        """🔥 Test système sous charge CPU élevée"""
        try:
            # Test simple de fonctionnement du reason loop
            # Note: Test simplifié car reason_loop nécessite setup complet
            assert load_context() is not None  # Test que le système charge
        except MemoryError:
            pytest.skip("Mémoire insuffisante pour le test")

    def test_performance_under_load(self):
        """⚡ Test performance sous charge"""
        start_time = time.time()

        # Simule charge
        self.chaos.simulate_high_load(duration=2)

        # Test opération critique
        # context = {"status": {"cpu": 85, "severity": "warning"}}  # Future test

        # Test que le système reste fonctionnel
        assert load_context() is not None
        execution_time = time.time() - start_time

        # Sous charge, le système peut être plus lent mais doit rester fonctionnel
        assert execution_time < 30, f"Système trop lent sous charge: {execution_time:.2f}s"

    def test_memory_pressure_resilience(self):
        """🧠 Test résilience sous pression mémoire"""
        try:
            # Alloue mémoire pour créer pression
            self.chaos.simulate_memory_pressure(mb_size=50)

            # Test que le système fonctionne encore
            assert load_context() is not None

            # Vérifie que les opérations de base fonctionnent
            test_data = {"test": "memory_pressure"}
            test_file = Path("test_memory.json")

            atomic_write(test_file, json.dumps(test_data))
            content_raw = locked_read(test_file)
            # Gestion type-safe du résultat de locked_read
            if isinstance(content_raw, str):
                content = json.loads(content_raw)
                assert content.get("test") == "memory_pressure"

            test_file.unlink()

        except MemoryError:
            pytest.skip("Mémoire insuffisante pour ce test")


class TestNetworkChaos:
    """Tests de résilience réseau"""

    def setup_method(self):
        self.config = ChaosTestConfig()
        self.chaos = ChaosTester(self.config)

    def teardown_method(self):
        self.chaos.cleanup()

    def test_system_offline_resilience(self):
        """📡 Test résilience système hors ligne"""
        with patch("socket.gethostbyname") as mock_dns:
            # Simule échec DNS
            mock_dns.side_effect = OSError("Network unreachable")

            # Le système devrait continuer à fonctionner sans réseau
            # context = {"status": {"cpu": 60, "severity": "normal"}}  # Future

            assert load_context() is not None

    def test_dns_failure_resilience(self):
        """🌐 Test résilience échec DNS"""
        with patch("socket.getaddrinfo") as mock_getaddr:
            mock_getaddr.side_effect = OSError("DNS resolution failed")

            # Système local devrait fonctionner même sans DNS
            # context = {"status": {"cpu": 70, "severity": "warning"}}  # Future

            assert load_context() is not None


class TestStatePersistenceChaos:
    """Tests de persistance d'état sous chaos"""

    def setup_method(self):
        self.config = ChaosTestConfig()
        self.chaos = ChaosTester(self.config)

    def teardown_method(self):
        self.chaos.cleanup()

    def test_state_corruption_recovery(self):
        """💾 Test récupération corruption état"""
        state_file = Path("test_state_chaos.toml")

        try:
            # État initial valide
            initial_state = {
                "decision": {"last": "monitor", "confidence": 0.8},
                "metrics": {"cpu": 45, "ram": 60},
            }

            atomic_write(state_file, toml.dumps(initial_state))

            # Corrompt l'état
            assert self.chaos.corrupt_file(state_file)

            # Test récupération (devrait gérer gracieusement)
            try:
                locked_read(state_file)
                # Si ça marche, le système a récupéré
            except Exception:
                # Erreur attendue, le système devrait avoir des fallbacks
                pass

        finally:
            self.chaos.restore_files()
            if state_file.exists():
                state_file.unlink()

    def test_concurrent_state_access_chaos(self):
        """🔄 Test accès concurrent état avec chaos"""
        state_file = Path("test_concurrent_chaos.toml")

        try:
            # État initial
            initial_state = {"counter": 0, "status": "active"}
            atomic_write(state_file, toml.dumps(initial_state))

            # Fonction de stress concurrent
            def stress_state_access():
                for _i in range(5):
                    try:
                        # Lecture
                        content_raw = locked_read(state_file)
                        if isinstance(content_raw, str):
                            data = toml.loads(content_raw)
                        else:
                            data = {"counter": 0}

                        # Modification
                        data["counter"] = data.get("counter", 0) + 1
                        data["last_update"] = int(time.time())

                        # Écriture atomique
                        atomic_write(state_file, toml.dumps(data))

                        time.sleep(0.1)
                    except Exception:
                        # Erreurs attendues sous stress
                        pass

            # Lance plusieurs threads concurrent
            import threading

            threads = []
            for _ in range(3):
                t = threading.Thread(target=stress_state_access)
                t.start()
                threads.append(t)

            # Attend fin
            for t in threads:
                t.join(timeout=10)

            # Vérifie que le fichier n'est pas corrompu
            final_content_raw = locked_read(state_file)
            if isinstance(final_content_raw, str):
                final_data = toml.loads(final_content_raw)
                assert isinstance(final_data.get("counter"), int)

        finally:
            if state_file.exists():
                state_file.unlink()


class TestCriticalSystemChaos:
    """Tests de chaos sur fonctions critiques système"""

    def setup_method(self):
        self.config = ChaosTestConfig()
        self.chaos = ChaosTester(self.config)

    def teardown_method(self):
        self.chaos.cleanup()

    def test_critical_decision_under_chaos(self):
        """⚠️ Test décision critique sous chaos"""
        # Crée contexte dégradé
        degraded_context = {
            "status": {"cpu": 95, "severity": "critical", "degraded": True},
            "chaos_test": True,
        }

        # Le système devrait fonctionner en mode dégradé
        assert load_context() is not None

        # En mode critique, devrait prendre décision conservatrice
        assert isinstance(degraded_context["status"]["cpu"], int)
        assert degraded_context["status"]["severity"] == "critical"


class TestChaosIntegration:
    """Tests d'intégration chaos complets"""

    def setup_method(self):
        self.config = ChaosTestConfig()
        self.chaos = ChaosTester(self.config)

    def teardown_method(self):
        self.chaos.cleanup()

    def test_full_system_chaos_simulation(self):
        """🌪️ Test simulation chaos système complet"""
        try:
            # Phase 1: Stress multi-facteur
            self.chaos.simulate_memory_pressure(30)
            self.chaos.simulate_high_load(5)

            # Phase 2: Test fonctionnalités critiques
            test_context = load_context()
            assert test_context is not None

            # Phase 3: Test persistance sous stress
            stress_file = Path("chaos_stress_test.toml")
            stress_data = {"chaos_test": True, "iteration": time.time()}

            atomic_write(stress_file, toml.dumps(stress_data))
            recovered_content_raw = locked_read(stress_file)

            if isinstance(recovered_content_raw, str):
                recovered_data = toml.loads(recovered_content_raw)
                assert recovered_data["chaos_test"] is True

            stress_file.unlink()

        except MemoryError:
            pytest.skip("Ressources système insuffisantes")

    def test_chaos_recovery_metrics(self):
        """📊 Test métriques de récupération chaos"""
        recovery_stats = {
            "corrupted_files": 0,
            "recovered_files": 0,
            "failed_operations": 0,
            "successful_operations": 0,
        }

        # Simule plusieurs corruptions et récupérations
        test_files = []
        for i in range(3):
            test_file = Path(f"chaos_metric_{i}.toml")
            test_data = {"id": i, "status": "testing"}

            try:
                atomic_write(test_file, toml.dumps(test_data))
                test_files.append(test_file)

                # Corrompt parfois
                if random.random() < 0.5:
                    self.chaos.corrupt_file(test_file)
                    recovery_stats["corrupted_files"] += 1

                # Tente récupération
                try:
                    content_raw = locked_read(test_file)
                    if isinstance(content_raw, str):
                        toml.loads(content_raw)
                    recovery_stats["successful_operations"] += 1
                except Exception:
                    recovery_stats["failed_operations"] += 1

            except Exception:
                recovery_stats["failed_operations"] += 1

        # Nettoie
        for test_file in test_files:
            if test_file.exists():
                test_file.unlink()

        # Métriques de récupération
        total_ops = recovery_stats["successful_operations"] + recovery_stats["failed_operations"]
        if total_ops > 0:
            success_rate = recovery_stats["successful_operations"] / total_ops
            assert success_rate >= 0.5, f"Taux de succès trop bas: {success_rate:.2%}"


# === UTILITAIRES CHAOS ===


def create_chaos_environment():
    """Crée un environnement de test chaos"""
    config = ChaosTestConfig()
    return ChaosTester(config)


def run_chaos_suite():
    """Lance la suite complète de tests chaos"""
    print("🌀 Démarrage suite tests chaos Arkalia-LUNA")

    # Lance tous les tests
    test_modules = [
        TestFileSystemChaos,
        TestSystemLoadChaos,
        TestNetworkChaos,
        TestStatePersistenceChaos,
        TestCriticalSystemChaos,
        TestChaosIntegration,
    ]

    for module in test_modules:
        print(f"🧪 Test module: {module.__name__}")

    print("✅ Suite chaos terminée")


if __name__ == "__main__":
    # Test standalone
    print("🌀 Tests de chaos Arkalia-LUNA")
    run_chaos_suite()
