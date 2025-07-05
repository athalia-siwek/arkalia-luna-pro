# 📄 modules/zeroia/snapshot_generator.py

import subprocess  # nosec
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import toml

from core.ark_logger import ark_logger

# 📌 Fichiers par défaut
STATE_FILE = Path(__file__).parent / "state" / "zeroia_state.toml"
SNAPSHOT_FILE = Path(__file__).parent / "state" / "zeroia_snapshot.toml"
FAILSAFE_SCRIPT = Path(__file__).parent / "failsafe.py"


def load_state(file_path: Path) -> dict:
    try:
        return toml.load(file_path)
    except FileNotFoundError:
        ark_logger.error(f"[ERROR] Fichier introuvable : {file_path}", extra={"module": "zeroia"})
        return {}
    except Exception as e:
        ark_logger.error(f"[ERROR] Chargement TOML échoué : {e}", extra={"module": "zeroia"})
        return {}


def is_valid_toml(data: dict) -> bool:
    try:
        toml.dumps(data)
        return True
    except Exception as e:
        ark_logger.error(f"[ERROR] Données TOML invalides : {e}", extra={"module": "zeroia"})
        return False


def generate_snapshot(
    input_path: Path | None = None,
    output_path: Path | None = None,
    fallback: bool = True,
) -> bool:
    input_file = input_path or STATE_FILE
    output_file = output_path or SNAPSHOT_FILE

    try:
        state = load_state(input_file)
        snapshot: dict[str, Any] = {}

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

        ark_logger.info(f"✅ Snapshot généré dans {output_file}", extra={"module": "zeroia"})

        with open("logs/snapshot_evolution.log", "a") as log_file:
            timestamp = datetime.utcnow().isoformat()
            score = snapshot.get("decision", {}).get("confidence_score", "N/A")
            log_file.write(f"{timestamp} :: Score: {score}\n")

        return True

    except Exception as e:
        ark_logger.error(f"[FAILSAFE] Échec snapshot : {e}", extra={"module": "zeroia"})
        if fallback and FAILSAFE_SCRIPT.exists():
            ark_logger.error("⚠️ Lancement du mode failsafe.", extra={"module": "zeroia"})
            subprocess.run([sys.executable, str(FAILSAFE_SCRIPT)], check=True)  # nosec
        return False


if __name__ == "__main__":
    generate_snapshot()
