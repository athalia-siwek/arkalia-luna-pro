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
    """Résultat d'un raisonnement collaboratif"""

    consensus_reached: bool
    final_decision: str
    confidence: float
    participating_modules: list[str]
    reasoning_steps: list[dict]
    timestamp: datetime

    def to_dict(self) -> dict:
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
    Système de raisonnement collaboratif entre IA

    Fonctionnalités :
    - Collecte des raisons de chaque module
    - Comparaison et analyse des divergences
    - Calcul de consensus
    - Résolution de conflits
    """

    def __init__(self, config: dict | None = None):
        self.config = config or {
            "consensus_threshold": 0.8,
            "max_reasoning_rounds": 3,
            "confidence_weight": 0.7,
            "agreement_weight": 0.3,
        }

        self.reasoning_history: list[ReasoningResult] = []

        logger.info("🧠 CollaborativeReasoning initialized")

    def collect_module_reasoning(self, module_decisions: dict[str, dict]) -> dict[str, Any]:
        """Collecte les raisonnements de chaque module"""

        reasoning_data = {}

        for module_name, decision_data in module_decisions.items():
            reasoning_data[module_name] = {
                "decision": decision_data.get("decision", "unknown"),
                "confidence": decision_data.get("confidence", 0.0),
                "reasoning": decision_data.get("reasoning", "No reasoning provided"),
                "timestamp": decision_data.get("timestamp", datetime.now().isoformat()),
            }

        return reasoning_data

    def calculate_consensus(self, reasoning_data: dict[str, Any]) -> ReasoningResult:
        """Calcule le consensus entre les modules"""

        if not reasoning_data:
            return ReasoningResult(
                consensus_reached=False,
                final_decision="no_data",
                confidence=0.0,
                participating_modules=[],
                reasoning_steps=[],
                timestamp=datetime.now(),
            )

        # Analyser les décisions
        decisions = {}
        total_confidence = 0.0

        for module, data in reasoning_data.items():
            decision = data.get("decision", "unknown")
            confidence = data.get("confidence", 0.0)

            if decision not in decisions:
                decisions[decision] = []

            decisions[decision].append(
                {
                    "module": module,
                    "confidence": confidence,
                    "reasoning": data.get("reasoning", ""),
                }
            )

            total_confidence += confidence

        # Trouver la décision majoritaire pondérée
        best_decision = None
        best_score = 0.0

        for decision, supporters in decisions.items():
            # Score = nombre de supporters + confiance moyenne
            support_count = len(supporters)
            avg_confidence = sum(s["confidence"] for s in supporters) / len(supporters)

            weighted_score = (
                support_count * self.config["agreement_weight"]
                + avg_confidence * self.config["confidence_weight"]
            )

            if weighted_score > best_score:
                best_score = weighted_score
                best_decision = decision

        # Calculer consensus
        consensus_reached = best_score >= self.config["consensus_threshold"]

        # Confiance finale
        if best_decision and best_decision in decisions:
            final_confidence = sum(s["confidence"] for s in decisions[best_decision]) / len(
                decisions[best_decision]
            )
        else:
            final_confidence = 0.0

        # Étapes de raisonnement
        reasoning_steps = [
            {
                "step": "decision_collection",
                "data": {
                    "decisions_found": list(decisions.keys()),
                    "total_modules": len(reasoning_data),
                },
            },
            {
                "step": "consensus_calculation",
                "data": {
                    "best_decision": best_decision,
                    "best_score": best_score,
                    "threshold": self.config["consensus_threshold"],
                },
            },
        ]

        result = ReasoningResult(
            consensus_reached=consensus_reached,
            final_decision=best_decision or "no_consensus",
            confidence=final_confidence,
            participating_modules=list(reasoning_data.keys()),
            reasoning_steps=reasoning_steps,
            timestamp=datetime.now(),
        )

        # Sauvegarder dans l'historique
        self.reasoning_history.append(result)

        return result

    def analyze_disagreements(self, reasoning_data: dict[str, Any]) -> dict[str, Any]:
        """Analyse les désaccords entre modules"""

        disagreements = []
        modules = list(reasoning_data.keys())

        # Comparer chaque paire de modules
        for i in range(len(modules)):
            for j in range(i + 1, len(modules)):
                module1, module2 = modules[i], modules[j]

                decision1 = reasoning_data[module1].get("decision")
                decision2 = reasoning_data[module2].get("decision")

                if decision1 != decision2:
                    disagreements.append(
                        {
                            "modules": [module1, module2],
                            "decisions": [decision1, decision2],
                            "confidence_gap": abs(
                                reasoning_data[module1].get("confidence", 0)
                                - reasoning_data[module2].get("confidence", 0)
                            ),
                        }
                    )

        return {
            "disagreement_count": len(disagreements),
            "disagreements": disagreements,
            "agreement_ratio": 1.0
            - (len(disagreements) / max(1, len(modules) * (len(modules) - 1) / 2)),
        }

    def run_collaborative_reasoning(self, module_decisions: dict[str, dict]) -> dict[str, Any]:
        """Exécute un cycle complet de raisonnement collaboratif"""

        logger.info("🧠 Starting collaborative reasoning...")

        # Collecter les raisonnements
        reasoning_data = self.collect_module_reasoning(module_decisions)

        # Analyser les désaccords
        disagreement_analysis = self.analyze_disagreements(reasoning_data)

        # Calculer consensus
        consensus_result = self.calculate_consensus(reasoning_data)

        # Résumé complet
        summary = {
            "timestamp": datetime.now().isoformat(),
            "input_modules": len(module_decisions),
            "reasoning_data": reasoning_data,
            "disagreement_analysis": disagreement_analysis,
            "consensus_result": consensus_result.to_dict(),
            "success": consensus_result.consensus_reached,
        }

        logger.info(
            f"✅ Collaborative reasoning complete - Consensus: {consensus_result.consensus_reached}"
        )

        return summary

    def get_reasoning_history(self, limit: int | None = None) -> list[dict]:
        """Retourne l'historique des raisonnements"""
        history = self.reasoning_history[-limit:] if limit else self.reasoning_history
        return [r.to_dict() for r in history]

    def get_consensus_stats(self) -> dict[str, Any]:
        """Statistiques sur les consensus atteints"""
        if not self.reasoning_history:
            return {"total_reasonings": 0, "consensus_rate": 0.0}

        consensus_count = sum(1 for r in self.reasoning_history if r.consensus_reached)

        return {
            "total_reasonings": len(self.reasoning_history),
            "consensus_reached": consensus_count,
            "consensus_rate": consensus_count / len(self.reasoning_history),
            "average_confidence": sum(r.confidence for r in self.reasoning_history)
            / len(self.reasoning_history),
        }


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
