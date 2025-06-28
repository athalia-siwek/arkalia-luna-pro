#!/usr/bin/env python3
# 🔄 modules/zeroia/reason_loop_enhanced.py
# Version améliorée avec Circuit Breaker et Event Sourcing

"""
Reason Loop Enhanced pour ZeroIA - Version Enterprise

Améliorations v3.x :
- Circuit Breaker pour protection cascade failures
- Event Sourcing complet des décisions
- Gestion d'erreurs avancée avec types spécialisés
- Métriques détaillées et monitoring
- Recovery automatique et graceful degradation
"""

import logging
import textwrap
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import toml

from modules.zeroia.adaptive_thresholds import should_lower_cpu_threshold
from modules.zeroia.circuit_breaker import (
    CircuitBreaker,
    CognitiveOverloadError,
    DecisionIntegrityError,
    SystemRebootRequired,
)
from modules.zeroia.event_store import EventStore, EventType
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
MIN_DECISION_INTERVAL = 30  # seconds

# === Instances globales Circuit Breaker et Event Store ===
circuit_breaker: Optional[CircuitBreaker] = None
event_store: Optional[EventStore] = None

logger = logging.getLogger(__name__)


def initialize_components() -> Tuple[CircuitBreaker, EventStore]:
    """Initialise les composants Circuit Breaker et Event Store"""
    global circuit_breaker, event_store
    
    if circuit_breaker is None:
        # Event Store d'abord
        event_store = EventStore()
        
        # Circuit Breaker avec Event Store intégré
        circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60,
            expected_exception=(CognitiveOverloadError, DecisionIntegrityError),
            event_store=event_store
        )
        
        logger.info("🔄 Circuit Breaker et Event Store initialisés")
        
        # Event pour initialisation
        event_store.add_event(
            EventType.STATE_CHANGE,
            {
                "component": "reason_loop_enhanced",
                "action": "initialized",
                "circuit_breaker_config": circuit_breaker.get_status()["config"]
            }
        )
    
    return circuit_breaker, event_store


def load_toml(path: Path) -> dict:
    """Charge un fichier TOML avec gestion d'erreurs robuste"""
    try:
        if not path.exists() or not path.read_text().strip():
            raise ValueError(f"TOML file {path} is empty or missing")
        return toml.load(path)
    except toml.TomlDecodeError as e:
        raise DecisionIntegrityError(f"[TOML] Format invalide dans {path}: {e}")
    except Exception as e:
        raise CognitiveOverloadError(f"[TOML] Erreur lors du chargement de {path}: {e}")


def load_context(path: Path = CTX_PATH) -> dict:
    """Charge le contexte global avec protection circuit breaker"""
    cb, es = initialize_components()
    return cb.call(load_toml, path)


def load_reflexia_state(path: Path = REFLEXIA_STATE) -> dict:
    """Charge l'état ReflexIA avec protection circuit breaker"""
    cb, es = initialize_components()
    return cb.call(load_toml, path)


def decide_protected(context: dict) -> Tuple[str, float]:
    """
    Fonction de décision protégée par circuit breaker
    
    Args:
        context: Contexte système
        
    Returns:
        Tuple (décision, score de confiance)
        
    Raises:
        CognitiveOverloadError: Si surcharge détectée
        DecisionIntegrityError: Si intégrité compromise
    """
    status = context.get("status", {})
    severity = status.get("severity", "none")
    cpu = status.get("cpu", 0)
    
    # Validation des données d'entrée
    if not isinstance(cpu, (int, float)) or cpu < 0 or cpu > 100:
        raise DecisionIntegrityError(f"CPU invalide: {cpu} (doit être 0-100)")
    
    if severity not in ["none", "low", "medium", "high", "critical"]:
        raise DecisionIntegrityError(f"Severity invalide: {severity}")
    
    # Détection de surcharge cognitive
    if cpu > 95:
        raise CognitiveOverloadError(f"CPU critique: {cpu}% - système surchargé")
    
    # Logique de décision avec seuils adaptatifs
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
    """Assure que le répertoire parent existe"""
    target = path.parent if path.suffix else path
    target.mkdir(parents=True, exist_ok=True)


def persist_state_enhanced(
    decision: str,
    score: float,
    ctx: dict,
    state_path_override: Optional[Path] = None,
) -> None:
    """Persistance d'état avec event sourcing"""
    reflexia_summary = ctx.get("reflexia", {})
    status = ctx.get("status", {})
    cpu = status.get("cpu", "N/A")
    severity = status.get("severity", "none")
    
    state_path = state_path_override or STATE_PATH
    ensure_parent_dir(state_path)
    save_backup()
    
    # Sauvegarder l'état
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
    
    # Event sourcing de la décision
    _, es = initialize_components()
    es.add_event(
        EventType.DECISION_MADE,
        {
            "decision": decision,
            "confidence": score,
            "cpu": cpu,
            "severity": severity,
            "reflexia_summary": reflexia_summary,
            "justification": f"cpu={cpu}, severity={severity}"
        }
    )
    
    # Log traditionnel
    ensure_parent_dir(LOG_PATH)
    with open(LOG_PATH, "a") as f:
        f.write(
            f"{datetime.now()} :: FROM REFLEXIA: {reflexia_summary} | "
            f"CPU={cpu} | SEVERITY={severity} → DECISION = "
            f"{decision} (confidence={score})\n"
        )


