#!/usr/bin/env python3
"""
🔗 Sandozia Adapter - Adaptateur SOLID pour Sandozia
🎯 Interface entre Sandozia existant et l'architecture SOLID
"""

import asyncio
import logging
import time
from typing import Any, Optional

from ..interfaces.module_interface import IModule, IModuleWithMonitoring, IModuleWithProcessing

logger = logging.getLogger(__name__)


class SandoziaAdapter(IModuleWithProcessing, IModuleWithMonitoring):
    """
    🔗 Adaptateur SOLID pour Sandozia
    🎯 Interface entre Sandozia existant et l'architecture SOLID
    """

    def __init__(self):
        self.name = "sandozia"
        self.version = "1.0.0"
        self.enabled = False
        self._initialized = False
        self._sandozia_core = None
        self._behavior_analyzer = None

        # Statistiques de traitement
        self._processing_stats = {
            "total_analyses": 0,
            "successful_analyses": 0,
            "failed_analyses": 0,
            "average_analysis_time": 0.0,
            "last_analysis": None,
            "patterns_detected": 0,
            "anomalies_found": 0,
        }

        # Métriques de monitoring
        self._metrics = {}
        self._alert_thresholds = {
            "anomaly_threshold": 2.0,
            "pattern_confidence": 0.7,
            "performance_regression": 0.1,
        }

    def initialize(self) -> bool:
        """Initialise l'adaptateur Sandozia"""
        try:
            logger.info("🔗 Initialisation Sandozia Adapter...")

            # Import dynamique pour éviter les dépendances circulaires
            try:
                from modules.sandozia.analyzer.behavior import BehaviorAnalyzer
                from modules.sandozia.core import UsandoziaConfig, UsandoziaCore

                # Initialiser le core Sandozia
                config = UsandoziaConfig()
                self._sandozia_core = UsandoziaCore(config)

                # Initialiser l'analyseur comportemental
                self._behavior_analyzer = BehaviorAnalyzer()

            except ImportError as e:
                logger.error(f"❌ Module Sandozia non disponible: {e}")
                # Essayer d'importer directement depuis le fichier
                try:
                    from modules.sandozia.analyzer.behavior import BehaviorAnalyzer
                    from modules.sandozia.core import UsandoziaConfig, UsandoziaCore

                    config = UsandoziaConfig()
                    self._sandozia_core = UsandoziaCore(config)
                    self._behavior_analyzer = BehaviorAnalyzer()

                except ImportError as e2:
                    logger.error(f"❌ Import direct Sandozia échoué: {e2}")
                    self._sandozia_core = None
                    self._behavior_analyzer = None
                    return False

            self.enabled = True
            self._initialized = True

            logger.info("✅ Sandozia Adapter initialisé avec succès")
            return True

        except Exception as e:
            logger.error(f"❌ Erreur initialisation Sandozia Adapter: {e}")
            return False

    def health_check(self) -> dict[str, Any]:
        """Vérification de santé de Sandozia"""
        try:
            if not self._initialized:
                return {
                    "status": "error",
                    "message": "Sandozia Adapter non initialisé",
                    "module": self.name,
                }

            # Récupérer le health check du core Sandozia
            if self._sandozia_core is None:
                return {
                    "status": "error",
                    "message": "Sandozia Core non disponible",
                    "module": self.name,
                }

            core_health = self._sandozia_core.health_check()

            # Analyser le statut
            status = core_health.get("status", "unknown")
            health_status = "ok" if status == "healthy" else "degraded"

            health_data = {
                "status": health_status,
                "module": self.name,
                "version": self.version,
                "enabled": self.enabled,
                "sandozia_status": status,
                "processing_stats": self._processing_stats,
                "patterns_detected": self._processing_stats["patterns_detected"],
                "anomalies_found": self._processing_stats["anomalies_found"],
                "last_analysis": self._processing_stats["last_analysis"],
            }

            return health_data

        except Exception as e:
            logger.error(f"❌ Erreur health check Sandozia Adapter: {e}")
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
            logger.info("🛑 Shutdown Sandozia Adapter...")

            self.enabled = False
            self._initialized = False

            logger.info("✅ Sandozia Adapter shutdown complet")
            return True

        except Exception as e:
            logger.error(f"❌ Erreur shutdown Sandozia Adapter: {e}")
            return False

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        """Traitement de données via Sandozia"""
        try:
            if not self._initialized:
                return {
                    "status": "error",
                    "message": "Sandozia Adapter non initialisé",
                    "analysis_result": {},
                }

            # Déterminer le type d'analyse
            analysis_type = data.get("analysis_type", "behavior")
            enhanced = data.get("enhanced", False)

            start_time = time.time()

            # Effectuer l'analyse
            if analysis_type == "behavior":
                analysis_result = self._analyze_behavior(data)
            elif analysis_type == "core":
                # Utiliser le core Sandozia
                if self._sandozia_core is None:
                    analysis_result = {"status": "error", "message": "Sandozia Core non disponible"}
                else:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        analysis_result = loop.run_until_complete(self._sandozia_core.process(data))
                    finally:
                        loop.close()
            else:
                analysis_result = {
                    "status": "error",
                    "message": f"Type d'analyse inconnu: {analysis_type}",
                }

            analysis_time = time.time() - start_time

            # Mettre à jour les statistiques
            success = analysis_result.get("status") == "success"
            self._update_processing_stats(analysis_time, success, analysis_result)

            # Enrichir le résultat
            processed_result = {
                "status": "success",
                "module": self.name,
                "analysis_type": analysis_type,
                "enhanced": enhanced,
                "analysis_result": analysis_result,
                "analysis_time": analysis_time,
                "processing_stats": self._processing_stats,
            }

            logger.info(f"✅ Sandozia analysis: {analysis_type} (temps: {analysis_time:.3f}s)")
            return processed_result

        except Exception as e:
            logger.error(f"❌ Erreur traitement Sandozia: {e}")

            # Mettre à jour les statistiques d'erreur
            self._update_processing_stats(0.0, False, {"status": "error", "message": str(e)})

            return {
                "status": "error",
                "message": str(e),
                "analysis_result": {},
                "module": self.name,
            }

    def get_processing_stats(self) -> dict[str, Any]:
        """Statistiques de traitement"""
        return {
            "module": self.name,
            "total_analyses": self._processing_stats["total_analyses"],
            "successful_analyses": self._processing_stats["successful_analyses"],
            "failed_analyses": self._processing_stats["failed_analyses"],
            "success_rate": (
                self._processing_stats["successful_analyses"]
                / self._processing_stats["total_analyses"]
                if self._processing_stats["total_analyses"] > 0
                else 0.0
            ),
            "average_analysis_time": self._processing_stats["average_analysis_time"],
            "patterns_detected": self._processing_stats["patterns_detected"],
            "anomalies_found": self._processing_stats["anomalies_found"],
            "last_analysis": self._processing_stats["last_analysis"],
        }

    def get_metrics(self) -> dict[str, Any]:
        """Récupération des métriques Sandozia"""
        try:
            if not self._initialized:
                return {
                    "status": "error",
                    "message": "Sandozia Adapter non initialisé",
                    "metrics": {},
                }

            # Récupérer les métriques de l'analyseur comportemental
            if self._behavior_analyzer:
                metrics_summary = self._behavior_analyzer.get_metrics_summary()
                pattern_history = self._behavior_analyzer.get_pattern_history(limit=10)
            else:
                metrics_summary = {}
                pattern_history = []

            # Mettre à jour les métriques stockées
            self._metrics = {
                "metrics_summary": metrics_summary,
                "pattern_history": pattern_history,
                "processing_stats": self._processing_stats,
            }

            return {
                "status": "success",
                "module": self.name,
                "metrics": self._metrics,
                "alert_thresholds": self._alert_thresholds,
                "last_update": "now",  # En production, utiliser datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Erreur récupération métriques Sandozia: {e}")
            return {
                "status": "error",
                "message": str(e),
                "metrics": {},
                "module": self.name,
            }

    def set_alert_threshold(self, metric: str, threshold: float) -> bool:
        """Configuration des seuils d'alerte"""
        try:
            if metric in self._alert_thresholds:
                self._alert_thresholds[metric] = threshold
                logger.info(f"✅ Seuil d'alerte {metric} mis à jour: {threshold}")
                return True
            else:
                logger.warning(f"⚠️ Métrique {metric} non reconnue")
                return False

        except Exception as e:
            logger.error(f"❌ Erreur configuration seuil d'alerte: {e}")
            return False

    def _analyze_behavior(self, data: dict[str, Any]) -> dict[str, Any]:
        """Analyse comportementale via BehaviorAnalyzer"""
        try:
            if not self._behavior_analyzer:
                return {"status": "error", "message": "BehaviorAnalyzer non disponible"}

            # Ajouter des métriques d'exemple si fournies
            if "metrics" in data:
                for module_name, metrics in data["metrics"].items():
                    for metric_name, value in metrics.items():
                        self._behavior_analyzer.add_metric_sample(module_name, metric_name, value)

            # Ajouter des événements de décision si fournis
            if "decisions" in data:
                for decision in data["decisions"]:
                    self._behavior_analyzer.add_decision_event(
                        decision.get("module", "unknown"), decision
                    )

            # Effectuer l'analyse complète
            analysis_result = self._behavior_analyzer.analyze_behavior()

            # Compter les patterns et anomalies
            patterns = analysis_result.get("patterns", [])
            anomalies = [p for p in patterns if p.get("pattern_type") == "statistical_anomaly"]

            self._processing_stats["patterns_detected"] += len(patterns)
            self._processing_stats["anomalies_found"] += len(anomalies)

            return {
                "status": "success",
                "analysis": analysis_result,
                "patterns_count": len(patterns),
                "anomalies_count": len(anomalies),
            }

        except Exception as e:
            logger.error(f"❌ Erreur analyse comportementale: {e}")
            return {"status": "error", "message": str(e)}

    def _update_processing_stats(
        self, analysis_time: float, success: bool, result: dict[str, Any]
    ) -> None:
        """Met à jour les statistiques de traitement"""
        self._processing_stats["total_analyses"] += 1

        if success:
            self._processing_stats["successful_analyses"] += 1
        else:
            self._processing_stats["failed_analyses"] += 1

        # Mettre à jour le temps d'analyse moyen
        total_successful = self._processing_stats["successful_analyses"]
        if total_successful > 0:
            current_avg = self._processing_stats["average_analysis_time"]
            new_avg = ((current_avg * (total_successful - 1)) + analysis_time) / total_successful
            self._processing_stats["average_analysis_time"] = new_avg

        self._processing_stats["last_analysis"] = {
            "success": success,
            "analysis_time": analysis_time,
            "result_status": result.get("status", "unknown"),
            "timestamp": "now",  # En production, utiliser datetime.now().isoformat()
        }

    def analyze_behavior(self, data: dict[str, Any]) -> dict[str, Any]:
        """Méthode spécifique pour l'analyse comportementale"""
        return self.process(
            {
                "analysis_type": "behavior",
                **data,
            }
        )

    def process_core(self, data: dict[str, Any]) -> dict[str, Any]:
        """Méthode spécifique pour le traitement core Sandozia"""
        return self.process(
            {
                "analysis_type": "core",
                **data,
            }
        )


# Factory function pour créer l'adaptateur
def create_sandozia_adapter() -> SandoziaAdapter:
    """Crée une instance de l'adaptateur Sandozia"""
    return SandoziaAdapter()
