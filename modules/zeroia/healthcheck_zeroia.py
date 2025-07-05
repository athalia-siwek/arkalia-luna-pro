"""
Module healthcheck_zeroia.

Ce module fait partie du système Arkalia Luna Pro.
"""

import os
import sys
from pathlib import Path

import toml

DEFAULT_PATH = "modules/zeroia/state/zeroia_state.toml"


def get_state_path() -> Path:
    """
    Fonction get_state_path.

    Cette fonction fait partie du système Arkalia Luna Pro.
    """
    return Path(os.environ.get("ZEROIA_STATE_PATH", DEFAULT_PATH))


def check_zeroia_health(verbose: bool = True) -> bool:
    try:
        state_path = get_state_path()

        if not state_path.exists():
            if verbose:
                print("❌ Fichier zeroia_state.toml manquant.", flush=True)
            return False

        data = toml.load(state_path)

        # Récupération des clés importantes
        active = data.get("active", False)
        last_decision = data.get("decision", {}).get("last_decision", None)

        if verbose:
            print(f"🩺 Debug: active={active}, last_decision={last_decision}", flush=True)

        # Vérification forcée (ex. pour les tests)
        if os.getenv("FORCE_ZEROIA_OK") == "1":
            if verbose:
                print("✅ ZeroIA forcée comme active (FORCE_ZEROIA_OK=1)", flush=True)
            return True

        # Vérification logique réelle
        if active is True and last_decision:
            if verbose:
                print("✅ ZeroIA est active.", flush=True)
            return True
        else:
            if verbose:
                print("❌ ZeroIA inactive ou état incomplet.", flush=True)
            return False

    except Exception as e:
        if verbose:
            print(f"💥 Erreur lors du chargement: {e}", flush=True)
        return False


if __name__ == "__main__":
    result = check_zeroia_health()
    sys.exit(0 if result else 1)
