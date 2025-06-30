#!/usr/bin/env python3
"""
Script de validation CI pour Arkalia-LUNA
Vérifie les points critiques sans échouer sur les erreurs mineures
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Exécute une commande et retourne le succès"""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCÈS")
            return True
        else:
            print(f"❌ {description} - ÉCHEC")
            if result.stderr:
                print(f"Erreur: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {description} - ERREUR: {e}")
        return False


def check_imports() -> bool:
    """Vérifie que les imports principaux fonctionnent"""
    print("🔍 Vérification des imports principaux...")

    test_imports = [
        "import modules.zeroia.core",
        "import modules.reflexia.core",
        "import modules.assistantia.core",
        "import modules.helloria.core",
        "import modules.security.core",
    ]

    for import_stmt in test_imports:
        try:
            exec(import_stmt)
            print(f"✅ {import_stmt}")
        except Exception as e:
            print(f"❌ {import_stmt} - {e}")
            return False

    return True


def check_config_files() -> bool:
    """Vérifie que les fichiers de configuration existent"""
    print("🔍 Vérification des fichiers de configuration...")

    required_files = [
        "pyproject.toml",
        "requirements.txt",
        ".pre-commit-config.yaml",
        "mkdocs.yml",
        ".github/workflows/ci.yml",
        ".github/workflows/docs.yml",
    ]

    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MANQUANT")
            return False

    return True


def check_test_structure() -> bool:
    """Vérifie la structure des tests"""
    print("🔍 Vérification de la structure des tests...")

    test_dirs = [
        "tests/unit",
        "tests/integration",
        "tests/security",
        "tests/performance",
        "tests/chaos",
    ]

    for test_dir in test_dirs:
        if Path(test_dir).exists():
            test_files = list(Path(test_dir).rglob("test_*.py"))
            if test_files:
                print(f"✅ {test_dir} ({len(test_files)} fichiers)")
            else:
                print(f"⚠️ {test_dir} - Aucun test trouvé")
        else:
            print(f"❌ {test_dir} - MANQUANT")
            return False

    return True


def main() -> int:
    """Point d'entrée principal"""
    print("🚀 Validation CI Arkalia-LUNA")
    print("=" * 50)

    checks = [
        ("Configuration", check_config_files),
        ("Structure des tests", check_test_structure),
        ("Imports principaux", check_imports),
        ("Formatage", lambda: run_command(["black", "--check", "."], "Vérification formatage")),
        ("Linting", lambda: run_command(["ruff", "check", "."], "Vérification linting")),
        (
            "Tests unitaires",
            lambda: run_command(["pytest", "tests/unit/", "-v", "--tb=short"], "Tests unitaires"),
        ),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n📋 {name}")
        print("-" * 30)
        success = check_func()
        results.append((name, success))

    # Rapport final
    print("\n" + "=" * 50)
    print("📊 RAPPORT FINAL")
    print("=" * 50)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {name}")

    print(f"\n🎯 Résultat: {passed}/{total} vérifications réussies")

    if passed == total:
        print("🎉 Toutes les vérifications CI sont passées !")
        return 0
    else:
        print("⚠️ Certaines vérifications ont échoué")
        return 1


if __name__ == "__main__":
    sys.exit(main())
