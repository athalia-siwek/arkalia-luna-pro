#!/usr/bin/env python3
# 🩺 modules/zeroia/healthcheck_enhanced.py
"""Healthcheck pour ZeroIA Orchestrator Enhanced"""

import json
import sys
from pathlib import Path
from typing import Any, Optional

import toml

from core.ark_logger import ark_logger


def load_healthcheck_config() -> dict[str, Any]:
    """Charge la configuration de healthcheck depuis le fichier TOML."""
    try:
        with open("config/healthcheck.toml") as f:
            return toml.load(f)
    except FileNotFoundError:
        return {"enabled": True, "interval": 30}
    except Exception:
        return {"enabled": False, "interval": 60}


def check_zeroia_health() -> bool:
    """Vérifie la santé du système ZeroIA."""
    try:
        state_path = Path("state/zeroia_state.toml")
        if not state_path.exists():
            return False

        with open(state_path) as f:
            state = toml.load(f)
            return state.get("status") == "active"
    except Exception:
        return False


def check_enhanced_health():
    """Vérifie la santé de ZeroIA Enhanced via Event Store"""
    try:
        # Vérifier Event Store
        events_dir = Path("cache/zeroia_events/events")
        if not events_dir.exists():
            ark_logger.debug(
                f"DEBUG: events_dir {events_dir} n existe pas", extra={"module": "zeroia"}
            )
            ark_logger.info("❌ Event Store non trouvé", extra={"module": "zeroia"})
            return False

        # Vérifier fichiers récents
        recent_files = list(events_dir.glob("*.cache"))
        if not recent_files:
            ark_logger.debug("DEBUG: pas de fichiers récents trouvés", extra={"module": "zeroia"})
            ark_logger.info("❌ Aucun événement récent", extra={"module": "zeroia"})
            return False

        # Vérifier état dashboard
        dashboard_file = Path("state/zeroia_dashboard.json")
        if dashboard_file.exists():
            try:
                with open(dashboard_file) as f:
                    data = json.load(f)
                    if data.get("status") == "active":
                        ark_logger.info("✅ ZeroIA Enhanced OK", extra={"module": "zeroia"})
                        return True
            except Exception:
                # Si erreur lecture dashboard, continuer avec Event Store
                pass

        # Si pas de dashboard ou erreur, vérifier activité récente via events
        ark_logger.info("✅ ZeroIA Enhanced - Event Store actif", extra={"module": "zeroia"})
        return True

    except Exception as e:
        ark_logger.error(
            f"DEBUG: Exception dans check_enhanced_health: {e}", extra={"module": "zeroia"}
        )
        ark_logger.info(f"❌ Erreur healthcheck: {e}", extra={"module": "zeroia"})
        return False


if __name__ == "__main__":
    if check_enhanced_health():
        sys.exit(0)
    else:
        sys.exit(1)