def update_dashboard_enhanced(
    decision: str,
    score: float,
    ctx: dict,
    dashboard_path_override: Optional[Path] = None,
) -> None:
    """Mise à jour dashboard avec métriques circuit breaker"""
    dashboard_path = dashboard_path_override or DASHBOARD_PATH
    ensure_parent_dir(dashboard_path)
    
    cb, es = initialize_components()
    
    # Récupérer les métriques du circuit breaker
    cb_status = cb.get_status()
    
    # Récupérer analytics des événements
    analytics = es.get_analytics()
    
    dashboard_data = {
        "last_decision": decision,
        "confidence": score,
        "reasoning_loop_active": True,
        "connected_modules": ["reflexia"],
        "previous": ["reduce_load", "monitor", "monitor"],
        "last_updated": datetime.now().isoformat(),
        "circuit_breaker": {
            "state": cb_status["state"],
            "failure_rate": cb_status["metrics"]["failure_rate"],
            "success_rate": cb_status["metrics"]["success_rate"],
            "consecutive_failures": cb_status["metrics"]["consecutive_failures"]
        },
        "event_analytics": {
            "total_events": analytics["total_events"],
            "recent_events": analytics["recent_events_analyzed"],
            "events_by_type": analytics["events_by_type"]
        }
    }
    
    save_json_if_changed(dashboard_data, str(dashboard_path))


def check_for_ia_conflict_enhanced(
    reflexia_decision: str,
    zeroia_decision: str,
    log_path: Path,
) -> bool:
    """Détection de conflit IA avec event sourcing"""
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
        
        # Event sourcing de la contradiction
        _, es = initialize_components()
        es.add_event(
            EventType.CONTRADICTION_DETECTED,
            {
                "reflexia_decision": reflexia_decision,
                "zeroia_decision": zeroia_decision,
                "severity": "medium"
            }
        )
        
        return True
    return False


def reason_loop_enhanced(
    context_path: Optional[Path] = None,
    reflexia_path: Optional[Path] = None,
    state_path: Optional[Path] = None,
    dashboard_path: Optional[Path] = None,
    log_path: Optional[Path] = None,
    contradiction_log_path: Optional[Path] = None,
) -> Tuple[str, float]:
    """
    Boucle de raisonnement améliorée avec circuit breaker et event sourcing
    
    Returns:
        Tuple (décision, score de confiance)
        
    Raises:
        SystemRebootRequired: Si système nécessite redémarrage
        CognitiveOverloadError: Si surcharge cognitive
    """
    cb, es = initialize_components()
    
    try:
        # Charger les données avec protection circuit breaker
        ctx = load_context(context_path or CTX_PATH)
        reflexia_data = load_reflexia_state(reflexia_path or REFLEXIA_STATE)
        
        # 🛡️ ROBUSTESSE v3.x - Valeurs par défaut si CPU/RAM manquants
        status = ctx.get("status", {})
        if "cpu" not in status or "ram" not in status:
            print("⚠️ [ZeroIA] CPU/RAM missing in context, using defaults", flush=True)
            ctx["status"] = {
                "cpu": status.get("cpu", 45),
                "ram": status.get("ram", 62),
                "severity": status.get("severity", "normal"),
                "disk_usage": status.get("disk_usage", 78),
                "network_latency": status.get("network_latency", 25),
            }
        
        # Décision protégée par circuit breaker
        decision, score = cb.call(decide_protected, ctx)
        
        # 🛡️ VALIDATION INTÉGRITÉ MODÈLE
        try:
            integrity_valid, integrity_reason = validate_decision_integrity(
                ctx, decision, score
            )
            if not integrity_valid:
                print(f"🚨 [ZeroIA] INTEGRITY VIOLATION: {integrity_reason}", flush=True)
                
                # Event sourcing de la violation
                es.add_event(
                    EventType.SYSTEM_ERROR,
                    {
                        "error_type": "integrity_violation",
                        "reason": integrity_reason,
                        "original_decision": decision,
                        "fallback_decision": "monitor"
                    }
                )
                
                # Forcer décision sécurisée
                decision, score = "monitor", 0.3
                
        except Exception as e:
            print(f"⚠️ [ZeroIA] Integrity check failed: {e}", flush=True)
            
            # Event sourcing de l'erreur
            es.add_event(
                EventType.SYSTEM_ERROR,
                {
                    "error_type": "integrity_check_failure",
                    "error": str(e),
                    "decision": decision
                }
            )
        
        # Vérifie si on doit traiter cette décision (anti-spam)
        if not should_process_decision(decision):
            print(
                f"[ZeroIA] Décision {decision} ignorée (répétition trop fréquente)",
                flush=True,
            )
            return decision, score
        
        # Persistance avec event sourcing
        persist_state_enhanced(decision, score, ctx, state_path)
        update_dashboard_enhanced(decision, score, ctx, dashboard_path)
        
        # Vérification contradictions
        reflexia_decision = reflexia_data.get("decision", {}).get(
            "last_decision", "unknown"
        )
        if check_for_ia_conflict_enhanced(
            reflexia_decision,
            decision,
            log_path=contradiction_log_path or Path(DEFAULT_CONTRADICTION_LOG),
        ):
            logger.warning(
                f"CONTRADICTION DETECTED: ReflexIA = {reflexia_decision}, "
                f"ZeroIA = {decision}"
            )
        
        # Logs améliorés
        status = ctx.get("status", {})
        cpu = status.get("cpu", "N/A")
        print(f"✅ ZeroIA decided: {decision} (confidence={score})", flush=True)
        print(f"[ZeroIA] CPU usage: {cpu}% → decision={decision} (score={score})", flush=True)
        
        return decision, score
        
    except SystemRebootRequired:
        # Propagation pour gestion niveau supérieur
        raise
    except (CognitiveOverloadError, DecisionIntegrityError) as e:
        # Erreurs gérées par le circuit breaker
        logger.error(f"🚨 [ZeroIA] Erreur gérée: {e}")
        
        # Décision de sécurité en cas d'erreur
        fallback_decision, fallback_score = "monitor", 0.1
        
        # Event sourcing de la récupération
        es.add_event(
            EventType.SYSTEM_ERROR,
            {
                "error_type": type(e).__name__,
                "error": str(e),
                "fallback_decision": fallback_decision,
                "fallback_score": fallback_score
            }
        )
        
        return fallback_decision, fallback_score
    
    except Exception as e:
        # Erreur inattendue - event sourcing critique
        logger.error(f"💥 [ZeroIA] Erreur critique: {e}")
        
        es.add_event(
            EventType.SYSTEM_ERROR,
            {
                "error_type": "unexpected_error",
                "error": str(e),
                "severity": "critical"
            }
        )
        
        # Reraise pour gestion niveau supérieur
        raise CognitiveOverloadError(f"Erreur critique dans reason_loop: {e}") from e


