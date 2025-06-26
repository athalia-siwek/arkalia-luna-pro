# modules/zeroia/healthcheck_zeroia.py

import sys

import toml

try:
    state = toml.load("modules/zeroia/state/zeroia_state.toml")
    if state.get("active", False) is True:
        print("✅ ZeroIA state is active.")
        sys.exit(0)
    else:
        print("❌ ZeroIA inactive.")
        sys.exit(1)
except Exception as e:
    print(f"💥 Healthcheck error: {e}")
    sys.exit(1)
