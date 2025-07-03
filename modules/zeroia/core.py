#!/usr/bin/env python3
"""
🧠 modules/zeroia/core.py
ZeroIA Core - Point d'entrée principal du système de raisonnement

Module core simplifié qui délègue aux composants enhanced spécialisés.
"""

import asyncio
import json
import logging
import os
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import toml
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
from pydantic import BaseModel

from .circuit_breaker import CircuitBreaker
from .reason_loop_enhanced import (
    initialize_components_with_recovery,
    reason_loop_enhanced_with_recovery,
)

print("🚨 DEBUT core.py")

# Métriques Prometheus locales pour ZeroIA
zeroia_decisions_total = Counter(
    "zeroia_decisions_total",
    "Nombre total de décisions ZeroIA",
    ["decision_type", "confidence_level"],
)

zeroia_confidence_score = Gauge(
    "zeroia_confidence_score", "Score de confiance de la dernière décision ZeroIA"
)

logger = logging.getLogger(__name__)

# === ROUTER ZEROIA ===
router = APIRouter(tags=["ZeroIA"])


# === CORE ZEROIA ===
class ZeroIACore:
    """🧠 Core ZeroIA - Système de décision intelligent"""

    def __init__(self):
        print("🧠 ZeroIACore __init__ appelé")
        self.circuit_breaker = CircuitBreaker()
        self.state_path = Path("state/zeroia_state.toml")
        self.dashboard_path = Path("state/zeroia_dashboard.json")
        self.reason_loop = reason_loop_enhanced_with_recovery
        self._ensure_state_files()
        self._load_state()

    def _ensure_state_files(self):
        self.state_path.parent.mkdir(exist_ok=True)
        if not self.state_path.exists():
            initial_state: dict[str, Any] = {
                "last_decision": "unknown",
                "confidence_score": 0.0,
                "reasoning_loop_active": False,
                "circuit_breaker_state": "closed",
                "last_update": datetime.now().isoformat(),
            }
            with open(self.state_path, "w") as f:
                toml.dump(initial_state, f)
        if not self.dashboard_path.exists():
            initial_dashboard: dict[str, Any] = {
                "last_decision": "unknown",
                "confidence": 0.0,
                "reasoning_loop_active": False,
                "circuit_breaker_status": "closed",
                "last_update": datetime.now().isoformat(),
            }
            with open(self.dashboard_path, "w") as f:
                json.dump(initial_dashboard, f, indent=2)

    def _load_state(self):
        try:
            if self.state_path.exists():
                self.state = toml.load(self.state_path)
            else:
                self.state = {}
        except Exception as e:
            logger.error(f"Erreur chargement état ZeroIA: {e}")
            self.state = {}

    def _save_state(self):
        try:
            with open(self.state_path, "w") as f:
                toml.dump(self.state, f)
            dashboard_data: dict[str, Any] = {
                "last_decision": self.state.get("last_decision", "unknown"),
                "confidence": self.state.get("confidence_score", 0.0),
                "reasoning_loop_active": self.state.get("reasoning_loop_active", False),
                "circuit_breaker_status": self.state.get("circuit_breaker_state", "closed"),
                "last_update": datetime.now().isoformat(),
            }
            with open(self.dashboard_path, "w") as f:
                json.dump(dashboard_data, f, indent=2)
        except Exception as e:
            logger.error(f"Erreur sauvegarde état ZeroIA: {e}")

    def make_decision(self, context: str) -> dict[str, Any]:
        print("🧪 make_decision déclaré")
        try:
            if not self.circuit_breaker.allow_request():
                logger.warning("Circuit breaker ouvert - décision différée")
                return {"decision": "deferred", "confidence": 0.0, "reason": "circuit_breaker_open"}
            start_time = time.time()
            # Appel direct de la fonction reason_loop avec un contexte par défaut
            decision, confidence = self.reason_loop()
            duration = time.time() - start_time
            decision_result = {"decision": decision, "confidence": confidence}
            zeroia_decisions_total.labels(decision_type=decision, confidence_level=confidence).inc()
            zeroia_confidence_score.set(confidence)
            self.state.update(
                {
                    "last_decision": decision,
                    "confidence_score": confidence,
                    "reasoning_loop_active": True,
                    "circuit_breaker_state": self.circuit_breaker.state,
                    "last_update": datetime.now().isoformat(),
                }
            )
            self._save_state()
            self.circuit_breaker.record_success()
            return decision_result
        except Exception as e:
            logger.error(f"Erreur décision ZeroIA: {e}")
            self.circuit_breaker.record_failure()
            zeroia_decisions_total.labels(decision_type="error", confidence_level="high").inc()
            return {"decision": "error", "confidence": 0.0, "reason": str(e)}

    def get_status(self) -> dict[str, Any]:
        return {
            "status": "active",
            "last_decision": self.state.get("last_decision", "unknown"),
            "confidence": self.state.get("confidence_score", 0.0),
            "circuit_breaker": self.circuit_breaker.state,
            "reasoning_loop_active": self.state.get("reasoning_loop_active", False),
            "last_update": self.state.get("last_update", "unknown"),
        }


