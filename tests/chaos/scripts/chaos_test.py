#!/usr/bin/env python3
"""
🧪 [CHAOS TEST] - Roadmap S2-P2 Arkalia-LUNA
Tests automatiques de résilience avec injection de chaos

Scénarios de chaos:
- Corruption fichiers de configuration
- Suppression fichiers critiques
- Surcharge CPU/mémoire
- Injection d'erreurs réseau
- Corruption état ZeroIA/ReflexIA
"""

import asyncio
import json
import logging
import os
import random
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any

import toml

# Ajout dynamique du chemin du projet pour garantir l'import correct
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from core.ark_logger import ark_logger


class ChaosInjector:
    """Injecteur de chaos pour tests de résilience Arkalia-LUNA"""

    def __init__(self, target_directory: str = ".") -> None:
        self.target_dir = Path(target_directory)
        self.backup_dir = Path("chaos_backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.test_results = []
        self.is_dry_run = False

    def set_dry_run(self, enabled: bool):
        """Active/désactive le mode simulation"""
        self.is_dry_run = enabled

    def _backup_file(self, file_path: Path) -> Path:
        """Sauvegarde un fichier avant modification"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}.backup"
        backup_path = self.backup_dir / backup_name

        if not self.is_dry_run and file_path.exists():
            shutil.copy2(file_path, backup_path)
            ark_logger.info(f"📦 [CHAOS] Backup: {file_path} → {backup_path}", extra={"module": "scripts"})

        return backup_path

    def _restore_file(self, backup_path: Path, original_path: Path):
        """Restaure un fichier depuis sa sauvegarde"""
        if backup_path.exists() and not self.is_dry_run:
            shutil.copy2(backup_path, original_path)
            ark_logger.info(f"🔄 [CHAOS] Restored: {backup_path} → {original_path}", extra={"module": "scripts"})

    def chaos_corrupt_config(self) -> dict:
        """💥 Corrompt les fichiers de configuration"""
        ark_logger.info("💥 [CHAOS] Corruption fichiers configuration...", extra={"module": "scripts"})

        config_files = [
            "config/settings.toml",
            "config/monitoring_config.toml",
            "modules/zeroia/state/zeroia_state.toml",
            "modules/reflexia/state/reflexia_state.toml",
        ]

        results = {"name": "config_corruption", "corrupted_files": [], "success": True}

        for config_file in config_files:
            file_path = self.target_dir / config_file
            if not file_path.exists():
                continue

            self._backup_file(file_path)  # Backup file before corruption
            results["corrupted_files"].append(str(file_path))

            if not self.is_dry_run:
                try:
                    # Corruption du fichier (ajout caractères invalides)
                    with open(file_path) as f:
                        content = f.read()

                    corrupted_content = (
                        content[: len(content) // 2]
                        + "§§§CHAOS_CORRUPTION§§§"
                        + content[len(content) // 2 :]
                    )

                    with open(file_path, "w") as f:
                        f.write(corrupted_content)

                    ark_logger.info(f"💀 [CHAOS] Corrompu: {file_path}", extra={"module": "scripts"})

                except Exception as e:
                    ark_logger.info(f"❌ [CHAOS] Erreur corruption {file_path}: {e}", extra={"module": "scripts"})
                    results["success"] = False

        return results

    def chaos_delete_critical_files(self) -> dict:
        """🗑️ Supprime des fichiers critiques temporairement"""
        ark_logger.info("🗑️ [CHAOS] Suppression fichiers critiques...", extra={"module": "scripts"})

        critical_files = [
            "modules/zeroia/core.py",
            "modules/reflexia/core.py",
            "modules/assistantia/core.py",
            "version.toml",
        ]

        results = {"name": "file_deletion", "deleted_files": [], "success": True}

        for critical_file in critical_files:
            file_path = self.target_dir / critical_file
            if not file_path.exists():
                continue

            self._backup_file(file_path)  # Backup file before deletion
            results["deleted_files"].append(str(file_path))

            if not self.is_dry_run:
                try:
                    file_path.unlink()
                    ark_logger.info(f"💥 [CHAOS] Supprimé: {file_path}", extra={"module": "scripts"})
                except Exception as e:
                    ark_logger.info(f"❌ [CHAOS] Erreur suppression {file_path}: {e}", extra={"module": "scripts"})
                    results["success"] = False

        return results

    def chaos_memory_stress(self, duration_seconds: int = 30) -> dict:
        """🧠 Surcharge mémoire pour tester la résilience"""
        ark_logger.info(f"🧠 [CHAOS] Surcharge mémoire pendant {duration_seconds}s...", extra={"module": "scripts"})

        results = {
            "name": "memory_stress",
            "duration": duration_seconds,
            "success": True,
        }

        if self.is_dry_run:
            ark_logger.info("🔍 [CHAOS] Mode dry-run: simulation surcharge mémoire", extra={"module": "scripts"})
            return results

        try:
            # Allocation mémoire progressive
            memory_chunks = []
            chunk_size = 1024 * 1024 * 50  # 50MB par chunk
            max_chunks = 20  # Max 1GB

            for i in range(max_chunks):
                try:
                    chunk = bytearray(chunk_size)
                    memory_chunks.append(chunk)
                    ark_logger.info(f"📈 [CHAOS] Alloué: {(i+1, extra={"module": "scripts"}) * 50}MB")
                    time.sleep(duration_seconds / max_chunks)
                except MemoryError:
                    ark_logger.info("💥 [CHAOS] Limite mémoire atteinte", extra={"module": "scripts"})
                    break

            # Libération progressive
            del memory_chunks
            ark_logger.info("🔄 [CHAOS] Mémoire libérée", extra={"module": "scripts"})

        except Exception as e:
            ark_logger.info(f"❌ [CHAOS] Erreur stress mémoire: {e}", extra={"module": "scripts"})
            results["success"] = False

        return results

    def chaos_network_simulation(self) -> dict:
        """🌐 Simule des erreurs réseau"""
        ark_logger.info("🌐 [CHAOS] Simulation erreurs réseau...", extra={"module": "scripts"})

        results = {"name": "network_simulation", "tests": [], "success": True}

        # Test de connectivité avec timeout agressif
        network_tests = [
            ("localhost", 8000, "API Arkalia"),
            ("localhost", 9090, "Prometheus"),
            ("localhost", 3000, "Grafana"),
            ("127.0.0.1", 11434, "Ollama"),
        ]

        for host, port, service in network_tests:
            test_result = {"service": service, "host": host, "port": port}

            try:
                if not self.is_dry_run:
                    import socket

                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)  # Timeout agressif
                    result = sock.connect_ex((host, port))
                    sock.close()

                    test_result["accessible"] = result == 0
                    test_result["chaos_injected"] = False
                else:
                    test_result["accessible"] = random.choice([True, False])  # nosec B311
                    test_result["chaos_injected"] = True

                ark_logger.info(f"🔗 [CHAOS] {service}: {'✅' if test_result['accessible'] else '❌'}", extra={"module": "scripts"})

            except Exception as e:
                test_result["accessible"] = False
                test_result["error"] = str(e)
                ark_logger.info(f"💥 [CHAOS] Erreur test {service}: {e}", extra={"module": "scripts"})

            results["tests"].append(test_result)

        return results

    def chaos_zeroia_state_corruption(self) -> dict:
        """🤖 Corrompt l'état de ZeroIA"""
        ark_logger.info("🤖 [CHAOS] Corruption état ZeroIA...", extra={"module": "scripts"})

        results = {"name": "zeroia_corruption", "files_corrupted": [], "success": True}

        zeroia_files = [
            "modules/zeroia/state/zeroia_state.toml",
            "modules/zeroia/state/zeroia_decision_log.toml",
            "state/global_context.toml",
        ]

        for zeroia_file in zeroia_files:
            file_path = self.target_dir / zeroia_file
            if not file_path.exists():
                continue

            self._backup_file(file_path)  # Backup file before corruption
            results["files_corrupted"].append(str(file_path))

            if not self.is_dry_run:
                try:
                    # Injection de chaos spécifique ZeroIA
                    with open(file_path) as f:
                        content = f.read()

                    # Corruption ciblée
                    chaos_injections = [
                        'cpu = "CHAOS_ERROR"',
                        "ram = -999.9",
                        'decision = "malformed_decision_###"',
                        'confidence = "NOT_A_NUMBER"',
                    ]

                    corrupted_content = content + "\n# CHAOS INJECTION\n"
                    corrupted_content += "\n".join(random.sample(chaos_injections, 2))  # nosec B311

                    with open(file_path, "w") as f:
                        f.write(corrupted_content)

                    ark_logger.info(f"💀 [CHAOS] État ZeroIA corrompu: {file_path}", extra={"module": "scripts"})

                except Exception as e:
                    ark_logger.info(f"❌ [CHAOS] Erreur corruption ZeroIA {file_path}: {e}", extra={"module": "scripts"})
                    results["success"] = False

        return results

    def run_resilience_test(self, test_duration: int = 60) -> dict:
        """🧪 Exécute un test de résilience complet"""
        ark_logger.info(f"🧪 [CHAOS] Démarrage test résilience ({test_duration}s, extra={"module": "scripts"})...")

        start_time = time.time()
        test_report = {
            "start_time": datetime.now().isoformat(),
            "test_duration": test_duration,
            "chaos_scenarios": [],
            "recovery_tests": [],
            "overall_success": True,
        }

        # Séquence de tests de chaos
        chaos_scenarios = [
            ("config_corruption", self.chaos_corrupt_config),
            ("memory_stress", lambda: self.chaos_memory_stress(15)),
            ("network_simulation", self.chaos_network_simulation),
            ("zeroia_corruption", self.chaos_zeroia_state_corruption),
            ("file_deletion", self.chaos_delete_critical_files),
        ]

        try:
            for scenario_name, chaos_func in chaos_scenarios:
                ark_logger.info(f"\n🎯 [CHAOS] Scénario: {scenario_name}", extra={"module": "scripts"})

                scenario_start = time.time()
                scenario_result = chaos_func()
                scenario_duration = time.time() - scenario_start

                scenario_result["duration"] = scenario_duration
                scenario_result["timestamp"] = datetime.now().isoformat()
                test_report["chaos_scenarios"].append(scenario_result)

                if not scenario_result["success"]:
                    test_report["overall_success"] = False

                # Attente entre scénarios
                time.sleep(random.uniform(2, 5))  # nosec B311

                # Test de récupération
                recovery_result = self._test_system_recovery()
                test_report["recovery_tests"].append(recovery_result)

        except KeyboardInterrupt:
            ark_logger.info("\n🛑 [CHAOS] Test interrompu par utilisateur", extra={"module": "scripts"})
            test_report["interrupted"] = True

        except Exception as e:
            raise RuntimeError(f"Erreur chaos test: {e}") from e

        finally:
            # Restauration des fichiers
            self._restore_all_backups()

        # Rapport final
        test_report["end_time"] = datetime.now().isoformat()
        test_report["actual_duration"] = time.time() - start_time

        self._generate_chaos_report(test_report)

        return test_report

    def _test_system_recovery(self) -> dict:
        """🔄 Teste la capacité de récupération du système"""
        recovery_result = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "success": True,
        }

        # Test imports critiques
        import_tests = [
            "modules.zeroia.core",
            "modules.reflexia.core",
            "modules.assistantia.core",
        ]

        for module_name in import_tests:
            try:
                if not self.is_dry_run:
                    __import__(module_name)
                    test_result = {"module": module_name, "importable": True}
                else:
                    test_result = {
                        "module": module_name,
                        "importable": random.choice([True, False]),  # nosec B311
                    }

                status = "✅" if test_result["importable"] else "❌"
                ark_logger.info(f"🔍 [RECOVERY] Module {module_name}: {status}", extra={"module": "scripts"})

            except Exception as e:
                test_result = {
                    "module": module_name,
                    "importable": False,
                    "error": str(e),
                }
                recovery_result["success"] = False
                ark_logger.info(f"💥 [RECOVERY] Échec import {module_name}: {e}", extra={"module": "scripts"})

            recovery_result["tests"].append(test_result)

        return recovery_result

    def _restore_all_backups(self):
        """🔄 Restaure tous les fichiers depuis les backups"""
        ark_logger.info("🔄 [CHAOS] Restauration des backups...", extra={"module": "scripts"})

        for backup_file in self.backup_dir.glob("*.backup"):
            try:
                # Extraire le nom original
                parts = backup_file.stem.split("_")
                if len(parts) >= 2:
                    original_name = "_".join(parts[:-2]) + backup_file.suffixes[-2]

                    # Rechercher le fichier original
                    for potential_path in self.target_dir.rglob(original_name):
                        if potential_path.is_file():
                            self._restore_file(backup_file, potential_path)
                            break

            except Exception as e:
                ark_logger.info(f"❌ [CHAOS] Erreur restauration {backup_file}: {e}", extra={"module": "scripts"})

    def _generate_chaos_report(self, test_report: dict):
        """📊 Génère le rapport de test de chaos"""
        report_dir = Path("logs/chaos_reports")
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"chaos_test_report_{timestamp}.json"

        with open(report_file, "w") as f:
            json.dump(test_report, f, indent=2)

        ark_logger.info("\n📊 [CHAOS] RAPPORT DE TEST:", extra={"module": "scripts"})
        ark_logger.info(f"   ⏱️ Durée: {test_report.get('actual_duration', 0, extra={"module": "scripts"}):.2f}s")
        ark_logger.info(f"   🎯 Scénarios: {len(test_report['chaos_scenarios'], extra={"module": "scripts"})}")
        ark_logger.info(f"   🔄 Tests récupération: {len(test_report['recovery_tests'], extra={"module": "scripts"})}")
        ark_logger.info(f"   ✅ Succès global: {'OUI' if test_report['overall_success'] else 'NON'}", extra={"module": "scripts"})
        ark_logger.info(f"   📄 Rapport: {report_file}", extra={"module": "scripts"})

        # Statistiques détaillées
        successful_scenarios = sum(
            1 for s in test_report["chaos_scenarios"] if s.get("success", False)
        )
        successful_recoveries = sum(
            1 for r in test_report["recovery_tests"] if r.get("success", False)
        )

        ark_logger.info("\n📈 [CHAOS] STATISTIQUES:", extra={"module": "scripts"})
        scenarios_count = len(test_report["chaos_scenarios"])
        recoveries_count = len(test_report["recovery_tests"])
        ark_logger.info(f"   💥 Scénarios réussis: {successful_scenarios}/{scenarios_count}", extra={"module": "scripts"})
        ark_logger.info(f"   🔄 Récupérations réussies: {successful_recoveries}/{recoveries_count}", extra={"module": "scripts"})

        total_tests = scenarios_count + recoveries_count
        total_successes = successful_scenarios + successful_recoveries
        resilience_score = total_successes / total_tests * 100
        ark_logger.info(f"   🛡️ Score de résilience: {resilience_score:.1f}%", extra={"module": "scripts"})


