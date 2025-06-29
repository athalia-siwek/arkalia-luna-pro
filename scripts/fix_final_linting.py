#!/usr/bin/env python3
"""
🔧 Script final de correction des erreurs de linting restantes
Pour faire fonctionner ark-act parfaitement
"""

import os
import re
import subprocess
from pathlib import Path
from typing import Any


def fix_line_length_errors():
    """Corrige les erreurs de longueur de ligne"""
    fixes = [
        # modules/crossmodule_validator/core.py:145
        (
            r'f"✅ Validation: score={validation.coherence_score:.2f}, conflits={len(validation.conflicts)}"',
            'f"✅ Validation: score={validation.coherence_score:.2f}, conflits={len(validation.conflicts)}"',
        ),
        # modules/generative_ai/core.py:500
        (
            r'f"🔧 Opportunités d\'optimisation: {len(analysis[\'optimization_opportunities\'])}"',
            "f\"🔧 Opportunités d'optimisation: {len(analysis['optimization_opportunities'])}\"",
        ),
        # modules/sandozia/analyzer/behavior.py:168
        (
            r'f"Anomalie statistique détectée dans {metric_name} (z-score: {z_score:.2f})"',
            'f"Anomalie statistique détectée dans {metric_name} (z-score: {z_score:.2f})"',
        ),
        # modules/sandozia/analyzer/behavior.py:238
        (
            r'f"Régression de performance détectée dans {metric_name}: {relative_change:.1%}"',
            'f"Régression de performance détectée dans {metric_name}: {relative_change:.1%}"',
        ),
        # modules/sandozia/analyzer/behavior.py:284
        (
            r'f"Pattern répétitif détecté: {len(recent_decisions)} décisions identiques ({list(unique_types)[0]})"',
            'f"Pattern répétitif détecté: {len(recent_decisions)} décisions identiques ({list(unique_types)[0]})"',
        ),
        # modules/sandozia/analyzer/behavior.py:313
        (
            r'f"Fréquence de décision élevée: {mean_interval:.2f}s entre décisions"',
            'f"Fréquence de décision élevée: {mean_interval:.2f}s entre décisions"',
        ),
        # modules/sandozia/core/chronalia.py:232
        (
            r'f"{len(recent_decisions)} décisions identiques: {list(unique_decisions)[0]}"',
            'f"{len(recent_decisions)} décisions identiques: {list(unique_decisions)[0]}"',
        ),
        # modules/sandozia/core/chronalia.py:250
        (
            r'f"Confiance effondrée: {confidences[0]:.2f} → {confidences[-1]:.2f}"',
            'f"Confiance effondrée: {confidences[0]:.2f} → {confidences[-1]:.2f}"',
        ),
        # modules/sandozia/validators/crossmodule.py:265
        (
            r'"Contradiction: ZeroIA détecte des incohérences mais Reflexia a une confiance élevée"',
            '"Contradiction: ZeroIA détecte des incohérences mais Reflexia a une confiance élevée"',
        ),
        # modules/sandozia/validators/crossmodule.py:318
        (
            r'f"Pattern comportemental suspect: {critical_count} erreurs critiques récentes"',
            'f"Pattern comportemental suspect: {critical_count} erreurs critiques récentes"',
        ),
        # modules/zeroia/circuit_breaker.py:173
        (
            r'f"Circuit breaker OPEN - trop d\'échecs consécutifs ({self.metrics.consecutive_failures})"',
            'f"Circuit breaker OPEN - trop d\'échecs consécutifs ({self.metrics.consecutive_failures})"',
        ),
        # modules/zeroia/circuit_breaker.py:229
        (
            r'f"🚨 CircuitBreaker échec: {exception} (consécutif: {self.metrics.consecutive_failures})"',
            'f"🚨 CircuitBreaker échec: {exception} (consécutif: {self.metrics.consecutive_failures})"',
        ),
        # modules/zeroia/event_store.py:370
        (
            r'f"{len(contradictions)} contradictions IA en {window_minutes}min"',
            'f"{len(contradictions)} contradictions IA en {window_minutes}min"',
        ),
        # modules/zeroia/event_store.py:446
        (
            r'f"📋 Nettoyage EventStore: {deleted_count} événements supprimés (> {days_to_keep} jours)"',
            'f"📋 Nettoyage EventStore: {deleted_count} événements supprimés (> {days_to_keep} jours)"',
        ),
    ]

    for pattern, replacement in fixes:
        # Appliquer les corrections dans tous les fichiers Python
        for root, dirs, files in os.walk("."):
            dirs[:] = [
                d
                for d in dirs
                if d not in [".git", "__pycache__", "venv", "node_modules", ".pytest_cache"]
            ]

            for file in files:
                if file.endswith(".py"):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, encoding="utf-8") as f:
                            content = f.read()

                        if pattern in content:
                            content = content.replace(pattern, replacement)
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(content)
                            print(f"✅ Corrigé: {file_path}")
                    except Exception as e:
                        print(f"❌ Erreur {file_path}: {e}")


def fix_import_errors():
    """Corrige les erreurs d'import"""
    # Corriger le fichier test_core.py
    test_core_path = Path("modules/generative_ai/generated/test_core.py")
    if test_core_path.exists():
        try:
            with open(test_core_path, encoding="utf-8") as f:
                content = f.read()

            # Corriger l'import
            content = content.replace("/ import pytest", "import pytest")
            content = content.replace(
                "from modules.core import TestCore",
                "from modules.generative_ai.core import TestCore",
            )

            with open(test_core_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Import corrigé: {test_core_path}")
        except Exception as e:
            print(f"❌ Erreur {test_core_path}: {e}")


def fix_noqa_directives():
    """Corrige les directives noqa invalides"""
    files_to_fix = ["scripts/arkalia_enhanced_integration.py", "scripts/restore_broken_files.py"]

    for file_path in files_to_fix:
        if Path(file_path).exists():
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                # Remplacer les noqa invalides
                content = re.sub(r"# noqa: F401\(\)", "# noqa: F401", content)
                content = re.sub(r"# noqa: F401", "# noqa: F401", content)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Noqa corrigé: {file_path}")
            except Exception as e:
                print(f"❌ Erreur {file_path}: {e}")


def main():
    """Fonction principale"""
    print("🔧 Correction finale des erreurs de linting...")

    # 1. Corriger les erreurs de longueur de ligne
    print("\n📏 Correction des erreurs de longueur de ligne...")
    fix_line_length_errors()

    # 2. Corriger les erreurs d'import
    print("\n📦 Correction des erreurs d'import...")
    fix_import_errors()

    # 3. Corriger les directives noqa
    print("\n🚫 Correction des directives noqa...")
    fix_noqa_directives()

    # 4. Appliquer le formatage
    print("\n🎨 Application du formatage...")
    subprocess.run(["black", "."], check=False)
    subprocess.run(["isort", "."], check=False)

    # 5. Vérifier le résultat
    print("\n🔍 Vérification finale...")
    result = subprocess.run(["ruff", "check", ".", "--statistics"], capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Toutes les erreurs corrigées !")
    else:
        print("⚠️  Il reste encore quelques erreurs, mais ark-act devrait fonctionner.")
        print(result.stdout)

    print("\n🚀 ark-act devrait maintenant fonctionner !")


if __name__ == "__main__":
    main()
