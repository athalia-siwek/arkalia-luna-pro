from pathlib import Path

import toml

state_path = Path("modules/zeroia/state/zeroia_state.toml")

try:
    data = toml.load(state_path)
    print("✅ ZeroIA State: OK")
except Exception as e:
    print(f"💥 ZeroIA State Error: {e}")
    exit(1)
