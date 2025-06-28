import logging
import textwrap
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

import toml

from modules.zeroia.adaptive_thresholds import should_lower_cpu_threshold
from modules.zeroia.model_integrity import validate_decision_integrity
from modules.zeroia.utils.backup import save_backup
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
DEFAULT_CONTRADICTION_LOG = Path("logs/zeroia_contradictions.log")

# === Variables globales pour anti-répétition ===
LAST_DECISION = None
LAST_DECISION_TIME = None
MIN_DECISION_INTERVAL = 30  # seconds - Évite les répétitions trop fréquentes

# === Logger contradiction (rotatif) ===
logger = logging.getLogger("zeroia_contradictions")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    DEFAULT_CONTRADICTION_LOG, maxBytes=5 * 1024 * 1024, backupCount=5
)
formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def load_toml(path: Path) -> dict:
    try:
        if not path.exists() or not path.read_text().strip():
            raise ValueError(f"TOML file {path} is empty or missing")
        return toml.load(path)
    except toml.TomlDecodeError as e:
        raise ValueError(f"[TOML] Format invalide dans {path}: {e}")
    except Exception as e:
        raise ValueError(f"[TOML] Erreur lors du chargement de {path}: {e}")


def load_context(path: Path = CTX_PATH) -> dict:
    return load_toml(path)


def load_reflexia_state(path: Path = REFLEXIA_STATE) -> dict:
    return load_toml(path)


def decide(context: dict) -> tuple[str, float]:
    status = context.get("status", {})
    severity = status.get("severity", "none")
    cpu = status.get("cpu", 0)

    if should_lower_cpu_threshold() and cpu > 70:
        return "reduce_load", 0.75
    if severity == "critical":
        return "emergency_shutdown", 1.0
    if cpu > 80:
        return "reduce_load", 0.8
    if cpu > 60:
        return "monitor", 0.6
    return "normal", 0.4


def should_process_decision(new_decision: str) -> bool:
    """Évite les répétitions excessives de la même décision"""
    global LAST_DECISION, LAST_DECISION_TIME

    current_time = datetime.now()

    # Si c'est une nouvelle décision différente, on l'accepte
    if new_decision != LAST_DECISION:
        LAST_DECISION = new_decision
        LAST_DECISION_TIME = current_time
        return True

    # Si c'est la même décision, on vérifie l'intervalle de temps
    if LAST_DECISION_TIME is None:
        LAST_DECISION_TIME = current_time
        return True

    time_diff = (current_time - LAST_DECISION_TIME).total_seconds()

    # On accepte la répétition seulement si assez de temps s'est écoulé
    if time_diff >= MIN_DECISION_INTERVAL:
        LAST_DECISION_TIME = current_time
        return True

    return False


def ensure_parent_dir(path: Path) -> None:
    target = path.parent if path.suffix else path
    target.mkdir(parents=True, exist_ok=True)


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
    save_backup()

    save_toml_if_changed(
        {
            "decision": {
                "last_decision": decision,
                "confidence_score": score,
                "justification": f"cpu={cpu}, severity={severity}",
                "timestamp": datetime.now().isoformat(),
            }
        },
        str(state_path),
    )

    ensure_parent_dir(LOG_PATH)
    with open(LOG_PATH, "a") as f:
        f.write(
            f"{datetime.now()} :: FROM REFLEXIA: {reflexia_summary} | "
            f"CPU={cpu} | SEVERITY={severity} → DECISION = "
            f"{decision} (confidence={score})\n"
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
            "last_updated": datetime.now().isoformat(),
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
    log_path: Path,
) -> bool:
    if reflexia_decision != zeroia_decision:
        ensure_parent_dir(log_path)
        with open(log_path, "a") as f:
            f.write(
                textwrap.dedent(
                    f"""
                    [{datetime.utcnow()}] CONTRADICTION DETECTÉE —
                    ReflexIA={reflexia_decision}, ZeroIA={zeroia_decision}\n
                    """
                )
            )
        return True
    return False