def main_loop_enhanced() -> None:
    """Boucle principale améliorée avec gestion d'erreurs robuste"""
    print("[ZeroIA Enhanced] loop started", flush=True)
    
    cb, es = initialize_components()
    
    try:
        decision, score = reason_loop_enhanced()
        
        # Event sourcing de succès
        es.add_event(
            EventType.CIRCUIT_SUCCESS,
            {
                "decision": decision,
                "confidence": score,
                "loop_iteration": "successful"
            }
        )
        
    except SystemRebootRequired as e:
        print(f"[ZeroIA Enhanced] 🔄 REDÉMARRAGE REQUIS: {e}", flush=True)
        
        # Event sourcing critique
        es.add_event(
            EventType.SYSTEM_ERROR,
            {
                "error_type": "reboot_required",
                "error": str(e),
                "severity": "critical",
                "action_required": "system_restart"
            }
        )
        
        # Attendre avant retry
        time.sleep(60)
        
    except (CognitiveOverloadError, DecisionIntegrityError) as e:
        print(f"[ZeroIA Enhanced] ⚠️ SURCHARGE: {e}", flush=True)
        
        # Graceful degradation
        time.sleep(30)
        
    except Exception as e:
        print(f"[ZeroIA Enhanced] 🚨 ERREUR: {e}", flush=True)
        logger.exception(e)
        
        # Event sourcing d'erreur
        es.add_event(
            EventType.SYSTEM_ERROR,
            {
                "error_type": "main_loop_error",
                "error": str(e),
                "severity": "high"
            }
        )


def get_circuit_status() -> dict:
    """Retourne le statut du circuit breaker"""
    cb, es = initialize_components()
    return cb.get_status()


def get_event_analytics() -> dict:
    """Retourne les analytics des événements"""
    cb, es = initialize_components()
    return es.get_analytics()


def reset_circuit_breaker() -> None:
    """Réinitialise manuellement le circuit breaker"""
    cb, es = initialize_components()
    cb.reset()
    print("🔄 Circuit breaker réinitialisé manuellement")


if __name__ == "__main__":
    try:
        print("[ZeroIA Enhanced] 🔄 Boucle cognitive initialisée avec protection...", flush=True)
        
        # Initialiser les composants
        initialize_components()
        
        while True:
            main_loop_enhanced()
            time.sleep(15)  # Intervalle de 15 secondes
            
    except KeyboardInterrupt:
        print("[ZeroIA Enhanced] 🧠 Arrêt manuel détecté.")
        
        # Event sourcing de l'arrêt
        _, es = initialize_components()
        es.add_event(
            EventType.STATE_CHANGE,
            {
                "action": "manual_shutdown",
                "reason": "keyboard_interrupt"
            }
        ) 