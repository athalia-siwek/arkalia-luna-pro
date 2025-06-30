from pathlib import Path
from typing import Any, Dict, Optional

import toml

STATE_FILE = Path("modules/zeroia/state/zeroia_state.toml")


def load_state(path: Path = STATE_FILE) -> dict[str, Any]:
    """
    Charge un fichier TOML en tant qu'état. Retourne un dict vide si absent.
    """
    if not path.exists() or path.stat().st_size == 0:
        raise ValueError(f"TOML file {path} is empty or missing")
    return toml.load(path)


def save_state(path: Path, data: dict[str, Any]) -> None:
    """
    Sauvegarde les données de l'état au format TOML.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        toml.dump(data, f)


def load_zeroia_state() -> dict[str, Any]:
    """Charge l'état ZeroIA depuis le fichier TOML."""
    try:
        with open("state/zeroia_state.toml") as f:
            return toml.load(f)
    except FileNotFoundError:
        return {"status": "inactive", "last_decision": None}
    except Exception:
        return {"status": "error", "last_decision": None}
