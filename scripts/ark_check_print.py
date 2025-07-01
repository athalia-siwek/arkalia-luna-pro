#!/usr/bin/env python3
"""
🔍 Script d'Audit Intelligent - Migration print() → ark_logger
Arkalia-LUNA Pro v4.0+

Analyse tous les print() dans modules/ et génère un rapport JSON
pour migration progressive et sécurisée.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def analyze_print_statement(line: str, line_num: int, file_path: str) -> dict[str, Any]:
    """Analyse une ligne contenant print() et détermine sa criticité."""

    # Critères de criticité
    critical_patterns = [
        r'print\(f"',  # f-strings complexes
        r"print\(.*json\.dumps",  # JSON dumps (à conserver)
        r"print\(.*health_check",  # Health checks
        r"print\(.*__version__",  # Version info
        r"print\(.*main_loop",  # Boucles principales
        r"print\(.*started",  # Messages de démarrage
        r"print\(.*finished",  # Messages de fin
    ]

    safe_patterns = [
        r'print\("debug',  # Debug simple
        r'print\("test',  # Tests
        r'print\("🧪',  # Emojis de test
        r'print\("✅',  # Emojis de succès
        r'print\("❌',  # Emojis d'erreur
    ]

    # Déterminer la criticité
    criticality = "MEDIUM"
    reason = "Analyse manuelle requise"

    for pattern in critical_patterns:
        if re.search(pattern, line, re.IGNORECASE):
            criticality = "HIGH"
            reason = f"Pattern critique détecté: {pattern}"
            break

    for pattern in safe_patterns:
        if re.search(pattern, line, re.IGNORECASE):
            criticality = "LOW"
            reason = "Pattern sûr détecté"
            break

    # Cas spéciaux
    if "json.dumps" in line:
        criticality = "EXCLUDE"
        reason = "JSON dumps - à conserver pour communication inter-process"

    if "test" in file_path.lower() or "generated" in file_path.lower():
        criticality = "LOW"
        reason = "Fichier de test ou généré"

    return {
        "line": line_num,
        "code": line.strip(),
        "criticality": criticality,
        "reason": reason,
        "file_path": file_path,
    }


def audit_prints() -> dict[str, Any]:
    """Audit complet de tous les print() dans modules/."""

    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "total_prints": 0,
            "by_criticality": {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "EXCLUDE": 0},
        },
        "files": {},
    }

    modules_path = Path("modules")
    if not modules_path.exists():
        print("❌ Dossier modules/ non trouvé")
        return results

    for py_file in modules_path.rglob("*.py"):
        file_path = str(py_file)
        prints_in_file = []

        try:
            with open(py_file, encoding="utf-8") as f:
                lines = f.readlines()

            for idx, line in enumerate(lines):
                if "print(" in line:
                    analysis = analyze_print_statement(line, idx + 1, file_path)
                    prints_in_file.append(analysis)
                    results["metadata"]["total_prints"] += 1
                    results["metadata"]["by_criticality"][analysis["criticality"]] += 1

            if prints_in_file:
                results["files"][file_path] = prints_in_file
                results["metadata"]["total_files"] += 1

        except Exception as e:
            print(f"⚠️ Erreur lecture {file_path}: {e}")

    return results


def generate_migration_plan(audit_results: dict[str, Any]) -> dict[str, Any]:
    """Génère un plan de migration basé sur l'audit."""

    plan = {
        "phase_1_safe": [],  # LOW criticality
        "phase_2_medium": [],  # MEDIUM criticality
        "phase_3_high": [],  # HIGH criticality
        "exclude": [],  # EXCLUDE (json.dumps, etc.)
        "recommendations": [],
    }

    for file_path, prints in audit_results["files"].items():
        for print_info in prints:
            if print_info["criticality"] == "LOW":
                plan["phase_1_safe"].append(print_info)
            elif print_info["criticality"] == "MEDIUM":
                plan["phase_2_medium"].append(print_info)
            elif print_info["criticality"] == "HIGH":
                plan["phase_3_high"].append(print_info)
            elif print_info["criticality"] == "EXCLUDE":
                plan["exclude"].append(print_info)

    # Recommandations
    plan["recommendations"] = [
        "Phase 1: Commencer par les fichiers de test et debug simples",
        "Phase 2: Analyser manuellement chaque cas MEDIUM",
        "Phase 3: Ne pas toucher aux cas HIGH sans validation complète",
        "Exclude: Ne jamais modifier les json.dumps",
        "Toujours tester après chaque modification",
    ]

    return plan


def main():
    """Fonction principale."""
    print("🔍 Début audit print() dans modules/...")

    # Audit
    audit_results = audit_prints()

    # Plan de migration
    migration_plan = generate_migration_plan(audit_results)

    # Sauvegarder les résultats
    with open("print_audit.json", "w", encoding="utf-8") as f:
        json.dump(
            {"audit": audit_results, "migration_plan": migration_plan},
            f,
            indent=2,
            ensure_ascii=False,
        )

    # Rapport console
    print("\n✅ Audit terminé!")
    print("📊 Résultats:")
    print(f"   • Fichiers analysés: {audit_results['metadata']['total_files']}")
    print(f"   • Total print(): {audit_results['metadata']['total_prints']}")
    print("   • Par criticité:")
    for crit, count in audit_results["metadata"]["by_criticality"].items():
        print(f"     - {crit}: {count}")

    print("\n📋 Plan de migration:")
    print(f"   • Phase 1 (SAFE): {len(migration_plan['phase_1_safe'])}")
    print(f"   • Phase 2 (MEDIUM): {len(migration_plan['phase_2_medium'])}")
    print(f"   • Phase 3 (HIGH): {len(migration_plan['phase_3_high'])}")
    print(f"   • Exclude: {len(migration_plan['exclude'])}")

    print("\n📄 Rapport complet: print_audit.json")
    print("🔐 Backup: backup_print_cleanup.patch")


if __name__ == "__main__":
    main()
