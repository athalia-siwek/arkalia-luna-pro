from core.ark_logger import ark_logger
import os
import sys
from pathlib import Path

import toml

DEFAULT_PATH = "modules/zeroia/state/zeroia_state.toml"


def get_state_path() -> Path:
    return Path(os.environ.get("ZEROIA_STATE_PATH", DEFAULT_PATH))


def check_zeroia_health(verbose: bool = True) -> bool:
    """Vérifie si ZeroIA est active avec une dernière décision."""
    try:
        state_path = get_state_path()

        if not state_path.exists():
            if verbose:
                ark_logger.info("❌ Fichier zeroia_state.toml manquant.", flush=True, extra={"module": "zeroia"})
            return False

        data = toml.load(state_path)

        # Récupération des clés importantes
        active = data.get("active", False)
        last_decision = data.get("decision", {}).get("last_decision", None)

        if verbose:
            ark_logger.debug(f"🩺 Debug: active={active}, last_decision={last_decision}", flush=True, extra={"module": "zeroia"})

        # Vérification forcée (ex. pour les tests)
        if os.getenv("FORCE_ZEROIA_OK") == "1":
            if verbose:
                ark_logger.info("✅ ZeroIA forcée comme active (FORCE_ZEROIA_OK=1, extra={"module": "zeroia"})", flush=True)
            return True

        # Vérification logique réelle
        if active is True and last_decision:
            if verbose:
                ark_logger.info("✅ ZeroIA est active.", flush=True, extra={"module": "zeroia"})
            return True
        else:
            if verbose:
                ark_logger.info("❌ ZeroIA inactive ou état incomplet.", flush=True, extra={"module": "zeroia"})
            return False

    except Exception as e:
        if verbose:
            ark_logger.info(f"💥 Erreur lors du chargement: {e}", flush=True, extra={"module": "zeroia"})
        return False


if __name__ == "__main__":
    result = check_zeroia_health()
    sys.exit(0 if result else 1)
