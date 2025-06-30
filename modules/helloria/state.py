from typing import Any

import toml


class HelloriaStateManager:
    def __init__(self, path="state/helloria_state.toml") -> None:
        self.path = path
        self.state = {}

    def load(self) -> None:
        try:
            self.state = toml.load(self.path)
        except FileNotFoundError:
            self.state = {}

    def save(self) -> None:
        with open(self.path, "w") as f:
            toml.dump(self.state, f)


def load_helloria_state(state: dict[str, Any]) -> dict[str, Any]:
    """Charge l'état Helloria depuis le fichier TOML."""
    try:
        with open("state/helloria_state.toml") as f:
            return toml.load(f)
    except FileNotFoundError:
        return {"status": "inactive"}
    except Exception:
        return {"status": "error"}


def save_helloria_state(state: dict[str, Any]) -> None:
    """Sauvegarde l'état Helloria dans le fichier TOML."""
    try:
        with open("state/helloria_state.toml", "w") as f:
            toml.dump(state, f)
    except Exception:
        pass  # Ignore les erreurs d'écriture


IS_HELLORIA = True
