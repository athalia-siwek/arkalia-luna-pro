import logging
import textwrap
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

import toml

from modules.zeroia.adaptive_thresholds import should_lower_cpu_threshold
from modules.zeroia.utils.state_writer import (
    save_json_if_changed,
    save_toml_if_changed,
)

# === Chemins par défaut ===
CTX_PATH = Path("state/global_context.toml")
REFLEXIA_STATE = Path("state/reflexia_state.toml")
LOG_PATH = Path("modules/zeroia/logs/zeroia.log")
STATE_PATH = Path("modules/zeroia/state/zeroia_state.toml")
DASHBOARD_PATH = Path("state/zeroia_dashboard.json")
CONFIG_PATH = Path("config/zeroia_config.toml")

# === Fallback pour contradiction log
DEFAULT_CONTRADICTION_LOG = Path("logs/zeroia_contradictions.log")

# === Logger contradiction
logger = logging.getLogger("zeroia_contradictions")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    DEFAULT_CONTRADICTION_LOG, maxBytes=5 * 1024 * 1024, backupCount=5
)
formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# === Chargements TOML robustes ===
def load_toml(path: Path) -> dict:
    try:
        if not path.exists() or path.read_text().strip() == "":
            raise ValueError(f"TOML file {path} is empty or missing")
        return toml.load(path)
    except toml.TomlDecodeError as e:
        print(f"[DEBUG] TOML Decode Error: {e}")
        raise ValueError(f"Invalid TOML format in {path}: {e}")
    except Exception as e:
        print(f"[DEBUG] General Error: {e}")
        raise ValueError(f"Failed to load TOML file {path}: {e}")


def load_context(path: Path = CTX_PATH) -> dict:
    return load_toml(path)


def load_reflexia_state(path: Path = REFLEXIA_STATE) -> dict:
    return load_toml(path)


# === Décision IA ===
def decide(context: dict) -> tuple[str, float]:
    status = context.get("status", {})
    severity = status.get("severity", "none")
    cpu = status.get("cpu", 0)

    if should_lower_cpu_threshold() and cpu > 70:
        return "reduce_load", 0.75
    if severity == "critical":
        return "emergency_shutdown", 1.0
    elif cpu > 80:
        return "reduce_load", 0.8
    elif cpu > 60:
        return "monitor", 0.6
    return "normal", 0.4


def ensure_parent_dir(path: Path) -> None:
    (path.parent if path.suffix else path).mkdir(parents=True, exist_ok=True)


def persist_state(
    decision: str,
    score: float,
    ctx: dict,
    state_path_override: Optional[Path] = None,
) -> None:
    reflexia_summary = ctx.get("reflexia", {})
    status = ctx.get("status", {})
    cpu = status.get("cpu", "N/A")
    severity = status.get("severity", "none")

    state_path = state_path_override or STATE_PATH
    ensure_parent_dir(state_path)
    save_toml_if_changed(
        {
            "decision": {
                "last_decision": decision,
                "confidence_score": score,
                "justification": f"cpu={cpu}, severity={severity}",
                "timestamp": str(datetime.now()),
            }
        },
        str(state_path),
    )

    ensure_parent_dir(LOG_PATH)
    with open(LOG_PATH, "a") as f:
        f.write(
            f"{datetime.now()} :: FROM REFLEXIA: {reflexia_summary} | "
            f"CPU={cpu} | SEVERITY={severity} → DECISION = {decision} "
            f"(confidence={score})\n"
        )


def update_dashboard(
    decision: str,
    score: float,
    ctx: dict,
    dashboard_path_override: Optional[Path] = None,
) -> None:
    dashboard_path = dashboard_path_override or DASHBOARD_PATH
    ensure_parent_dir(dashboard_path)
    save_json_if_changed(
        {
            "last_decision": decision,
            "confidence": score,
            "reasoning_loop_active": True,
            "connected_modules": ["reflexia"],
            "previous": ["reduce_load", "monitor", "monitor"],
            "last_updated": str(datetime.now()),
        },
        str(dashboard_path),
    )


def get_configured_contradiction_log() -> Path:
    try:
        config = toml.load(CONFIG_PATH)
        log_path_str = config.get("logging", {}).get("contradiction_log_path")
        return Path(log_path_str) if log_path_str else DEFAULT_CONTRADICTION_LOG
    except Exception:
        return DEFAULT_CONTRADICTION_LOG


def check_for_ia_conflict(
    reflexia_decision: str,
    zeroia_decision: str,
    log_path: Path = get_configured_contradiction_log(),
) -> bool:
    if reflexia_decision != zeroia_decision:
        ensure_parent_dir(log_path)
        with open(log_path, "a") as f:
            f.write(
                textwrap.dedent(
                    f"""
                [{datetime.utcnow()}] CONTRADICTION DETECTÉE — \
                ReflexIA={reflexia_decision}, ZeroIA={zeroia_decision}\n
                """
                )
            )
        return True
    return False


def log_conflict(conflict_msg: str) -> None:
    logger.debug(conflict_msg)
    logger.info(
        "💥 Contradiction explicite entre ReflexIA et ZeroIA "
        "(mocks injectés sur chemins TOML)"
    )


def check_and_exit_if_inactive():
    state = load_toml(STATE_PATH)
    if not state.get("active", True):
        print("🛑 ZeroIA détectée inactive, arrêt boucle.")
        exit(1)


def reason_loop(
    context_path: Optional[Path] = None,
    reflexia_path: Optional[Path] = None,
    state_path: Optional[Path] = None,
    dashboard_path: Optional[Path] = None,
    log_path: Optional[Path] = None,
    contradiction_log_path: Optional[Path] = None,
) -> tuple[str, float]:
    check_and_exit_if_inactive()
    ctx = load_context(context_path or CTX_PATH)
    reflexia_data = load_reflexia_state(reflexia_path or REFLEXIA_STATE)

    if not ctx:
        raise ValueError(
            f"Context file {context_path or CTX_PATH} is empty or invalid."
        )

    ctx["reflexia"] = reflexia_data.get("reflexia", {})
    ctx.setdefault("status", {}).update(reflexia_data.get("status", {}))

    if "cpu" not in ctx["status"] or "ram" not in ctx["status"]:
        raise KeyError(
            "Missing required keys in context: 'cpu' and 'ram' must be present."
        )

    cpu = ctx["status"].get("cpu", 0)
    decision, score = decide(ctx)

    persist_state(decision, score, ctx, state_path)
    update_dashboard(decision, score, ctx, dashboard_path)

    if check_for_ia_conflict(
        reflexia_data.get("decision", {}).get("last_decision", "unknown"),
        decision,
        log_path=contradiction_log_path or get_configured_contradiction_log(),
    ):
        log_conflict(
            f"CONTRADICTION DETECTED: ReflexIA = "
            f"{reflexia_data.get('decision', {}).get('last_decision')}, "
            f"ZeroIA = {decision}"
        )

    print(f"CPU usage: {cpu}%")
    return decision, score


def compute_confidence_score(success_rate: float, error_rate: float) -> float:
    return max(0.0, min(1.0, success_rate - error_rate))


def main():
    print("🟢 ZeroIA loop started successfully")
    decision, score = reason_loop()
    print(f"ZeroIA decided: {decision} (confidence={score})")


if __name__ == "__main__":
    main()
