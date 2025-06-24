from pathlib import Path

import toml

LOG_PATH = Path("modules/zeroia/state/zeroia_decision_log.toml")


def load_decision_log():
    if LOG_PATH.exists():
        return toml.load(LOG_PATH).get("decisions", [])
    return []


def count_recent_action(action: str, window: int = 10) -> int:
    log = load_decision_log()[-window:]
    return sum(1 for entry in log if entry["output"] == action)


def should_lower_cpu_threshold() -> bool:
    return count_recent_action("monitor", window=10) >= 8
