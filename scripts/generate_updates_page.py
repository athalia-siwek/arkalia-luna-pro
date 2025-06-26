# scripts/generate_updates_page.py

import subprocess  # nosec
from pathlib import Path

# Supprimer les fichiers ._* (pollution macOS)
for file in Path("docs/releases").glob("._*"):
    file.unlink()


def main(**kwargs):
    print("✅ Hook exécuté : génération des updates")

    repo_path = Path.cwd()  # Assure que le chemin actuel est un dépôt Git
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
        result = subprocess.run(
            command, cwd=repo_path, capture_output=True, text=True, check=True
        )  # nosec
        output_file.parent.mkdir(parents=True, exist_ok=True)

        new_content = "# 🔄 Dernières mises à jour\n" + result.stdout.strip() + "\n"
        if (
            output_file.exists()
            and output_file.read_text(encoding="utf-8") == new_content
        ):
            print("✅ Aucun changement détecté, pas d'écriture nécessaire.")
            return

        with output_file.open("w", encoding="utf-8") as f:
            f.write(new_content)

        print(
            f"✅ Updates page générée avec {len(result.stdout.strip().splitlines())} "
            "commits récents."
        )

        # Supprimer les fichiers macOS invisibles s'ils existent
        for file in output_file.parent.glob("._*"):
            file.unlink()
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande git: {e}")
