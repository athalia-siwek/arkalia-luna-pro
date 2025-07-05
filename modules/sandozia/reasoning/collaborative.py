#!/usr/bin/env python3
# 🧠 modules/sandozia/reasoning/collaborative.py
# CollaborativeReasoning - Raisonnement collaboratif IA

"""
CollaborativeReasoning - Raisonnement Multi-Agent

Coordonne le raisonnement entre modules IA :
- Comparaison des raisons de décision
- Consensus entre IA
- Résolution de conflits
- Apprentissage collaboratif
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class ReasoningResult:
    consensus_reached: bool
    final_decision: str
    confidence: float
    participating_modules: list[str]
    reasoning_steps: list[dict]
    timestamp: datetime

    def to_dict(self) -> dict:
        """
        Fonction to_dict.

        Cette fonction fait partie du système Arkalia Luna Pro.
        """
        return {
            "consensus_reached": self.consensus_reached,
            "final_decision": self.final_decision,
            "confidence": self.confidence,
            "participating_modules": self.participating_modules,
            "reasoning_steps": self.reasoning_steps,
            "timestamp": self.timestamp.isoformat(),
        }


class CollaborativeReasoning:
    """
    Système de raisonnement collaboratif

    Coordonne les intelligences multiples :
    - Fusion des perspectives
    - Résolution de conflits
    - Synthèse des décisions
    - Apprentissage collectif
    """

    def __init__(self, config: dict | None = None) -> None:
        """
        Fonction __init__.

        Cette fonction fait partie du système Arkalia Luna Pro.
        """
        self.config = config or {
            "consensus_threshold": 0.7,
            "max_iterations": 3,
            "timeout_seconds": 30,
        }
        self.reasoning_history: list[dict] = []
        self.consensus_cache: dict[str, dict] = {}
        logger.info("🤝 CollaborativeReasoning initialized")

    def coordinate_reasoning(
        self, module_insights: dict[str, dict], context: dict | None = None
    ) -> dict[str, Any]:
        """
        Coordonne le raisonnement entre modules

        Args:
            module_insights: Insights de chaque module
            context: Contexte additionnel

        Returns:
            dict: Synthèse collaborative
        """
        logger.info("🤝 Starting collaborative reasoning...")

        # Analyser les insights
        analysis = self._analyze_insights(module_insights)
        if not analysis["has_conflicts"]:
            return self._create_consensus(analysis)

        # Résoudre les conflits
        resolution = self._resolve_conflicts(analysis, context)
        return self._create_final_synthesis(resolution)

    def _analyze_insights(self, module_insights: dict[str, dict]) -> dict[str, Any]:
        """
        Analyse les insights des modules

        Args:
            module_insights: Insights de chaque module

        Returns:
            dict: Analyse des insights
        """
        analysis: dict[str, Any] = {
            "modules": list(module_insights.keys()),
            "insights": module_insights,
            "conflicts": [],
            "agreements": [],
            "has_conflicts": False,
        }

        # Détecter les conflits
        for module1, insight1 in module_insights.items():
            for module2, insight2 in module_insights.items():
                if module1 >= module2:
                    continue

                conflict = self._detect_conflict(insight1, insight2)
                if conflict:
                    analysis["conflicts"].append(conflict)
                    analysis["has_conflicts"] = True
                else:
                    agreement = self._detect_agreement(insight1, insight2)
                    if agreement:
                        analysis["agreements"].append(agreement)

        return analysis

    def _detect_conflict(self, insight1: dict, insight2: dict) -> dict | None:
        """
        Détecte les conflits entre insights

        Args:
            insight1: Premier insight
            insight2: Deuxième insight

        Returns:
            dict | None: Conflit détecté ou None
        """
        # Logique de détection de conflit simplifiée
        if insight1.get("confidence", 0) > 0.8 and insight2.get("confidence", 0) > 0.8:
            if insight1.get("decision") != insight2.get("decision"):
                return {
                    "type": "decision_conflict",
                    "insight1": insight1,
                    "insight2": insight2,
                    "severity": "high",
                }
        return None

    def _detect_agreement(self, insight1: dict, insight2: dict) -> dict | None:
        """
        Détecte les accords entre insights

        Args:
            insight1: Premier insight
            insight2: Deuxième insight

        Returns:
            dict | None: Accord détecté ou None
        """
        if insight1.get("decision") == insight2.get("decision"):
            return {
                "type": "decision_agreement",
                "insight1": insight1,
                "insight2": insight2,
                "confidence": (insight1.get("confidence", 0) + insight2.get("confidence", 0)) / 2,
            }
        return None

    def _resolve_conflicts(self, analysis: dict, context: dict | None = None) -> dict[str, Any]:
        """
        Résout les conflits détectés

        Args:
            analysis: Analyse des insights
            context: Contexte additionnel

        Returns:
            dict: Résolution des conflits
        """
        resolution: dict[str, Any] = {
            "resolved_conflicts": [],
            "unresolved_conflicts": [],
            "final_decision": None,
            "confidence": 0.0,
        }

        for conflict in analysis["conflicts"]:
            resolved = self._resolve_single_conflict(conflict, context)
            if resolved:
                resolution["resolved_conflicts"].append(resolved)
            else:
                resolution["unresolved_conflicts"].append(conflict)

        # Créer la décision finale
        if resolution["resolved_conflicts"]:
            resolution["final_decision"] = self._create_final_decision(resolution)
            resolution["confidence"] = self._calculate_final_confidence(resolution)

        return resolution

    def _resolve_single_conflict(self, conflict: dict, context: dict | None = None) -> dict | None:
        """
        Résout un conflit individuel

        Args:
            conflict: Conflit à résoudre
            context: Contexte additionnel

        Returns:
            dict | None: Conflit résolu ou None
        """
        # Logique de résolution simplifiée
        if conflict["type"] == "decision_conflict":
            # Prioriser l'insight avec la plus haute confiance
            insight1 = conflict["insight1"]
            insight2 = conflict["insight2"]

            if insight1.get("confidence", 0) > insight2.get("confidence", 0):
                return {
                    "conflict": conflict,
                    "resolution": "prioritize_insight1",
                    "selected_insight": insight1,
                }
            else:
                return {
                    "conflict": conflict,
                    "resolution": "prioritize_insight2",
                    "selected_insight": insight2,
                }

        return None

    def _create_final_decision(self, resolution: dict) -> dict:
        """
        Crée la décision finale

        Args:
            resolution: Résolution des conflits

        Returns:
            dict: Décision finale
        """
        # Logique simplifiée pour créer la décision finale
        selected_insights = [r["selected_insight"] for r in resolution["resolved_conflicts"]]
        if not selected_insights:
            return {"decision": "no_consensus", "confidence": 0.0}

        # Prendre la décision avec la plus haute confiance
        best_insight = max(selected_insights, key=lambda x: x.get("confidence", 0))
        return {
            "decision": best_insight.get("decision"),
            "confidence": best_insight.get("confidence", 0),
            "reasoning": "highest_confidence_selection",
        }

    def _calculate_final_confidence(self, resolution: dict) -> float:
        """
        Calcule la confiance finale

        Args:
            resolution: Résolution des conflits

        Returns:
            float: Confiance finale
        """
        if not resolution["resolved_conflicts"]:
            return 0.0

        confidences = [
            r["selected_insight"].get("confidence", 0) for r in resolution["resolved_conflicts"]
        ]
        return sum(confidences) / len(confidences)

    def _create_consensus(self, analysis: dict) -> dict[str, Any]:
        """
        Crée un consensus quand il n'y a pas de conflits

        Args:
            analysis: Analyse des insights

        Returns:
            dict: Consensus créé
        """
        insights = list(analysis["insights"].values())
        if not insights:
            return {"decision": "no_insights", "confidence": 0.0}

        # Prendre la décision avec la plus haute confiance
        best_insight = max(insights, key=lambda x: x.get("confidence", 0))
        return {
            "decision": best_insight.get("decision"),
            "confidence": best_insight.get("confidence", 0),
            "reasoning": "consensus_no_conflicts",
            "agreements": len(analysis["agreements"]),
        }

    def _create_final_synthesis(self, resolution: dict) -> dict[str, Any]:
        """
        Crée la synthèse finale

        Args:
            resolution: Résolution des conflits

        Returns:
            dict: Synthèse finale
        """
        synthesis = {
            "status": "completed",
            "final_decision": resolution["final_decision"],
            "confidence": resolution["confidence"],
            "conflicts_resolved": len(resolution["resolved_conflicts"]),
            "conflicts_unresolved": len(resolution["unresolved_conflicts"]),
            "timestamp": datetime.now().isoformat(),
        }

        # Enregistrer dans l'historique
        self.reasoning_history.append(synthesis)
        if len(self.reasoning_history) > 100:  # Limiter l'historique
            self.reasoning_history = self.reasoning_history[-100:]

        logger.info(f"🤝 Collaborative reasoning completed: {synthesis['final_decision']}")
        return synthesis

    def get_reasoning_history(self, limit: int | None = None) -> list[dict]:
        """
        Récupère l'historique du raisonnement

        Args:
            limit: Limite du nombre d'entrées

        Returns:
            list[dict]: Historique du raisonnement
        """
        if limit:
            return self.reasoning_history[-limit:]
        return self.reasoning_history.copy()

    def clear_cache(self) -> None:
        """
        Nettoie le cache de consensus
        """
        self.consensus_cache.clear()
        logger.info("🧹 Collaborative reasoning cache cleared")


# CLI pour test
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CollaborativeReasoning CLI")
    parser.add_argument("--demo", action="store_true", help="Run demo with synthetic data")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    collaborative = CollaborativeReasoning()

    if args.demo:
        print("🧠 Demo CollaborativeReasoning...")

        # Données de test
        test_decisions = {
            "reflexia": {
                "decision": "monitor",
                "confidence": 0.85,
                "reasoning": "CPU usage is moderate, monitoring is appropriate",
                "timestamp": datetime.now().isoformat(),
            },
            "zeroia": {
                "decision": "monitor",
                "confidence": 0.78,
                "reasoning": "No contradictions detected, monitoring sufficient",
                "timestamp": datetime.now().isoformat(),
            },
            "assistantia": {
                "decision": "reduce_load",
                "confidence": 0.65,
                "reasoning": "User interactions suggest system strain",
                "timestamp": datetime.now().isoformat(),
            },
        }

        result = collaborative.run_collaborative_reasoning(test_decisions)
        print(json.dumps(result, indent=2))
