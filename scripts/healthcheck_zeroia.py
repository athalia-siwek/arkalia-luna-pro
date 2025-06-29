#!/usr/bin/env python3
# ✅ Healthcheck IA ZeroIA — Vérification de l'état cognitif

import datetime
import os
import sys

import toml

STATE_PATH = "modules/zeroia/state/zeroia_state.toml"
REQUIRED_FIELDS = ["last_decision", "confidence_score", "justification", "timestamp"]


def check_state_file() -> None:
    if not os.path.exists(STATE_PATH):
        print("❌ Fichier d'état introuvable.")
        return 2

    try:
        with open(STATE_PATH) as f:
            data = toml.load(f)
    except toml.TomlDecodeError as e:
        print(f"❌ Erreur TOML : {e}")
        return 2

    decision_block = data.get("decision", {})
    missing = [f for f in REQUIRED_FIELDS if f not in decision_block]

    if missing:
        print(f"⚠️ Champs manquants : {missing}")
        return 1

    print("✅ État ZeroIA valide.")
    return 0


if __name__ == "__main__":
    code = check_state_file()
    now = datetime.datetime.now().isoformat()
    print(f"📆 Vérification effectuée à : {now}")
    sys.exit(code)
