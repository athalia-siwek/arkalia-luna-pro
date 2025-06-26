# 📄 modules/zeroia/snapshot_generator.py

from datetime import datetime
from pathlib import Path
from typing import Optional

import toml

# 📌 Fichiers par défaut
STATE_FILE = Path(__file__).parent / "state" / "zeroia_state.toml"
SNAPSHOT_FILE = Path(__file__).parent / "state" / "zeroia_snapshot.toml"
FAILSAFE_SCRIPT = Path(__file__).parent / "failsafe.py"


def load_state(file_path: Path) -> dict:
    try:
        return toml.load(file_path)
    except FileNotFoundError:
        print(f"[ERROR] Fichier introuvable : {file_path}")
        return {}
    except Exception as e:
        print(f"[ERROR] Chargement TOML échoué : {e}")
        return {}


def is_valid_toml(data: dict) -> bool:
    try:
        toml.dumps(data)
        return True
    except Exception as e:
        print(f"[ERROR] Données TOML invalides : {e}")
        return False


def generate_snapshot(
    input_path: Optional[Path] = None,
    output_path: Optional[Path] = None,
    fallback: bool = True,
) -> bool:
    input_file = input_path or STATE_FILE
    output_file = output_path or SNAPSHOT_FILE

    try:
        state = load_state(input_file)
        snapshot = {}

        # ✅ Sections pertinentes
        if "inputs" in state:
            snapshot["inputs"] = state["inputs"]
        if "decision" in state:
            snapshot["decision"] = state["decision"]

        # 🕓 Timestamps
        snapshot["timestamp"] = state.get("timestamp", datetime.utcnow().isoformat())
        snapshot["snapshot_time"] = datetime.utcnow().isoformat()

        # 🔒 Validation
        if not is_valid_toml(snapshot):
            raise ValueError("Échec validation TOML")

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w") as f:
            toml.dump(snapshot, f)

        print(f"✅ Snapshot généré dans {output_file}")
        return True

    except Exception as e:
        print(f"[FAILSAFE] Échec snapshot : {e}")
        if fallback and FAILSAFE_SCRIPT.exists():
            print("⚠️ Lancement du mode failsafe.")
            import subprocess

            subprocess.run(["python", str(FAILSAFE_SCRIPT)])
        return False


if __name__ == "__main__":
    generate_snapshot()
