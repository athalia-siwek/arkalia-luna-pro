"""
Module state.

Ce module fait partie du système Arkalia Luna Pro.
"""

from typing import Any, Optional

import toml


class HelloriaStateManager:
    """
    Classe HelloriaStateManager.

    Cette classe fait partie du système Arkalia Luna Pro.
    """

    def __init__(self, path: str = "state/helloria_state.toml") -> None:
        """
        Fonction __init__.

        Cette fonction fait partie du système Arkalia Luna Pro.
        """
        self.path = path
        self.state: dict[str, Any] = {}

    def load(self) -> None:
        """
        Fonction load.

        Cette fonction fait partie du système Arkalia Luna Pro.
        """
        try:
            self.state = toml.load(self.path)
        except FileNotFoundError:
            self.state = {}

    def save(self) -> None:
        """
        Fonction save.

        Cette fonction fait partie du système Arkalia Luna Pro.
        """
        with open(self.path, "w") as f:
            toml.dump(self.state, f)


def load_helloria_state(state: dict[str, Any]) -> dict[str, Any]:
    try:
        with open("state/helloria_state.toml") as f:
            return toml.load(f)
    except FileNotFoundError:
        return {"status": "inactive"}
    except Exception:
        return {"status": "error"}


def save_helloria_state(state: dict[str, Any]) -> None:
    try:
        with open("state/helloria_state.toml", "w") as f:
            toml.dump(state, f)
    except Exception:
        pass  # Ignore les erreurs d'écriture


IS_HELLORIA = True
