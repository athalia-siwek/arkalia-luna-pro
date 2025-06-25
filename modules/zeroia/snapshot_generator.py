# 📄 modules/zeroia/snapshot_generator.py

import os
from datetime import datetime

import toml


def load_state(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            return toml.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except Exception as e:
        print(f"Error loading state: {e}")
        return {}


STATE_FILE = os.path.join(os.path.dirname(__file__), "state", "zeroia_state.toml")
SNAPSHOT_FILE = os.path.join(os.path.dirname(__file__), "state", "zeroia_snapshot.toml")

try:
    state = load_state(STATE_FILE)
    state["snapshot_time"] = datetime.utcnow().isoformat()
    with open(SNAPSHOT_FILE, "w") as f:
        toml.dump(state, f)
    print(f"✅ Snapshot généré dans {SNAPSHOT_FILE}")
except Exception as e:
    print(f"[FAILSAFE] Échec snapshot : {e}")
    os.system(f"python {os.path.join(os.path.dirname(__file__), 'failsafe.py')}")
    exit(1)
