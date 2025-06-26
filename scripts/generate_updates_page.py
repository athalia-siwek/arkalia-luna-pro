# scripts/generate_updates_page.py

import subprocess
from pathlib import Path

# Supprimer les fichiers ._* (pollution macOS)
for file in Path("docs/releases").glob("._*"):
    file.unlink()


def run(**kwargs):
    output_file = Path("docs/releases/dernieres_updates.md")
    command = [
        "git",
        "log",
        "--pretty=format:%h - %s (%ad)",
        "--abbrev-commit",
        "--date=short",
        "-n",
        "10",
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open("w", encoding="utf-8") as f:
            f.write("# 🕒 Dernières Updates\n\n")
            f.write(result.stdout.strip() + "\n")

        print(f"✅ Fichier généré : {output_file}")

        # Supprimer les fichiers macOS invisibles s'ils existent
        for file in output_file.parent.glob("._*"):
            file.unlink()
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution de git log : {e.stderr}")
