# modules/zeroia/healthcheck_zeroia.py

import os
import sys
from pathlib import Path

import toml

DEFAULT_PATH = "modules/zeroia/state/zeroia_state.toml"
path = Path(os.environ.get("ZEROIA_STATE_PATH", DEFAULT_PATH))

try:
    if not path.exists():
        print("❌ Fichier zeroia_state.toml manquant.", flush=True)
        sys.exit(1)

    data = toml.load(path)

    # Validation logique
    active = data.get("active", False)
    last_decision = data.get("decision", {}).get("last_decision", None)

    if active is True and last_decision:
        print("✅ ZeroIA est active.", flush=True)
        sys.exit(0)
    else:
        print("❌ ZeroIA inactive ou état incomplet.", flush=True)
        sys.exit(1)

except Exception as e:
    print(f"💥 Erreur lors du chargement: {e}", flush=True)
    sys.exit(1)
