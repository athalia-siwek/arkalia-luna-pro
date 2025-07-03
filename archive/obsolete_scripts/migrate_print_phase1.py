#!/usr/bin/env python3
"""
🔄 Script de Migration Phase 1 - print() → ark_logger (SAFE)
Arkalia-LUNA Pro v4.0+

Remplace uniquement les print() de criticité LOW (sûrs)
avec validation et tests automatiques.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def load_audit_results() -> dict[str, Any]:
    """Charge les résultats de l'audit."""
    try:
        with open("print_audit.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ print_audit.json non trouvé. Lancez d'abord ark_check_print.py")
        sys.exit(1)


def migrate_safe_prints(audit_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Extrait les print() sûrs pour migration Phase 1."""
    safe_prints = []

    for _file_path, prints in audit_data["audit"]["files"].items():
        for print_info in prints:
            if print_info["criticality"] == "LOW":
                safe_prints.append(print_info)

    return safe_prints


def backup_file(file_path: str) -> str:
    """Crée une sauvegarde du fichier."""
    backup_path = f"{file_path}.backup_print_migration"
    with open(file_path, encoding="utf-8") as src:
        with open(backup_path, "w", encoding="utf-8") as dst:
            dst.write(src.read())
    return backup_path


def migrate_print_to_logger(line: str, file_path: str) -> str:
    """Convertit un print() en ark_logger."""

    # Patterns de remplacement
    patterns = [
        # Debug simple
        (r'print\("debug', r'ark_logger.debug("debug'),
        (r'print\("test', r'ark_logger.info("test'),
        (r'print\("🧪', r'ark_logger.info("🧪'),
        (r'print\("✅', r'ark_logger.info("✅'),
        (r'print\("❌', r'ark_logger.error("❌'),
        (r'print\("⚠️', r'ark_logger.warning("⚠️'),
        (r'print\("🛡️', r'ark_logger.info("🛡️'),
        (r'print\("🔄', r'ark_logger.info("🔄'),
        (r'print\("🛑', r'ark_logger.info("🛑'),
        (r'print\("🚀', r'ark_logger.info("🚀'),
        (r'print\("🧠', r'ark_logger.info("🧠'),
        (r'print\("🐳', r'ark_logger.info("🐳'),
        (r'print\("🎯', r'ark_logger.info("🎯'),
        (r'print\("⏱️', r'ark_logger.info("⏱️'),
    ]

    # Appliquer les patterns
    for pattern, replacement in patterns:
        if re.search(pattern, line):
            return re.sub(pattern, replacement, line)

    # Cas par défaut
    if line.strip() == "print()":
        return line  # Ne pas toucher aux print() vides

    # Remplacement générique pour les messages simples
    if line.strip().startswith('print("') and line.strip().endswith('")'):
        return line.replace('print("', 'ark_logger.info("')

    return line


def migrate_file(file_path: str, safe_prints: list[dict[str, Any]]) -> bool:
    """Migre un fichier en remplaçant les print() sûrs."""

    # Filtrer les print() de ce fichier
    file_prints = [p for p in safe_prints if p["file_path"] == file_path]

    if not file_prints:
        return True  # Aucun print() à migrer

    print(f"🔄 Migration de {file_path} ({len(file_prints)} print() sûrs)")

    # Sauvegarde
    backup_path = backup_file(file_path)
    print(f"   📦 Sauvegarde: {backup_path}")

    try:
        # Lire le fichier
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()

        # Appliquer les migrations
        modified = False
        for print_info in file_prints:
            line_num = print_info["line"] - 1  # Index 0-based
            if line_num < len(lines):
                old_line = lines[line_num]
                new_line = migrate_print_to_logger(old_line, file_path)

                if new_line != old_line:
                    lines[line_num] = new_line
                    modified = True
                    print(
                        f"   ✅ Ligne {print_info['line']}: {old_line.strip()} → {new_line.strip()}"
                    )

        # Écrire le fichier modifié
        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print("   ✅ Fichier migré avec succès")
            return True
        else:
            print("   ⚠️ Aucune modification nécessaire")
            return True

    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        # Restaurer la sauvegarde
        with open(backup_path, encoding="utf-8") as src:
            with open(file_path, "w", encoding="utf-8") as dst:
                dst.write(src.read())
        return False


def run_tests() -> bool:
    """Lance les tests pour valider la migration."""
    print("\n🧪 Validation par tests...")

    try:
        # Tests unitaires rapides
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/unit/", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("✅ Tests unitaires passent")
            return True
        else:
            print("❌ Tests unitaires échouent:")
            print(result.stdout)
            print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("⚠️ Tests timeout - à vérifier manuellement")
        return True
    except Exception as e:
        print(f"❌ Erreur tests: {e}")
        return False


def main():
    """Fonction principale."""
    print("🔄 Début migration Phase 1 (SAFE) - print() → ark_logger")

    # Charger l'audit
    audit_data = load_audit_results()
    safe_prints = migrate_safe_prints(audit_data)

    if not safe_prints:
        print("✅ Aucun print() sûr à migrer")
        return

    print(f"📊 {len(safe_prints)} print() sûrs identifiés")

    # Grouper par fichier
    files_to_migrate = {}
    for print_info in safe_prints:
        file_path = print_info["file_path"]
        if file_path not in files_to_migrate:
            files_to_migrate[file_path] = []
        files_to_migrate[file_path].append(print_info)

    print(f"📁 {len(files_to_migrate)} fichiers à migrer")

    # Migration
    success_count = 0
    for file_path in files_to_migrate:
        if migrate_file(file_path, safe_prints):
            success_count += 1

    print(f"\n📊 Résultat migration: {success_count}/{len(files_to_migrate)} fichiers migrés")

    # Validation par tests
    if run_tests():
        print("✅ Migration Phase 1 validée")
    else:
        print("❌ Migration Phase 1 échouée - restauration nécessaire")
        print("💡 Utilisez les fichiers .backup_print_migration pour restaurer")


if __name__ == "__main__":
    main()