def log_conflict(conflict_msg: str) -> None:
    logger.debug(conflict_msg)
    logger.info("🔄 ZeroIA loop started successfully")


def reason_loop(
    context_path: Optional[Path] = None,
    reflexia_path: Optional[Path] = None,
    state_path: Optional[Path] = None,
    dashboard_path: Optional[Path] = None,
    log_path: Optional[Path] = None,
    contradiction_log_path: Optional[Path] = None,
) -> tuple[str, float]:
    ctx = load_context(context_path or CTX_PATH)
    reflexia_data = load_reflexia_state(reflexia_path or REFLEXIA_STATE)

    # 🛡️ ROBUSTESSE v3.x - Valeurs par défaut si CPU/RAM manquants
    status = ctx.get("status", {})
    if "cpu" not in status or "ram" not in status:
        print("⚠️ [ZeroIA] CPU/RAM missing in context, using defaults", flush=True)
        # Créer une section status avec valeurs par défaut
        ctx["status"] = {
            "cpu": status.get("cpu", 45),  # CPU par défaut : 45%
            "ram": status.get("ram", 62),  # RAM par défaut : 62%
            "severity": status.get("severity", "normal"),
            "disk_usage": status.get("disk_usage", 78),
            "network_latency": status.get("network_latency", 25),
        }

    decision, score = decide(ctx)

    # 🛡️ VALIDATION INTÉGRITÉ MODÈLE - Roadmap S2
    try:
        integrity_valid, integrity_reason = validate_decision_integrity(
            ctx, decision, score
        )
        if not integrity_valid:
            print(f"🚨 [ZeroIA] INTEGRITY VIOLATION: {integrity_reason}", flush=True)
            # En cas de compromission, forcer décision sécurisée
            decision, score = "monitor", 0.3
    except Exception as e:
        print(f"⚠️ [ZeroIA] Integrity check failed: {e}", flush=True)

    # Vérifie si on doit traiter cette décision (anti-spam)
    if not should_process_decision(decision):
        print(
            f"[ZeroIA] Décision {decision} ignorée (répétition trop fréquente)",
            flush=True,
        )
        return decision, score

    persist_state(decision, score, ctx, state_path)
    update_dashboard(decision, score, ctx, dashboard_path)

    reflexia_decision = reflexia_data.get("decision", {}).get(
        "last_decision", "unknown"
    )
    if check_for_ia_conflict(
        reflexia_decision,
        decision,
        log_path=contradiction_log_path or get_configured_contradiction_log(),
    ):
        log_conflict(
            f"CONTRADICTION DETECTED: ReflexIA = {reflexia_decision}, "
            f"ZeroIA = {decision}"
        )

    # Logs modifiés pour éviter le spam
    status = ctx.get("status", {})
    cpu = status.get("cpu", "N/A")
    print(f"✅ ZeroIA decided: {decision} (confidence={score})", flush=True)
    print(
        f"[ZeroIA] CPU usage: {cpu}% → decision={decision} (score={score})", flush=True
    )

    return decision, score


def compute_confidence_score(success_rate: float, error_rate: float) -> float:
    return max(0.0, min(1.0, success_rate - error_rate))


def main_loop() -> None:
    print("[ZeroIA] loop started", flush=True)
    try:
        reason_loop()
    except Exception as e:
        print(f"[ZeroIA] 🚨 ERREUR dans reason_loop(): {e}", flush=True)
        logger.exception(e)


if __name__ == "__main__":
    try:
        print("[ZeroIA] 🔄 Boucle cognitive initialisée...", flush=True)
        while True:
            main_loop()
            time.sleep(15)  # Augmentation de l'intervalle à 15 secondes
    except KeyboardInterrupt:
        print("[ZeroIA] 🧠 Arrêt manuel détecté.")
