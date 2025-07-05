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
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    OK = "ok"


@dataclass
class ValidationResult:
    level: ValidationLevel
    module_source: str
    module_target: str
    message: str
    details: dict[str, Any]
    timestamp: datetime
    suggested_action: str | None = None

    def to_dict(self) -> dict:
        """
        Fonction to_dict.

        Cette fonction fait partie du système Arkalia Luna Pro.
        """
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
    Validateur cross-modules Sandozia

    Valide la cohérence entre modules :
    - Vérification des interfaces
    - Validation des données partagées
    - Détection des incohérences
    - Rapport de validation
    """

    def __init__(self, config: dict | None = None) -> None:
        """
        Fonction __init__.

        Cette fonction fait partie du système Arkalia Luna Pro.
        """
        self.config = config or {
            "validation_timeout": 30,
            "strict_mode": False,
            "auto_fix": False,
        }
        self.validation_history: list[dict] = []
        self.known_issues: dict[str, list] = {}
        self.state_paths: dict[str, Path] = {}
        self.state_cache: dict[str, dict] = {}
        logger.info("🔍 CrossModuleValidator initialized")

    def validate_module_interfaces(self, modules_data: dict[str, dict]) -> dict[str, Any]:
        """
        Valide les interfaces entre modules

        Args:
            modules_data: Données des modules

        Returns:
            dict: Résultats de validation
        """
        logger.info("🔍 Starting cross-module interface validation...")

        validation_result = {
            "status": "completed",
            "modules_checked": list(modules_data.keys()),
            "issues_found": [],
            "warnings": [],
            "passed": True,
            "timestamp": datetime.now().isoformat(),
        }

        # Vérifier les interfaces communes
        for module1, data1 in modules_data.items():
            for module2, data2 in modules_data.items():
                if module1 >= module2:
                    continue

                interface_issues = self._validate_interface(module1, data1, module2, data2)
                validation_result["issues_found"].extend(interface_issues)  # type: ignore

        # Déterminer le statut global
        if validation_result["issues_found"]:
            validation_result["passed"] = False

        # Enregistrer dans l'historique
        self.validation_history.append(validation_result)
        if len(self.validation_history) > 50:
            self.validation_history = self.validation_history[-50:]

        logger.info(f"✅ Cross-module validation completed: {validation_result['passed']}")
        return validation_result

    def _validate_interface(
        self, module1: str, data1: dict, module2: str, data2: dict
    ) -> list[dict]:
        """
        Valide l'interface entre deux modules

        Args:
            module1: Nom du premier module
            data1: Données du premier module
            module2: Nom du deuxième module
            data2: Données du deuxième module

        Returns:
            list[dict]: Problèmes détectés
        """
        issues = []

        # Vérifier les types de données partagées
        shared_keys = set(data1.keys()) & set(data2.keys())
        for key in shared_keys:
            type1 = type(data1[key])
            type2 = type(data2[key])

            if type1 != type2:
                issues.append(
                    {
                        "type": "type_mismatch",
                        "module1": module1,
                        "module2": module2,
                        "key": key,
                        "type1": str(type1),
                        "type2": str(type2),
                        "severity": "error",
                    }
                )

        # Vérifier les valeurs incohérentes
        for key in shared_keys:
            if isinstance(data1[key], int | float) and isinstance(data2[key], int | float):
                if abs(data1[key] - data2[key]) > 0.01:  # Tolérance pour les floats
                    issues.append(
                        {
                            "type": "value_mismatch",
                            "module1": module1,
                            "module2": module2,
                            "key": key,
                            "value1": data1[key],
                            "value2": data2[key],
                            "severity": "warning",
                        }
                    )

        return issues

    def validate_data_consistency(self, modules_data: dict[str, dict]) -> dict[str, Any]:
        """
        Valide la cohérence des données entre modules

        Args:
            modules_data: Données des modules

        Returns:
            dict: Résultats de validation
        """
        logger.info("🔍 Starting data consistency validation...")

        consistency_result = {
            "status": "completed",
            "consistency_score": 1.0,
            "inconsistencies": [],
            "timestamp": datetime.now().isoformat(),
        }

        # Analyser la cohérence des données
        all_keys: set[str] = set()
        for data in modules_data.values():
            all_keys.update(data.keys())

        for key in all_keys:
            values = []
            for module_name, data in modules_data.items():
                if key in data:
                    values.append((module_name, data[key]))

            if len(values) > 1:
                inconsistency = self._check_value_consistency(key, values)
                if inconsistency:
                    consistency_result["inconsistencies"].append(inconsistency)

        # Calculer le score de cohérence
        total_checks = len(all_keys)
        failed_checks = len(consistency_result["inconsistencies"])
        if total_checks > 0:
            consistency_result["consistency_score"] = 1.0 - (failed_checks / total_checks)

        logger.info(
            f"✅ Data consistency validation completed: {consistency_result['consistency_score']:.2f}"
        )
        return consistency_result

    def _check_value_consistency(self, key: str, values: list[tuple[str, Any]]) -> dict | None:
        """
        Vérifie la cohérence des valeurs pour une clé

        Args:
            key: Clé à vérifier
            values: Liste de (module, valeur)

        Returns:
            dict | None: Incohérence détectée ou None
        """
        if not values:
            return None

        # Vérifier si toutes les valeurs sont identiques
        first_value = values[0][1]
        inconsistent_modules = []

        for module_name, value in values:
            if value != first_value:
                inconsistent_modules.append(
                    {
                        "module": module_name,
                        "value": value,
                    }
                )

        if inconsistent_modules:
            return {
                "key": key,
                "expected_value": first_value,
                "inconsistent_modules": inconsistent_modules,
            }

        return None

    def get_validation_summary(self) -> dict[str, Any]:
        """
        Récupère un résumé des validations

        Returns:
            dict: Résumé des validations
        """
        if not self.validation_history:
            return {"total_validations": 0, "success_rate": 0.0}

        total_validations = len(self.validation_history)
        successful_validations = sum(1 for v in self.validation_history if v.get("passed", False))
        success_rate = successful_validations / total_validations

        return {
            "total_validations": total_validations,
            "successful_validations": successful_validations,
            "success_rate": success_rate,
            "last_validation": self.validation_history[-1] if self.validation_history else None,
        }

    def get_known_issues(self) -> dict[str, list]:
        """
        Récupère les problèmes connus

        Returns:
            dict: Problèmes connus par module
        """
        return self.known_issues.copy()

    def add_known_issue(self, module: str, issue: dict) -> None:
        """
        Ajoute un problème connu

        Args:
            module: Nom du module
            issue: Description du problème
        """
        if module not in self.known_issues:
            self.known_issues[module] = []
        self.known_issues[module].append(issue)

    def clear_validation_history(self) -> None:
        """
        Nettoie l'historique de validation
        """
        self.validation_history.clear()
        logger.info("🧹 Validation history cleared")

    def load_module_states(self) -> dict[str, dict]:
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
        results: list[Any] = []
        now = datetime.now()

        # Analyser les tendances récentes
        if len(self.validation_history) >= 5:
            recent_validations = self.validation_history[-10:]

            # Compter les erreurs critiques récentes
            critical_count = sum(
                1
                for v in recent_validations
                if isinstance(v, ValidationResult) and v.level == ValidationLevel.CRITICAL
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
                else "degraded" if coherence_score > 0.6 else "critical"
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
        recent_validations = self.validation_history[-50:] if self.validation_history else []

        return {
            "total_validations_run": len(self.validation_history),
            "recent_validations": [
                v.to_dict() if hasattr(v, "to_dict") else v for v in recent_validations
            ],
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