def main():
    """Point d'entrée principal"""
    import argparse

    parser = argparse.ArgumentParser(description="🧪 Arkalia-LUNA Chaos Testing")
    parser.add_argument("--dry-run", action="store_true", help="Mode simulation")
    parser.add_argument("--duration", type=int, default=60, help="Durée du test (secondes)")
    parser.add_argument(
        "--scenario",
        choices=["config", "memory", "network", "zeroia", "files"],
        help="Scénario spécifique",
    )

    args = parser.parse_args()

    chaos = ChaosInjector()
    chaos.set_dry_run(args.dry_run)

    try:
        if args.scenario:
            # Test d'un scénario spécifique
            scenario_map = {
                "config": chaos.chaos_corrupt_config,
                "memory": lambda: chaos.chaos_memory_stress(30),
                "network": chaos.chaos_network_simulation,
                "zeroia": chaos.chaos_zeroia_state_corruption,
                "files": chaos.chaos_delete_critical_files,
            }

            if args.scenario in scenario_map:
                result = scenario_map[args.scenario]()
                status = "Succès" if result["success"] else "Échec"
                ark_logger.info(f"\n✅ [CHAOS] Scénario {args.scenario} terminé: {status}", extra={"module": "scripts"})

        else:
            # Test complet de résilience
            report = chaos.run_resilience_test(args.duration)
            exit_code = 0 if report["overall_success"] else 1
            exit(exit_code)

    except KeyboardInterrupt:
        ark_logger.info("\n🛑 [CHAOS] Arrêt demandé par l'utilisateur", extra={"module": "scripts"})
        exit(130)
    except Exception as e:
        ark_logger.info(f"💥 [CHAOS] Erreur fatale: {e}", extra={"module": "scripts"})
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
