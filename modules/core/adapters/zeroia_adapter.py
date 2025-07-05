#!/usr/bin/env python3
"""
🔗 ZeroIA Adapter - Adaptateur SOLID pour ZeroIA
🎯 Interface entre ZeroIA existant et l'architecture SOLID
"""

import logging
from typing import Any

from ..interfaces.module_interface import IModule, IModuleWithProcessing

logger = logging.getLogger(__name__)


class ZeroIAAdapter(IModuleWithProcessing):
    """
    🔗 Adaptateur SOLID pour ZeroIA
    🎯 Interface entre ZeroIA existant et l'architecture SOLID
    """

    def __init__(self):
        self.name = "zeroia"
        self.version = "1.0.0"
        self.enabled = False
        self._zeroia_core = None
        self._initialized = False

        # Statistiques de traitement
        self._processing_stats = {
            "total_decisions": 0,
            "successful_decisions": 0,
            "failed_decisions": 0,
            "average_confidence": 0.0,
            "last_decision": None,
        }

    def initialize(self) -> bool:
        """Initialise l'adaptateur ZeroIA"""
        try:
            logger.info("🔗 Initialisation ZeroIA Adapter...")

            # Import dynamique pour éviter les dépendances circulaires
            from modules.zeroia.core import get_zeroia_core

            self._zeroia_core = get_zeroia_core()

            if self._zeroia_core is None:
                logger.error("❌ Impossible d'obtenir l'instance ZeroIA Core")
                return False

            self.enabled = True
            self._initialized = True

            logger.info("✅ ZeroIA Adapter initialisé avec succès")
            return True

        except Exception as e:
            logger.error(f"❌ Erreur initialisation ZeroIA Adapter: {e}")
            return False

    def health_check(self) -> dict[str, Any]:
        """Vérification de santé de ZeroIA"""
        try:
            if not self._initialized or self._zeroia_core is None:
                return {
                    "status": "error",
                    "message": "ZeroIA Adapter non initialisé",
                    "module": self.name,
                }

            # Récupérer le statut depuis ZeroIA Core
            status = self._zeroia_core.get_status()

            # Enrichir avec les métriques de l'adaptateur
            health_data = {
                "status": "ok" if status.get("status") == "active" else "degraded",
                "module": self.name,
                "version": self.version,
                "enabled": self.enabled,
                "zeroia_status": status,
                "processing_stats": self._processing_stats,
                "circuit_breaker": status.get("circuit_breaker", "unknown"),
                "last_decision": status.get("last_decision", "unknown"),
                "confidence": status.get("confidence", 0.0),
            }

            return health_data

        except Exception as e:
            logger.error(f"❌ Erreur health check ZeroIA Adapter: {e}")
            return {
                "status": "error",
                "message": str(e),
                "module": self.name,
            }

    def get_name(self) -> str:
        """Nom du module"""
        return self.name

    def get_version(self) -> str:
        """Version du module"""
        return self.version

    def is_enabled(self) -> bool:
        """État d'activation du module"""
        return self.enabled

    def shutdown(self) -> bool:
        """Arrêt propre du module"""
        try:
            logger.info("🛑 Shutdown ZeroIA Adapter...")

            # Sauvegarder l'état final si nécessaire
            if self._zeroia_core is not None:
                # ZeroIA sauvegarde automatiquement son état
                pass

            self.enabled = False
            self._initialized = False

            logger.info("✅ ZeroIA Adapter shutdown complet")
            return True

        except Exception as e:
            logger.error(f"❌ Erreur shutdown ZeroIA Adapter: {e}")
            return False

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        """Traitement de données via ZeroIA"""
        try:
            if not self._initialized or self._zeroia_core is None:
                return {
                    "status": "error",
                    "message": "ZeroIA Adapter non initialisé",
                    "decision": "error",
                    "confidence": 0.0,
                }

            # Extraire le contexte des données
            context = data.get("context", "")
            if not context:
                context = "default_context"

            # Appeler ZeroIA pour une décision
            result = self._zeroia_core.make_decision(context)

            # Mettre à jour les statistiques
            self._update_processing_stats(result)

            # Enrichir le résultat
            processed_result = {
                "status": "success",
                "module": self.name,
                "decision": result.get("decision", "unknown"),
                "confidence": result.get("confidence", 0.0),
                "reason": result.get("reason", ""),
                "processing_stats": self._processing_stats,
            }

            logger.info(
                f"✅ ZeroIA decision: {result.get('decision')} (confidence: {result.get('confidence')})"
            )
            return processed_result

        except Exception as e:
            logger.error(f"❌ Erreur traitement ZeroIA: {e}")

            # Mettre à jour les statistiques d'erreur
            self._processing_stats["failed_decisions"] += 1
            self._processing_stats["total_decisions"] += 1

            return {
                "status": "error",
                "message": str(e),
                "decision": "error",
                "confidence": 0.0,
                "module": self.name,
            }

    def get_processing_stats(self) -> dict[str, Any]:
        """Statistiques de traitement"""
        return {
            "module": self.name,
            "total_decisions": self._processing_stats["total_decisions"],
            "successful_decisions": self._processing_stats["successful_decisions"],
            "failed_decisions": self._processing_stats["failed_decisions"],
            "success_rate": (
                self._processing_stats["successful_decisions"]
                / self._processing_stats["total_decisions"]
                if self._processing_stats["total_decisions"] > 0
                else 0.0
            ),
            "average_confidence": self._processing_stats["average_confidence"],
            "last_decision": self._processing_stats["last_decision"],
        }

    def _update_processing_stats(self, result: dict[str, Any]) -> None:
        """Met à jour les statistiques de traitement"""
        self._processing_stats["total_decisions"] += 1

        decision = result.get("decision", "unknown")
        confidence = result.get("confidence", 0.0)

        if decision != "error":
            self._processing_stats["successful_decisions"] += 1
        else:
            self._processing_stats["failed_decisions"] += 1

        # Mettre à jour la confiance moyenne
        total_successful = self._processing_stats["successful_decisions"]
        if total_successful > 0:
            current_avg = self._processing_stats["average_confidence"]
            new_avg = ((current_avg * (total_successful - 1)) + confidence) / total_successful
            self._processing_stats["average_confidence"] = new_avg

        self._processing_stats["last_decision"] = {
            "decision": decision,
            "confidence": confidence,
            "timestamp": "now",  # En production, utiliser datetime.now().isoformat()
        }

    def make_decision(self, context: str) -> dict[str, Any]:
        """Méthode spécifique pour les décisions ZeroIA"""
        return self.process({"context": context})


# Factory function pour créer l'adaptateur
def create_zeroia_adapter() -> ZeroIAAdapter:
    """Crée une instance de l'adaptateur ZeroIA"""
    return ZeroIAAdapter()
