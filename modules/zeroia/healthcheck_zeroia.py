# modules/zeroia/healthcheck_zeroia.py

import os
import sys
from pathlib import Path

import toml

DEFAULT_PATH = "modules/zeroia/state/zeroia_state.toml"
path = Path(os.environ.get("ZEROIA_STATE_PATH", DEFAULT_PATH))


def check_zeroia_health():
    try:
        if not path.exists():
            print("❌ Fichier zeroia_state.toml manquant.", flush=True)
            return False

        data = toml.load(path)

        # Validation logique
        active = data.get("active", False)
        last_decision = data.get("decision", {}).get("last_decision", None)

        if active is True and last_decision:
            print("✅ ZeroIA est active.", flush=True)
            return True
        else:
            print("❌ ZeroIA inactive ou état incomplet.", flush=True)
            return False

    except Exception as e:
        print(f"💥 Erreur lors du chargement: {e}", flush=True)
        return False


if __name__ == "__main__":
    if not check_zeroia_health():
        sys.exit(1)
