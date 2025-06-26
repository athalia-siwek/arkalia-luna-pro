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


def adjust_threshold(current: float, feedback: str) -> float:
    if feedback == "success":
        return min(1.0, current + 0.05)
    elif feedback == "fail":
        return max(0.0, current - 0.05)
    elif feedback == "neutral":
        return current
    else:
        raise ValueError(f"Unknown feedback: {feedback}")
