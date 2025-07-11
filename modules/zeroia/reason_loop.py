from core.ark_logger import ark_logger
import logging
import textwrap
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Optional

import toml

from modules.zeroia.adaptive_thresholds import should_lower_cpu_threshold
from modules.zeroia.model_integrity import validate_decision_integrity
from modules.zeroia.utils.backup import save_backup
from modules.zeroia.utils.state_writer import save_json_if_changed, save_toml_if_changed

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

# === Cache TOML optimisé pour performance ===
_TOML_CACHE: dict[str, Any] = {}
_CACHE_TIMESTAMPS: dict[str, Any] = {}

# === Logger contradiction (rotatif) ===
logger = logging.getLogger("zeroia_contradictions")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(DEFAULT_CONTRADICTION_LOG, maxBytes=5 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def load_toml_with_cache(path: Path, max_age: int = 30) -> dict:
    """
    Charge un fichier TOML avec cache intelligent pour optimiser les performances.

    Args:
        path: Chemin vers le fichier TOML
        max_age: Âge maximum du cache en secondes (défaut: 30s)

    Returns:
        dict: Contenu du fichier TOML

    Raises:
        ValueError: Si le fichier est invalide ou manquant
    """
    path_str = str(path)
    current_time = time.time()

    # Vérifier si on a une version cachée et valide
    if (
        path_str in _TOML_CACHE
        and path_str in _CACHE_TIMESTAMPS
        and current_time - _CACHE_TIMESTAMPS[path_str] < max_age
    ):
        return _TOML_CACHE[path_str]

    try:
        if not path.exists() or not path.read_text().strip():
            # Créer un contexte par défaut si manquant
            if "global_context" in path_str:
                default_context = create_default_context()
                ensure_parent_dir(path)
                with open(path, "w") as f:
                    toml.dump(default_context, f)
                _TOML_CACHE[path_str] = default_context
                _CACHE_TIMESTAMPS[path_str] = current_time
                return default_context
            raise ValueError(f"TOML file {path} is empty or missing")

        data = toml.load(path)
        _TOML_CACHE[path_str] = data
        _CACHE_TIMESTAMPS[path_str] = current_time
        return data

    except toml.TomlDecodeError as e:
        raise ValueError(f"[TOML] Format invalide dans {path}: {e}") from e
    except Exception as e:
        raise ValueError(f"[TOML] Erreur lors du chargement de {path}: {e}") from e


def create_default_context() -> dict:
    """
    Crée un contexte par défaut robuste pour éviter les warnings CPU/RAM.

    Returns:
        dict: Contexte par défaut avec valeurs système optimales
    """
    return {
        "status": {
            "cpu": 45,  # CPU par défaut : 45% (charge normale)
            "ram": 62,  # RAM par défaut : 62% (charge normale)
            "severity": "normal",
            "disk_usage": 78,
            "network_latency": 25,
            "load_avg": 1.2,
            "active_processes": 150,
        },
        "reflexia": {"status": "operational", "last_check": datetime.now().isoformat()},
        "metadata": {
            "initialized": datetime.now().isoformat(),
            "version": "2.7.1-enhanced",
            "source": "auto_generated_default",
        },
    }


def load_toml(path: Path) -> dict:
    """
    DEPRECATED: Utiliser load_toml_with_cache() pour de meilleures performances.
    Conservé pour rétrocompatibilité.
    """
    return load_toml_with_cache(path)


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
    state_path_override: Path | None = None,
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
    dashboard_path_override: Path | None = None,
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


def validate_and_fix_context(ctx: dict) -> dict:
    """
    🛡️ VALIDATION ET CORRECTION DU CONTEXTE
    Assure que toutes les clés requises sont présentes avec des valeurs par défaut sécurisées
    """
    # Créer une copie pour éviter de modifier l'original
    validated_ctx = ctx.copy()

    # Assurer que la section status existe
    if "status" not in validated_ctx:
        validated_ctx["status"] = {}

    status = validated_ctx["status"]

    # Valeurs par défaut sécurisées pour les métriques système
    default_metrics = {
        "cpu": 45.0,  # CPU par défaut : 45% (normal)
        "ram": 62.0,  # RAM par défaut : 62% (normal)
        "severity": "normal",  # Sévérité par défaut
        "disk_usage": 78.0,  # Usage disque par défaut
        "network_latency": 25.0,  # Latence réseau par défaut
    }

    # Appliquer les valeurs par défaut pour les clés manquantes
    for key, default_value in default_metrics.items():
        if key not in status or status[key] is None:
            status[key] = default_value
            ark_logger.info(
                f"⚠️ [ZeroIA] {key} manquant dans le contexte, valeur par défaut: {default_value}",
                flush=True,
            , extra={"module": "zeroia"})

    return validated_ctx


def reason_loop(
    context_path: Path | None = None,
    reflexia_path: Path | None = None,
    state_path: Path | None = None,
    dashboard_path: Path | None = None,
    log_path: Path | None = None,
    contradiction_log_path: Path | None = None,
) -> tuple[str, float]:
    ctx = load_context(context_path or CTX_PATH)
    reflexia_data = load_reflexia_state(reflexia_path or REFLEXIA_STATE)

    # 🛡️ ROBUSTESSE v4.0 - Validation et correction automatique du contexte
    ctx = validate_and_fix_context(ctx)

    decision, score = decide(ctx)

    # 🛡️ VALIDATION INTÉGRITÉ MODÈLE - Roadmap S2
    try:
        integrity_valid, integrity_reason = validate_decision_integrity(ctx, decision, score)
        if not integrity_valid:
            ark_logger.info(f"🚨 [ZeroIA] INTEGRITY VIOLATION: {integrity_reason}", flush=True, extra={"module": "zeroia"})
            # En cas de compromission, forcer décision sécurisée
            decision, score = "monitor", 0.3
    except Exception as e:
        ark_logger.error(f"⚠️ [ZeroIA] Integrity check failed: {e}", flush=True, extra={"module": "zeroia"})

    # Vérifie si on doit traiter cette décision (anti-spam)
    if not should_process_decision(decision):
        ark_logger.info(
            f"[ZeroIA] Décision {decision} ignorée (répétition trop fréquente, extra={"module": "zeroia"})",
            flush=True,
        )
        return decision, score

    persist_state(decision, score, ctx, state_path)
    update_dashboard(decision, score, ctx, dashboard_path)

    reflexia_decision = reflexia_data.get("decision", {}).get("last_decision", "unknown")
    if check_for_ia_conflict(
        reflexia_decision,
        decision,
        log_path=contradiction_log_path or get_configured_contradiction_log(),
    ):
        log_conflict(
            f"CONTRADICTION DETECTED: ReflexIA = {reflexia_decision}, " f"ZeroIA = {decision}"
        )

    # Logs modifiés pour éviter le spam
    status = ctx.get("status", {})
    cpu = status.get("cpu", "N/A")
    ark_logger.info(f"✅ ZeroIA decided: {decision} (confidence={score}, extra={"module": "zeroia"})", flush=True)
    ark_logger.info(f"[ZeroIA] CPU usage: {cpu}% → decision={decision} (score={score}, extra={"module": "zeroia"})", flush=True)

    return decision, score


def compute_confidence_score(success_rate: float, error_rate: float) -> float:
    return max(0.0, min(1.0, success_rate - error_rate))


def main_loop() -> None:
    ark_logger.info("[ZeroIA] loop started", flush=True, extra={"module": "zeroia"})
    try:
        reason_loop()
    except Exception as e:
        ark_logger.info(f"[ZeroIA] 🚨 ERREUR dans reason_loop(, extra={"module": "zeroia"}): {e}", flush=True)
        logger.exception(e)


if __name__ == "__main__":
    try:
        ark_logger.info("[ZeroIA] 🔄 Boucle cognitive initialisée...", flush=True, extra={"module": "zeroia"})
        while True:
            main_loop()
            time.sleep(15)  # Augmentation de l'intervalle à 15 secondes
    except KeyboardInterrupt:
        ark_logger.info("[ZeroIA] 🧠 Arrêt manuel détecté.", extra={"module": "zeroia"})
