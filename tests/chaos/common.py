# 🌀 tests/chaos/common.py
# Classes et utilitaires communs pour les tests de chaos

import random
import subprocess
import tempfile
import time
from pathlib import Path


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
                for i in range(min(10, len(corrupted))):
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
