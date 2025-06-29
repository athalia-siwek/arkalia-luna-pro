#!/usr/bin/env python3
"""
🔧 Script de correction automatique des erreurs de typing deprecated
Corrige UP035 (typing.Dict -> dict, typing.List -> list, etc.)
"""

import os
import re
import subprocess
from pathlib import Path
from typing import Any

# Patterns de remplacement
REPLACEMENTS = {
    r"from typing import.*Dict.*": "from typing import Any, Optional",
    r"from typing import.*List.*": "from typing import Any, Optional",
    r"from typing import.*Tuple.*": "from typing import Any, Optional",
    r"from typing import.*Set.*": "from typing import Any, Optional",
    r"from typing import.*Union.*": "from typing import Any, Optional",
    r"Dict\[": "dict[",
    r"List\[": "list[",
    r"Tuple\[": "tuple[",
    r"Set\[": "set[",
    r"Union\[": "Any",
}


def fix_typing_errors(file_path: Path) -> bool:
    """Corrige les erreurs de typing dans un fichier"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Appliquer les remplacements
        for pattern, replacement in REPLACEMENTS.items():
            content = re.sub(pattern, replacement, content)

        # Nettoyer les imports vides
        content = re.sub(r"from typing import\s*$", "", content, flags=re.MULTILINE)
        content = re.sub(r"from typing import\s*\n", "", content, flags=re.MULTILINE)

        # Si le contenu a changé, sauvegarder
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True

        return False
    except Exception as e:
        print(f"❌ Erreur lors du traitement de {file_path}: {e}")
        return False


def main():
    """Fonction principale"""
    print("🔧 Correction automatique des erreurs de typing deprecated...")

    # Trouver tous les fichiers Python
    python_files = []
    for root, dirs, files in os.walk("."):
        # Ignorer les dossiers à exclure
        dirs[:] = [
            d
            for d in dirs
            if d not in [".git", "__pycache__", "venv", "node_modules", ".pytest_cache"]
        ]

        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)

    fixed_count = 0
    total_files = len(python_files)

    for file_path in python_files:
        if fix_typing_errors(file_path):
            fixed_count += 1
            print(f"✅ Corrigé: {file_path}")

    print(f"\n🎯 Résumé: {fixed_count}/{total_files} fichiers corrigés")

    # Appliquer Black et isort
    print("\n🎨 Application du formatage...")
    subprocess.run(["black", "."], check=False)
    subprocess.run(["isort", "."], check=False)

    print("✅ Correction terminée!")


if __name__ == "__main__":
    main()
