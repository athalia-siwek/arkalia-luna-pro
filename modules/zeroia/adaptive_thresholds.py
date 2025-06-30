from pathlib import Path
from typing import Any, Optional

import toml

LOG_PATH = Path("modules/zeroia/state/zeroia_decision_log.toml")


def load_decision_log(file_path: str) -> dict[str, Any] | None:
    """Charge le log de décisions depuis un fichier TOML"""
    try:
        with open(file_path, encoding="utf-8") as f:
            return toml.load(f)
    except Exception:
        return None


def analyze_decision_patterns(log_data: dict[str, Any]) -> dict[str, Any]:
    """Analyse les patterns de décisions pour ajuster les seuils"""
    # Analyse des patterns
    return {"patterns": log_data}


def adjust_thresholds_based_on_history(history: dict[str, Any]) -> None:
    """Ajuste les seuils basés sur l'historique des décisions"""
    # Logique d'ajustement des seuils
    pass


def count_recent_action(action: str, window: int = 10) -> int:
    log_data = load_decision_log(str(LOG_PATH))
    if log_data is None or "decisions" not in log_data:
        return 0
    log = log_data["decisions"][-window:]
    return sum(1 for entry in log if entry.get("output") == action)


def should_lower_cpu_threshold() -> bool:
    return count_recent_action("monitor", window=10) >= 8


def load_adaptive_thresholds_config() -> dict[str, Any] | None:
    """Charge la configuration des seuils adaptatifs depuis le fichier TOML."""
    try:
        with open("config/adaptive_thresholds.toml") as f:
            data = toml.load(f)
            return data if isinstance(data, dict) else None
    except FileNotFoundError:
        return None
    except Exception:
        return None


def adjust_threshold(current_threshold: float, feedback: str) -> float:
    """
    Ajuste le seuil en fonction du feedback reçu.

    Args:
        current_threshold: Le seuil actuel
        feedback: Le feedback ('increase', 'decrease', 'stable')

    Returns:
        Le nouveau seuil ajusté
    """
    if feedback == "increase":
        return current_threshold * 1.1
    elif feedback == "decrease":
        return current_threshold * 0.9
    else:
        return current_threshold


def save_adaptive_thresholds_config(config: dict[str, Any]) -> None:
    """Sauvegarde la configuration des seuils adaptatifs."""
    try:
        with open("config/adaptive_thresholds.toml", "w") as f:
            toml.dump(config, f)
    except Exception:
        pass  # Ignore les erreurs d'écriture
