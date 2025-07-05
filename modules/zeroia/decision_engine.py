#!/usr/bin/env python3
"""
🧠 Decision Engine - Moteur de décision pour ZeroIA

Extrait de reason_loop_enhanced.py pour simplifier la maintenance.
Responsabilité : Analyse du contexte et prise de décision.
"""

import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Tuple

import toml

from modules.zeroia.metrics import update_zeroia_metrics

logger = logging.getLogger(__name__)

# === Chemins par défaut ===
CTX_PATH = Path("state/global_context.toml")
REFLEXIA_STATE = Path("state/reflexia_state.toml")


class DecisionEngine:
    """Moteur de décision principal pour ZeroIA"""
    
    def __init__(self):
        self.last_decision = None
        self.last_decision_time = None
        self.min_decision_interval = 30  # seconds
        
    def create_default_context_enhanced(self) -> dict:
        """
        Crée un contexte par défaut enterprise pour éviter les warnings CPU/RAM.
        Optimisé pour containers Docker avec tous les modules Arkalia.
        """
        current_time = datetime.now().isoformat()
        return {
            "last_update": current_time,
            "system_status": "operational",
            "active_modules": [
                "reflexia", "zeroia", "assistantia", "sandozia", 
                "helloria", "taskia", "nyxalia"
            ],
            "version": "3.0.0-enhanced",
            "status": {
                "cpu": 45.2,  # CPU par défaut : 45% (charge normale container)
                "ram": 62.8,  # RAM par défaut : 62% (charge normale container)
                "severity": "normal",
                "disk_usage": 78,
                "network_latency": 25,
                "load_avg": 1.2,
                "active_processes": 150,
                "container_health": "healthy",
            },
            "reflexia": {
                "status": "operational",
                "last_check": current_time,
                "module_active": True,
                "last_decision": "normal",
                "confidence": 0.85,
                "cycle_count": 626,
            },
            "modules": {
                "sandozia": {
                    "status": "active",
                    "intelligence_level": "adaptive",
                    "health": "healthy",
                },
                "assistantia": {
                    "status": "active",
                    "response_time": "optimal",
                    "health": "healthy",
                    "port": 8001,
                },
                "helloria": {"status": "active", "api_ready": True, "health": "healthy"},
                "nyxalia": {
                    "status": "active",
                    "monitoring": "enabled",
                    "health": "healthy",
                },
                "taskia": {"status": "active", "queue_size": 0, "health": "healthy"},
                "zeroia": {
                    "status": "active",
                    "reason_loop": "enhanced",
                    "health": "healthy",
                    "circuit_breaker": "closed",
                },
            },
            "metadata": {
                "initialized": current_time,
                "version": "3.0.0-enhanced",
                "source": "arkalia_global_context_v3",
                "container": "arkalia-luna-system",
                "environment": "production",
                "docker_compose": True,
            },
        }
    
    def load_context(self, path: Path = CTX_PATH) -> dict:
        """Charge le contexte global"""
        try:
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    return toml.load(f)
            else:
                logger.warning(f"Contexte non trouvé: {path}, création par défaut")
                return self.create_default_context_enhanced()
        except Exception as e:
            logger.error(f"Erreur chargement contexte: {e}")
            return self.create_default_context_enhanced()
    
    def load_reflexia_state(self, path: Path = REFLEXIA_STATE) -> dict:
        """Charge l'état Reflexia"""
        try:
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    return toml.load(f)
            else:
                logger.warning(f"État Reflexia non trouvé: {path}")
                return {"status": "unknown", "last_decision": "unknown"}
        except Exception as e:
            logger.error(f"Erreur chargement Reflexia: {e}")
            return {"status": "error", "last_decision": "error"}
    
    def analyze_context(self, context: dict) -> dict:
        """Analyse le contexte et extrait les métriques importantes"""
        status = context.get("status", {})
        reflexia = context.get("reflexia", {})
        
        return {
            "cpu": status.get("cpu", 50.0),
            "ram": status.get("ram", 60.0),
            "severity": status.get("severity", "normal"),
            "reflexia_decision": reflexia.get("last_decision", "unknown"),
            "reflexia_confidence": reflexia.get("confidence", 0.5),
            "system_status": context.get("system_status", "unknown"),
        }
    
    def generate_decision(self, analysis: dict) -> Tuple[str, float]:
        """
        Génère une décision basée sur l'analyse du contexte
        
        Returns:
            Tuple[str, float]: (décision, score_de_confiance)
        """
        start_time = time.time()
        
        try:
            cpu = analysis["cpu"]
            ram = analysis["ram"]
            severity = analysis["severity"]
            reflexia_decision = analysis["reflexia_decision"]
            
            # Logique de décision simplifiée
            if cpu > 80 or ram > 85:
                decision = "critical"
                score = 0.95
            elif cpu > 70 or ram > 75:
                decision = "warning"
                score = 0.85
            elif severity == "high":
                decision = "attention"
                score = 0.75
            elif reflexia_decision == "critical":
                decision = "sync_critical"
                score = 0.90
            else:
                decision = "normal"
                score = 0.70
            
            # Vérifier si on doit baisser le seuil CPU
            if should_lower_cpu_threshold():
                decision = "optimize_cpu"
                score = 0.80
            
            # Mettre à jour les métriques
            duration = time.time() - start_time
            update_zeroia_metrics("context_analysis", "success", duration, cognitive_score=score)
            
            return decision, score
            
        except Exception as e:
            logger.error(f"Erreur génération décision: {e}")
            duration = time.time() - start_time
            update_zeroia_metrics("context_analysis", "error", duration)
            return "error", 0.0
    
    def validate_decision(self, decision: str, score: float) -> bool:
        """Valide une décision"""
        if not decision or decision == "error":
            return False
        
        if score < 0.0 or score > 1.0:
            return False
        
        valid_decisions = [
            "normal", "warning", "critical", "attention", 
            "sync_critical", "optimize_cpu", "error"
        ]
        
        return decision in valid_decisions
    
    def should_process_decision(self, new_decision: str) -> bool:
        """Vérifie si on doit traiter cette décision (anti-répétition)"""
        current_time = time.time()
        
        # Première décision
        if self.last_decision is None:
            self.last_decision = new_decision
            self.last_decision_time = current_time
            return True
        
        # Même décision récente
        if (new_decision == self.last_decision and 
            self.last_decision_time is not None and
            current_time - self.last_decision_time < self.min_decision_interval):
            return False
        
        # Nouvelle décision ou temps écoulé
        self.last_decision = new_decision
        self.last_decision_time = current_time
        return True
    
    def decide_protected(self, context: dict) -> Tuple[str, float]:
        """
        Prise de décision protégée avec gestion d'erreurs
        
        Returns:
            Tuple[str, float]: (décision, score_de_confiance)
        """
        try:
            # Analyser le contexte
            analysis = self.analyze_context(context)
            
            # Générer la décision
            decision, score = self.generate_decision(analysis)
            
            # Valider la décision
            if not self.validate_decision(decision, score):
                logger.warning(f"Décision invalide: {decision} (score: {score})")
                return "error", 0.0
            
            # Vérifier si on doit traiter
            if not self.should_process_decision(decision):
                logger.debug(f"Décision ignorée (répétition): {decision}")
                return decision, score
            
            logger.info(f"✅ Décision prise: {decision} (score: {score:.2f})")
            return decision, score
            
        except Exception as e:
            logger.error(f"❌ Erreur prise de décision: {e}")
            update_zeroia_metrics("decision_making", "error", 0.0)
            return "error", 0.0

def should_lower_cpu_threshold() -> bool:
    """
    Détermine si le seuil CPU doit être abaissé (logique simple, à adapter selon besoins).
    Ici, on retourne False par défaut (comportement safe).
    """
    # Logique simple : on pourrait lire une config, un état système, etc.
    return False 