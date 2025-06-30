#!/usr/bin/env python3
# 🧠 modules/sandozia/validators/crossmodule.py
# CrossModuleValidator - Validation croisée entre modules IA

"""
CrossModuleValidator - Validation Cohérence Inter-Modules

Vérifie la cohérence entre :
- Reflexia (auto-réflexion)
- ZeroIA (détection contradictions)
- AssistantIA (interactions utilisateur)

Détecte :
- Désalignements temporels
- Contradictions logiques
- Incohérences de scores/confiance
- Dérives comportementales
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import toml

logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Niveaux de validation"""

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    OK = "ok"


@dataclass
class ValidationResult:
    """Résultat d'une validation croisée"""

    level: ValidationLevel
    module_source: str
    module_target: str
    message: str
    details: dict[str, Any]
    timestamp: datetime
    suggested_action: str | None = None

    def to_dict(self) -> dict:
        return {
            "level": self.level.value,
            "module_source": self.module_source,
            "module_target": self.module_target,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "suggested_action": self.suggested_action,
        }


class CrossModuleValidator:
    """
    Validateur de cohérence inter-modules IA

    Fonctionnalités :
    - Validation temporelle (synchronisation)
    - Validation logique (contradictions)
    - Validation de confiance (scores cohérents)
    - Validation comportementale (patterns)
    """

    def __init__(self, config: dict | None = None) -> None:
        self.config = config or {
            "temporal_tolerance_minutes": 5,
            "confidence_variance_threshold": 0.2,
            "critical_coherence_threshold": 0.6,
            "max_validation_history": 1000,
        }

        self.validation_history: list[ValidationResult] = []
        self.state_cache: dict[str, dict] = {}

        # Chemins des états des modules
        self.state_paths = {
            "reflexia": Path("state/reflexia_state.toml"),
            "zeroia": Path("state/zeroia_state.toml"),
            "global": Path("state/global_context.toml"),
        }

        logger.info("🔍 CrossModuleValidator initialized")

    def load_module_states(self) -> dict[str, dict]:
        """Charge les états actuels de tous les modules"""
        states: dict[str, Any] = {}

        for module_name, state_path in self.state_paths.items():
            try:
                if state_path.exists():
                    with open(state_path) as f:
                        states[module_name] = toml.load(f)
                    logger.debug(f"✅ Loaded {module_name} state")
                else:
                    states[module_name] = {}
                    logger.warning(f"⚠️ {module_name} state file not found: {state_path}")
            except Exception as e:
                logger.error(f"❌ Error loading {module_name} state: {e}")
                states[module_name] = {}

        # Cache pour comparaisons futures
        self.state_cache = states.copy()
        return states

    def validate_temporal_coherence(self, states: dict[str, dict]) -> list[ValidationResult]:
        """Valide la cohérence temporelle entre modules"""
        results: list[Any] = []
        now = datetime.now()
        tolerance = timedelta(minutes=self.config["temporal_tolerance_minutes"])

        # Extraire les timestamps des différents modules
        timestamps: dict[str, Any] = {}

        # Reflexia
        reflexia_state = states.get("reflexia", {})
        if "last_execution" in reflexia_state:
            try:
                timestamps["reflexia"] = datetime.fromisoformat(
                    reflexia_state["last_execution"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pass

        # ZeroIA
        zeroia_state = states.get("zeroia", {})
        if "last_check" in zeroia_state:
            try:
                timestamps["zeroia"] = datetime.fromisoformat(
                    zeroia_state["last_check"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pass

        # Global context
        global_state = states.get("global", {})
        if "last_update" in global_state:
            try:
                timestamps["global"] = datetime.fromisoformat(
                    global_state["last_update"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pass

        # Vérifier la synchronisation
        if len(timestamps) >= 2:
            module_pairs = [
                ("reflexia", "zeroia"),
                ("reflexia", "global"),
                ("zeroia", "global"),
            ]

            for mod1, mod2 in module_pairs:
                if mod1 in timestamps and mod2 in timestamps:
                    time_diff = abs(timestamps[mod1] - timestamps[mod2])

                    if time_diff > tolerance:
                        level = (
                            ValidationLevel.WARNING
                            if time_diff < tolerance * 2
                            else ValidationLevel.CRITICAL
                        )

                        result = ValidationResult(
                            level=level,
                            module_source=mod1,
                            module_target=mod2,
                            message=f"Désynchronisation temporelle détectée: {time_diff}",
                            details={
                                "time_difference_seconds": time_diff.total_seconds(),
                                "tolerance_seconds": tolerance.total_seconds(),
                                f"{mod1}_timestamp": timestamps[mod1].isoformat(),
                                f"{mod2}_timestamp": timestamps[mod2].isoformat(),
                            },
                            timestamp=now,
                            suggested_action="Vérifier les processus de mise à jour des modules",
                        )
                        results.append(result)

        return results

    def validate_confidence_coherence(self, states: dict[str, dict]) -> list[ValidationResult]:
        """Valide la cohérence des scores de confiance"""
        results: list[Any] = []
        now = datetime.now()

        # Extraire les scores de confiance
        confidence_scores: dict[str, Any] = {}

        # Reflexia confidence
        reflexia_state = states.get("reflexia", {})
        if "decision_metrics" in reflexia_state:
            confidence_scores["reflexia"] = reflexia_state["decision_metrics"].get(
                "confidence", 0.0
            )

        # ZeroIA confidence
        zeroia_state = states.get("zeroia", {})
        if "confidence_score" in zeroia_state:
            confidence_scores["zeroia"] = zeroia_state["confidence_score"]

        # Vérifier la cohérence des scores
        if len(confidence_scores) >= 2:
            score_values = list(confidence_scores.values())
            score_variance = max(score_values) - min(score_values)

            threshold = self.config["confidence_variance_threshold"]

            if score_variance > threshold:
                level = (
                    ValidationLevel.WARNING
                    if score_variance < threshold * 1.5
                    else ValidationLevel.CRITICAL
                )

                result = ValidationResult(
                    level=level,
                    module_source="confidence_analyzer",
                    module_target="all_modules",
                    message=f"Variance élevée dans les scores de confiance: {score_variance:.3f}",
                    details={
                        "confidence_scores": confidence_scores,
                        "variance": score_variance,
                        "threshold": threshold,
                        "modules_analyzed": list(confidence_scores.keys()),
                    },
                    timestamp=now,
                    suggested_action="Investiguer les causes de divergence des scores de confiance",
                )
                results.append(result)

        return results

    def validate_logical_consistency(self, states: dict[str, dict]) -> list[ValidationResult]:
        """Valide la consistance logique entre modules"""
        results: list[Any] = []
        now = datetime.now()

        # Analyser ZeroIA vs Reflexia
        reflexia_state = states.get("reflexia", {})
        zeroia_state = states.get("zeroia", {})

        # ZeroIA détecte des contradictions mais Reflexia haute confiance
        if (
            zeroia_state.get("contradictions_detected", 0) > 0
            and reflexia_state.get("decision_metrics", {}).get("confidence", 0.0) > 0.9
        ):
            result = ValidationResult(
                level=ValidationLevel.WARNING,
                module_source="zeroia",
                module_target="reflexia",
                message=(
                    "Contradiction: ZeroIA détecte des incohérences mais "
                    "Reflexia a une confiance élevée"
                ),
                details={
                    "zeroia_contradictions": zeroia_state.get("contradictions_detected", 0),
                    "reflexia_confidence": reflexia_state.get("decision_metrics", {}).get(
                        "confidence", 0.0
                    ),
                    "potential_issue": "Possible blindspot or false positive",
                },
                timestamp=now,
                suggested_action="Vérifier manuellement la logique des décisions récentes",
            )
            results.append(result)

        # Reflexia en erreur mais ZeroIA n'a rien détecté
        reflexia_errors = reflexia_state.get("recent_errors", [])
        if len(reflexia_errors) > 0 and zeroia_state.get("contradictions_detected", 0) == 0:
            result = ValidationResult(
                level=ValidationLevel.INFO,
                module_source="reflexia",
                module_target="zeroia",
                message="Reflexia signale des erreurs mais ZeroIA ne détecte pas de contradictions",
                details={
                    "reflexia_errors": len(reflexia_errors),
                    "zeroia_contradictions": zeroia_state.get("contradictions_detected", 0),
                    "last_reflexia_error": (reflexia_errors[-1] if reflexia_errors else None),
                },
                timestamp=now,
                suggested_action="Vérifier si ZeroIA doit être plus sensible",
            )
            results.append(result)

        return results

    def validate_behavioral_patterns(self, states: dict[str, dict]) -> list[ValidationResult]:
        """Valide les patterns comportementaux"""
        results: list[Any] = []
        now = datetime.now()

        # Analyser les tendances récentes
        if len(self.validation_history) >= 5:
            recent_validations = self.validation_history[-10:]

            # Compter les erreurs critiques récentes
            critical_count = sum(
                1 for v in recent_validations if v.level == ValidationLevel.CRITICAL
            )

            if critical_count >= 3:
                result = ValidationResult(
                    level=ValidationLevel.CRITICAL,
                    module_source="pattern_analyzer",
                    module_target="system",
                    message=(
                        f"Pattern comportemental suspect: {critical_count} "
                        f"erreurs critiques récentes"
                    ),
                    details={
                        "critical_errors_count": critical_count,
                        "validation_window": 10,
                        "error_rate": critical_count / 10,
                    },
                    timestamp=now,
                    suggested_action="Investigation urgente des causes systémiques",
                )
                results.append(result)

        return results

    def run_full_validation(self) -> dict[str, Any]:
        """Exécute une validation complète inter-modules"""
        logger.info("🔍 Starting cross-module validation...")

        # Charger les états
        states = self.load_module_states()

        # Exécuter toutes les validations
        all_results: list[Any] = []

        all_results.extend(self.validate_temporal_coherence(states))
        all_results.extend(self.validate_confidence_coherence(states))
        all_results.extend(self.validate_logical_consistency(states))
        all_results.extend(self.validate_behavioral_patterns(states))

        # Ajouter à l'historique
        self.validation_history.extend(all_results)

        # Limiter l'historique
        max_history = self.config["max_validation_history"]
        if len(self.validation_history) > max_history:
            self.validation_history = self.validation_history[-max_history:]

        # Calculer le score global de cohérence
        if all_results:
            critical_count = sum(1 for r in all_results if r.level == ValidationLevel.CRITICAL)
            warning_count = sum(1 for r in all_results if r.level == ValidationLevel.WARNING)

            # Score basé sur la gravité des issues
            coherence_score = max(0.0, 1.0 - (critical_count * 0.3 + warning_count * 0.1))
        else:
            coherence_score = 1.0

        # Résumé
        summary = {
            "timestamp": datetime.now().isoformat(),
            "coherence_score": coherence_score,
            "total_validations": len(all_results),
            "issues_by_level": {
                "critical": sum(1 for r in all_results if r.level == ValidationLevel.CRITICAL),
                "warning": sum(1 for r in all_results if r.level == ValidationLevel.WARNING),
                "info": sum(1 for r in all_results if r.level == ValidationLevel.INFO),
                "ok": sum(1 for r in all_results if r.level == ValidationLevel.OK),
            },
            "modules_analyzed": list(states.keys()),
            "validation_results": [r.to_dict() for r in all_results],
            "overall_status": (
                "healthy"
                if coherence_score > 0.8
                else "degraded"
                if coherence_score > 0.6
                else "critical"
            ),
        }

        logger.info(f"✅ Cross-module validation complete - Score: {coherence_score:.3f}")
        return summary

    def validate_cross_modules(self, active_modules: list[str] | None = None) -> dict[str, Any]:
        """
        Méthode principale de validation croisée - Interface pour Orchestrateur

        Args:
            active_modules: Liste des modules actifs à valider

        Returns:
            Dict avec résultats de validation
        """
        try:
            # Charger les états et effectuer la validation
            validation_results = self.run_full_validation()

            # Adapter la validation selon les modules actifs
            if active_modules:
                logger.info(
                    f"🔍 Validating cross-module coherence for: {', '.join(active_modules)}"
                )

            # Simplifier la réponse pour l'orchestrateur
            return {
                "status": "success",
                "active_modules": active_modules or [],
                "total_validations": len(validation_results.get("results", [])),
                "critical_count": len(
                    [
                        r
                        for r in validation_results.get("results", [])
                        if r.get("level") == "critical"
                    ]
                ),
                "warning_count": len(
                    [
                        r
                        for r in validation_results.get("results", [])
                        if r.get("level") == "warning"
                    ]
                ),
                "coherence_score": validation_results.get("coherence_score", 0.8),
                "score": validation_results.get(
                    "coherence_score", 0.8
                ),  # Alias pour l'orchestrateur
                "details": validation_results,
            }
        except Exception as e:
            logger.error(f"❌ CrossModule validation error: {e}")
            return {"status": "error", "error": str(e), "coherence_score": 0.0}

    def get_validation_report(self) -> dict[str, Any]:
        """Génère un rapport de validation"""
        recent_validations = self.validation_history[-50:] if self.validation_history else []

        return {
            "total_validations_run": len(self.validation_history),
            "recent_validations": [v.to_dict() for v in recent_validations],
            "current_config": self.config,
            "modules_monitored": list(self.state_paths.keys()),
        }


# CLI pour test
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CrossModuleValidator CLI")
    parser.add_argument("--validate", action="store_true", help="Run full validation")
    parser.add_argument("--report", action="store_true", help="Generate validation report")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    validator = CrossModuleValidator()

    if args.validate:
        result = validator.run_full_validation()
        print(json.dumps(result, indent=2))

    if args.report:
        report = validator.get_validation_report()
        print(json.dumps(report, indent=2))
