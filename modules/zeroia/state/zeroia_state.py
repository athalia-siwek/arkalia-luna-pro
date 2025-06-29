from pathlib import Path
from typing import Any, Optional

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
