import logging
from pathlib import Path

import toml

logging.basicConfig(level=logging.INFO)

state_path = Path("modules/zeroia/state/zeroia_state.toml")

try:
    data = toml.load(state_path)
    logging.info("✅ ZeroIA State: OK")
except Exception as e:
    logging.error(f"💥 ZeroIA State Error: {e}")
    exit(1)
