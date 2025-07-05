#!/usr/bin/env python3
# ✅ Healthcheck IA ZeroIA — Vérification de l'état cognitif

from core.ark_logger import ark_logger
import datetime
import os
import sys

import toml

STATE_PATH = "modules/zeroia/state/zeroia_state.toml"
REQUIRED_FIELDS = ["last_decision", "confidence_score", "justification", "timestamp"]


def check_state_file() -> int:
    if not os.path.exists(STATE_PATH):
        ark_logger.info("❌ Fichier d'état introuvable.", extra={"module": "scripts"})
        return 2

    try:
        with open(STATE_PATH) as f:
            data = toml.load(f)
    except toml.TomlDecodeError as e:
        ark_logger.info(f"❌ Erreur TOML : {e}", extra={"module": "scripts"})
        return 2

    decision_block = data.get("decision", {})
    missing = [f for f in REQUIRED_FIELDS if f not in decision_block]

    if missing:
        ark_logger.info(f"⚠️ Champs manquants : {missing}", extra={"module": "scripts"})
        return 1

    ark_logger.info("✅ État ZeroIA valide.", extra={"module": "scripts"})
    return 0


if __name__ == "__main__":
    code = check_state_file()
    now = datetime.datetime.now().isoformat()
    ark_logger.info(f"📆 Vérification effectuée à : {now}", extra={"module": "scripts"})
    sys.exit(code)
