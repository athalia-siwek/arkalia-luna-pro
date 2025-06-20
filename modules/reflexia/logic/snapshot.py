import json
from datetime import datetime
from pathlib import Path

SNAPSHOT_FILE = Path("modules/reflexia/state/reflexia_state.toml")


def save_snapshot(metrics: dict, status: str):
    """
    Sauvegarde l'état réflexif dans un fichier .toml (format JSON simulé).
    """
    snapshot = {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": metrics,
        "status": status,
    }
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        f.write(json.dumps(snapshot, indent=2))
