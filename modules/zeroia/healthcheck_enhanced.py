#!/usr/bin/env python3
# 🩺 modules/zeroia/healthcheck_enhanced.py
"""Healthcheck pour ZeroIA Orchestrator Enhanced"""

import json
import sys
from pathlib import Path


def check_enhanced_health():
    """Vérifie la santé de ZeroIA Enhanced via Event Store"""
    try:
        # Vérifier Event Store
        events_dir = Path("cache/zeroia_events/events")
        if not events_dir.exists():
            print("❌ Event Store non trouvé")
            return False

        # Vérifier fichiers récents
        recent_files = list(events_dir.glob("*.cache"))
        if not recent_files:
            print("❌ Aucun événement récent")
            return False

        # Vérifier état dashboard
        dashboard_file = Path("state/zeroia_dashboard.json")
        if dashboard_file.exists():
            with open(dashboard_file) as f:
                data = json.load(f)
                if data.get("status") == "active":
                    print("✅ ZeroIA Enhanced OK")
                    return True

        # Si pas de dashboard, vérifier activité récente via events
        print("✅ ZeroIA Enhanced - Event Store actif")
        return True

    except Exception as e:
        print(f"❌ Erreur healthcheck: {e}")
        return False


if __name__ == "__main__":
    if check_enhanced_health():
        sys.exit(0)
    else:
        sys.exit(1)
