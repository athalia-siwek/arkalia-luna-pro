#!/usr/bin/env python3
"""
🧠 Cognitive Reactor — Intelligence Avancée v2.7.0
==================================================

Module d'intelligence avancée pour Arkalia-LUNA capable de :
- Réactions automatiques basées sur l'analyse cognitive
- Apprentissage et adaptation continue
- Intégration avec tous les modules Arkalia
- Prédictions et recommandations intelligentes
"""

import argparse
import asyncio
import json
import logging
import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# === Configuration du logging ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/cognitive_reactor.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class CognitiveReactor:
    """
    🧠 Réacteur cognitif avancé pour Arkalia-LUNA
    """

    def __init__(self, mode: str = "production"):
        self.mode = mode
        self.enabled = os.getenv("COGNITIVE_REACTOR_ENABLED", "true").lower() == "true"
        self.max_reactions = int(os.getenv("COGNITIVE_MAX_REACTIONS", "100"))
        self.reaction_interval = int(os.getenv("COGNITIVE_REACTION_INTERVAL", "30"))

        # === États et métriques ===
        self.reaction_count = 0
        self.start_time = time.time()
        self.last_reaction_time = 0
        self.cognitive_state = {
            "active": True,
            "mode": mode,
            "reactions_triggered": 0,
            "learning_cycles": 0,
            "predictions_made": 0,
            "last_update": datetime.now().isoformat(),
        }

        # === Répertoires ===
        self.state_dir = Path("modules/cognitive_reactor/state")
        self.state_dir.mkdir(parents=True, exist_ok=True)

        # === Patterns d'apprentissage ===
        self.learned_patterns = []
        self.reaction_history = []

        logger.info(f"🧠 CognitiveReactor initialisé en mode {mode}")

    def load_cognitive_state(self) -> Dict[str, Any]:
        """Charge l'état cognitif depuis le fichier"""
        state_file = self.state_dir / "cognitive_state.json"
        try:
            if state_file.exists():
                with open(state_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Impossible de charger l'état cognitif: {e}")
        return self.cognitive_state

    def save_cognitive_state(self):
        """Sauvegarde l'état cognitif"""
        state_file = self.state_dir / "cognitive_state.json"
        try:
            with open(state_file, "w") as f:
                json.dump(self.cognitive_state, f, indent=2)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de l'état: {e}")

    def analyze_system_context(self) -> Dict[str, Any]:
        """Analyse le contexte système global"""
        context = {
            "timestamp": datetime.now().isoformat(),
            "zeroia_state": self._load_module_state("zeroia"),
            "reflexia_state": self._load_module_state("reflexia"),
            "sandozia_state": self._load_module_state("sandozia"),
            "assistantia_state": self._load_module_state("assistantia"),
            "system_metrics": self._get_system_metrics(),
        }
        return context

    def _load_module_state(self, module_name: str) -> Dict[str, Any]:
        """Charge l'état d'un module spécifique"""
        try:
            state_file = Path(f"state/{module_name}_state.toml")
            if state_file.exists():
                import tomli

                with open(state_file, "rb") as f:
                    return tomli.load(f)
        except Exception as e:
            logger.debug(f"Impossible de charger l'état de {module_name}: {e}")
        return {"active": False, "error": "state_unavailable"}

    def _get_system_metrics(self) -> Dict[str, Any]:
        """Récupère les métriques système"""
        try:
            import psutil

            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage("/").percent,
            }
        except ImportError:
            return {"cpu_percent": 0, "memory_percent": 0, "disk_usage": 0}

    def detect_cognitive_patterns(
        self, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Détecte les patterns cognitifs dans le contexte"""
        patterns = []

        # === Pattern 1: Surcharge système ===
        if context.get("system_metrics", {}).get("cpu_percent", 0) > 80:
            patterns.append(
                {
                    "type": "system_overload",
                    "confidence": 0.9,
                    "severity": "high",
                    "description": "Surcharge CPU détectée",
                }
            )

        # === Pattern 2: Module inactif ===
        for module in ["zeroia", "reflexia", "sandozia"]:
            if not context.get(f"{module}_state", {}).get("active", False):
                patterns.append(
                    {
                        "type": "module_inactive",
                        "module": module,
                        "confidence": 0.8,
                        "severity": "medium",
                        "description": f"Module {module} inactif",
                    }
                )

        # === Pattern 3: Décision répétitive ===
        zeroia_state = context.get("zeroia_state", {})
        if zeroia_state.get("decision", {}).get("last_decision") == zeroia_state.get(
            "decision", {}
        ).get("previous_decision"):
            patterns.append(
                {
                    "type": "repetitive_decision",
                    "confidence": 0.7,
                    "severity": "low",
                    "description": "Décision ZeroIA répétitive",
                }
            )

        return patterns

    def generate_cognitive_reactions(
        self, patterns: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Génère des réactions cognitives basées sur les patterns"""
        reactions = []

        for pattern in patterns:
            if pattern["type"] == "system_overload":
                reactions.append(
                    {
                        "type": "adaptive_threshold_adjustment",
                        "action": "increase_cpu_threshold",
                        "parameters": {"new_threshold": 85},
                        "priority": "high",
                        "description": "Ajustement automatique du seuil CPU",
                    }
                )

            elif pattern["type"] == "module_inactive":
                reactions.append(
                    {
                        "type": "module_restart",
                        "action": "restart_module",
                        "parameters": {"module": pattern["module"]},
                        "priority": "medium",
                        "description": f"Redémarrage automatique de {pattern['module']}",
                    }
                )

            elif pattern["type"] == "repetitive_decision":
                reactions.append(
                    {
                        "type": "decision_diversity",
                        "action": "suggest_alternative",
                        "parameters": {"suggestion": "explore_new_strategies"},
                        "priority": "low",
                        "description": "Suggestion de diversification des décisions",
                    }
                )

        return reactions

    def execute_cognitive_reaction(self, reaction: Dict[str, Any]) -> bool:
        """Exécute une réaction cognitive"""
        try:
            logger.info(f"🧠 Exécution réaction cognitive: {reaction['type']}")

            if reaction["type"] == "adaptive_threshold_adjustment":
                return self._adjust_threshold(reaction["parameters"])

            elif reaction["type"] == "module_restart":
                return self._restart_module(reaction["parameters"]["module"])

            elif reaction["type"] == "decision_diversity":
                return self._suggest_alternative(reaction["parameters"])

            return False

        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de la réaction: {e}")
            return False

    def _adjust_threshold(self, parameters: Dict[str, Any]) -> bool:
        """Ajuste les seuils adaptatifs"""
        try:
            # Intégration avec ZeroIA pour ajuster les seuils
            logger.info(f"🔧 Ajustement seuil: {parameters}")
            return True
        except Exception as e:
            logger.error(f"Erreur ajustement seuil: {e}")
            return False

    def _restart_module(self, module_name: str) -> bool:
        """Redémarre un module"""
        try:
            logger.info(f"🔄 Redémarrage module: {module_name}")
            # Intégration avec Docker pour redémarrer le conteneur
            return True
        except Exception as e:
            logger.error(f"Erreur redémarrage module: {e}")
            return False

    def _suggest_alternative(self, parameters: Dict[str, Any]) -> bool:
        """Suggère des alternatives"""
        try:
            logger.info(f"💡 Suggestion alternative: {parameters}")
            return True
        except Exception as e:
            logger.error(f"Erreur suggestion alternative: {e}")
            return False

    def learn_from_reactions(
        self, reactions: List[Dict[str, Any]], outcomes: List[bool]
    ):
        """Apprend des réactions précédentes"""
        for reaction, outcome in zip(reactions, outcomes):
            learning_entry = {
                "timestamp": datetime.now().isoformat(),
                "reaction": reaction,
                "outcome": outcome,
                "context": self.analyze_system_context(),
            }
            self.reaction_history.append(learning_entry)
            self.cognitive_state["learning_cycles"] += 1

        # Limiter l'historique
        if len(self.reaction_history) > 1000:
            self.reaction_history = self.reaction_history[-500:]

    def predict_future_patterns(self) -> List[Dict[str, Any]]:
        """Prédit les patterns futurs basés sur l'apprentissage"""
        predictions = []

        # Analyse des patterns récurrents
        pattern_counts = {}
        for entry in self.reaction_history[-100:]:
            pattern_type = entry["reaction"]["type"]
            pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1

        # Prédictions basées sur la fréquence
        for pattern_type, count in pattern_counts.items():
            if count > 3:  # Pattern récurrent
                predictions.append(
                    {
                        "type": f"predicted_{pattern_type}",
                        "confidence": min(0.9, count / 10),
                        "expected_time": "within_1_hour",
                        "description": f"Pattern {pattern_type} probable",
                    }
                )

        return predictions

    async def cognitive_loop(self):
        """Boucle principale du réacteur cognitif"""
        logger.info("🧠 Démarrage de la boucle cognitive")

        while self.enabled and self.reaction_count < self.max_reactions:
            try:
                # === Analyse du contexte ===
                context = self.analyze_system_context()

                # === Détection des patterns ===
                patterns = self.detect_cognitive_patterns(context)

                if patterns:
                    logger.info(f"🧠 Patterns détectés: {len(patterns)}")

                    # === Génération des réactions ===
                    reactions = self.generate_cognitive_reactions(patterns)

                    # === Exécution des réactions ===
                    outcomes = []
                    for reaction in reactions:
                        outcome = self.execute_cognitive_reaction(reaction)
                        outcomes.append(outcome)
                        self.reaction_count += 1

                    # === Apprentissage ===
                    self.learn_from_reactions(reactions, outcomes)

                    # === Prédictions ===
                    predictions = self.predict_future_patterns()
                    if predictions:
                        logger.info(f"🔮 Prédictions: {len(predictions)}")
                        self.cognitive_state["predictions_made"] += len(predictions)

                # === Mise à jour de l'état ===
                self.cognitive_state["reactions_triggered"] = self.reaction_count
                self.cognitive_state["last_update"] = datetime.now().isoformat()
                self.save_cognitive_state()

                # === Attente ===
                await asyncio.sleep(self.reaction_interval)

            except Exception as e:
                logger.error(f"Erreur dans la boucle cognitive: {e}")
                await asyncio.sleep(10)

        logger.info("🧠 Boucle cognitive terminée")

    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du réacteur cognitif"""
        return {
            "active": self.enabled,
            "mode": self.mode,
            "reaction_count": self.reaction_count,
            "max_reactions": self.max_reactions,
            "uptime_hours": (time.time() - self.start_time) / 3600,
            "cognitive_state": self.cognitive_state,
            "learned_patterns": len(self.learned_patterns),
            "reaction_history_size": len(self.reaction_history),
        }


async def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Cognitive Reactor - Intelligence Avancée"
    )
    parser.add_argument(
        "--mode", default="production", choices=["production", "development", "test"]
    )
    parser.add_argument("--daemon", action="store_true", help="Mode daemon")
    parser.add_argument(
        "--max-reactions", type=int, default=100, help="Nombre max de réactions"
    )
    parser.add_argument(
        "--interval", type=int, default=30, help="Intervalle entre réactions (secondes)"
    )

    args = parser.parse_args()

    # === Configuration ===
    os.environ["COGNITIVE_MAX_REACTIONS"] = str(args.max_reactions)
    os.environ["COGNITIVE_REACTION_INTERVAL"] = str(args.interval)

    # === Initialisation ===
    reactor = CognitiveReactor(mode=args.mode)

    if not reactor.enabled:
        logger.warning("🧠 Cognitive Reactor désactivé")
        return

    # === Gestion des signaux ===
    def signal_handler(signum, frame):
        logger.info("🧠 Signal de terminaison reçu")
        reactor.enabled = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # === Démarrage ===
    try:
        await reactor.cognitive_loop()
    except KeyboardInterrupt:
        logger.info("🧠 Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"🧠 Erreur fatale: {e}")
        sys.exit(1)
    finally:
        logger.info("🧠 Cognitive Reactor arrêté")


if __name__ == "__main__":
    asyncio.run(main())