# Chargement du core dans un bloc sécurisé
try:
    zeroia_core: ZeroIACore | None = ZeroIACore()
    print("✅ ZeroIA core initialisé")
except Exception as e:
    print("❌ Erreur init ZeroIA Core")
    traceback.print_exc()
    zeroia_core = None  # pour éviter un crash si utilisé plus bas


# === ROUTES ===
@router.get("/status")
async def get_zeroia_status():
    if zeroia_core is None:
        return {"error": "core not available"}
    return zeroia_core.get_status()


class DecisionRequest(BaseModel):
    context: str


@router.post("/decision")
async def make_decision(request: DecisionRequest):
    if zeroia_core is None:
        return {"error": "core not available"}
    result = zeroia_core.make_decision(request.context)
    return result


@router.get("/dummy-check")
def dummy_check():
    return {"status": "router loaded"}


# Instance globale (singleton pattern simple)
_zeroia_core_instance: ZeroIACore | None = None


def get_zeroia_core() -> ZeroIACore:
    """
    Retourne l'instance singleton de ZeroIA Core

    Returns:
        ZeroIACore: Instance du core
    """
    global _zeroia_core_instance

    if _zeroia_core_instance is None:
        _zeroia_core_instance = ZeroIACore()

    return _zeroia_core_instance


def quick_decision(context_path: Path | None = None) -> tuple[str, float]:
    """
    Interface rapide pour une décision ZeroIA

    Args:
        context_path: Chemin vers le contexte (optionnel)

    Returns:
        tuple[str, float]: (décision, score_confiance)
    """
    core = get_zeroia_core()

    # if not core.initialized:
    #     core.initialize()

    # return core.run_decision_cycle(context_path)
    # Fonctionnalité désactivée : méthodes non définies dans ZeroIACore
    return ("not_implemented", 0.0)


def health_check() -> dict[str, Any]:
    """
    Vérifie l'état de santé du core ZeroIA

    Returns:
        Dict: État de santé détaillé
    """
    try:
        core = get_zeroia_core()
        return core.get_status()
    except Exception as e:
        return {"status": "critical_error", "error": str(e), "initialized": False}


# === LOG DES ROUTES ===
for route in router.routes:
    print(
        f"🛣️ Route enregistrée : {getattr(route, 'path', 'unknown')} [{getattr(route, 'name', 'unknown')}]"
    )

if __name__ == "__main__":
    # Test rapide du core
    print("🧠 ZeroIA Core - Test de démarrage")

    core = get_zeroia_core()

    # if core.initialize():
    #     print("✅ Initialisation réussie")
    #     decision, confidence = core.run_decision_cycle()
    #     print(f"🎯 Décision: {decision} (confiance: {confidence:.2f})")
    #     status = core.get_status()
    #     print(f"📊 État: {status['status']}")
    # else:
    #     print("❌ Échec initialisation")
    print("[DEMO] Fonctions avancées désactivées (initialize/run_decision_cycle)")
