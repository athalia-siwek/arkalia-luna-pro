#!/usr/bin/env python3
# 🧠 modules/sandozia/analyzer/behavior.py
# BehaviorAnalyzer - Détection de patterns comportementaux

"""
BehaviorAnalyzer - Analyse Comportementale IA

Détecte des patterns suspects ou aberrants dans :
- Logs d'activité des modules IA
- Historique des décisions
- Métriques de performance
- Corrélations temporelles

Signale :
- Dérives comportementales
- Anomalies statistiques
- Patterns de régression
- Incohérences répétitives
"""

import json
import logging
import statistics
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class BehaviorPattern:
    """Pattern comportemental détecté"""

    pattern_type: str
    severity: str  # "low", "medium", "high", "critical"
    description: str
    affected_modules: List[str]
    confidence: float  # 0.0-1.0
    first_detected: datetime
    last_detected: datetime
    occurrences: int
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict:
        return {
            "pattern_type": self.pattern_type,
            "severity": self.severity,
            "description": self.description,
            "affected_modules": self.affected_modules,
            "confidence": self.confidence,
            "first_detected": self.first_detected.isoformat(),
            "last_detected": self.last_detected.isoformat(),
            "occurrences": self.occurrences,
            "metadata": self.metadata,
        }


class BehaviorAnalyzer:
    """
    Analyseur de comportements IA

    Analyse en temps réel :
    - Patterns de décision
    - Dérives de performance
    - Anomalies statistiques
    - Corrélations suspectes
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {
            "window_size_minutes": 60,
            "anomaly_threshold": 2.0,  # Écarts-types
            "pattern_min_occurrences": 3,
            "confidence_threshold": 0.7,
            "max_pattern_history": 500,
        }

        self.pattern_history: List[BehaviorPattern] = []
        self.metrics_buffer: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.decision_history: deque = deque(maxlen=500)

        # État statistique
        self.baseline_stats: Dict[str, Dict] = {}
        self.anomaly_counters: Dict[str, int] = defaultdict(int)

        logger.info("🧠 BehaviorAnalyzer initialized")

    def add_metric_sample(
        self,
        module_name: str,
        metric_name: str,
        value: float,
        timestamp: Optional[datetime] = None,
    ):
        """Ajoute un échantillon de métrique pour analyse"""
        timestamp = timestamp or datetime.now()

        key = f"{module_name}.{metric_name}"
        self.metrics_buffer[key].append({"value": value, "timestamp": timestamp})

        # Mettre à jour les statistiques de base si suffisamment d'échantillons
        if len(self.metrics_buffer[key]) >= 30:
            self._update_baseline_stats(key)

    def add_decision_event(self, module_name: str, decision_data: Dict):
        """Ajoute un événement de décision pour analyse"""
        decision_event = {
            "module": module_name,
            "timestamp": datetime.now(),
            "data": decision_data,
        }
        self.decision_history.append(decision_event)

    def _update_baseline_stats(self, metric_key: str):
        """Met à jour les statistiques de base pour une métrique"""
        samples = self.metrics_buffer[metric_key]
        values = [s["value"] for s in samples]

        if len(values) >= 5:  # Minimum pour calculs statistiques
            self.baseline_stats[metric_key] = {
                "mean": statistics.mean(values),
                "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
                "median": statistics.median(values),
                "min": min(values),
                "max": max(values),
                "sample_size": len(values),
                "last_updated": datetime.now(),
            }

    def detect_statistical_anomalies(self) -> List[BehaviorPattern]:
        """Détecte des anomalies statistiques dans les métriques"""
        patterns = []
        now = datetime.now()
        threshold = self.config["anomaly_threshold"]

        for metric_key, samples in self.metrics_buffer.items():
            if len(samples) < 10:
                continue

            # Récupérer les statistiques de base
            stats = self.baseline_stats.get(metric_key)
            if not stats or stats["stdev"] == 0:
                continue

            # Analyser les échantillons récents
            recent_samples = [
                s for s in samples if (now - s["timestamp"]).total_seconds() < 3600
            ]  # 1h

            if len(recent_samples) >= 3:
                recent_values = [s["value"] for s in recent_samples]
                recent_mean = statistics.mean(recent_values)

                # Calculer l'écart par rapport à la baseline
                z_score = abs(recent_mean - stats["mean"]) / stats["stdev"]

                if z_score > threshold:
                    module_name = metric_key.split(".")[0]
                    metric_name = ".".join(metric_key.split(".")[1:])

                    severity = "high" if z_score > threshold * 1.5 else "medium"

                    pattern = BehaviorPattern(
                        pattern_type="statistical_anomaly",
                        severity=severity,
                        description=f"Anomalie statistique détectée dans {metric_name} (z-score: {z_score:.2f})",
                        affected_modules=[module_name],
                        confidence=min(0.95, z_score / (threshold * 2)),
                        first_detected=recent_samples[0]["timestamp"],
                        last_detected=recent_samples[-1]["timestamp"],
                        occurrences=len(recent_samples),
                        metadata={
                            "metric_key": metric_key,
                            "z_score": z_score,
                            "recent_mean": recent_mean,
                            "baseline_mean": stats["mean"],
                            "baseline_stdev": stats["stdev"],
                            "threshold": threshold,
                        },
                    )
                    patterns.append(pattern)

        return patterns

    def detect_performance_regression(self) -> List[BehaviorPattern]:
        """Détecte des régressions de performance"""
        patterns = []

        # Analyser les métriques de performance connues
        performance_metrics = [
            "response_time",
            "accuracy",
            "confidence_score",
            "processing_time",
            "success_rate",
        ]

        for metric_name in performance_metrics:
            for module_name in ["reflexia", "zeroia", "assistantia"]:
                metric_key = f"{module_name}.{metric_name}"

                if metric_key not in self.metrics_buffer:
                    continue

                samples = list(self.metrics_buffer[metric_key])
                if len(samples) < 20:
                    continue

                # Comparer première moitié vs deuxième moitié
                mid = len(samples) // 2
                first_half = [s["value"] for s in samples[:mid]]
                second_half = [s["value"] for s in samples[mid:]]

                if len(first_half) >= 5 and len(second_half) >= 5:
                    first_mean = statistics.mean(first_half)
                    second_mean = statistics.mean(second_half)

                    # Pour métriques où moins = mieux (temps de réponse)
                    regression_metrics = ["response_time", "processing_time"]
                    is_regression_metric = metric_name in regression_metrics

                    # Calculer le changement relatif
                    if first_mean > 0:
                        relative_change = (second_mean - first_mean) / first_mean

                        # Détecter régression
                        threshold = 0.2  # 20% de dégradation
                        is_regression = (
                            is_regression_metric and relative_change > threshold
                        ) or (not is_regression_metric and relative_change < -threshold)

                        if is_regression:
                            pattern = BehaviorPattern(
                                pattern_type="performance_regression",
                                severity=(
                                    "medium" if abs(relative_change) < 0.4 else "high"
                                ),
                                description=f"Régression de performance détectée dans {metric_name}: {relative_change:.1%}",
                                affected_modules=[module_name],
                                confidence=min(0.9, abs(relative_change) * 2),
                                first_detected=samples[mid]["timestamp"],
                                last_detected=samples[-1]["timestamp"],
                                occurrences=len(second_half),
                                metadata={
                                    "metric_name": metric_name,
                                    "first_half_mean": first_mean,
                                    "second_half_mean": second_mean,
                                    "relative_change": relative_change,
                                    "is_regression_metric": is_regression_metric,
                                },
                            )
                            patterns.append(pattern)

        return patterns

    def detect_decision_patterns(self) -> List[BehaviorPattern]:
        """Détecte des patterns suspects dans les décisions"""
        patterns = []

        if len(self.decision_history) < 10:
            return patterns

        # Analyser les décisions par module
        decisions_by_module = defaultdict(list)
        for decision in self.decision_history:
            decisions_by_module[decision["module"]].append(decision)

        for module_name, decisions in decisions_by_module.items():
            if len(decisions) < 5:
                continue

            # Détecter patterns répétitifs suspects
            recent_decisions = decisions[-10:]  # 10 dernières décisions

            # Analyser la diversité des décisions
            decision_types = [
                d["data"].get("decision_type", "unknown") for d in recent_decisions
            ]

            # Si toutes les décisions sont identiques -> potentiel problème
            unique_types = set(decision_types)
            if len(unique_types) == 1 and len(recent_decisions) >= 5:
                pattern = BehaviorPattern(
                    pattern_type="repetitive_decisions",
                    severity="medium",
                    description=f"Pattern répétitif détecté: {len(recent_decisions)} décisions identiques ({list(unique_types)[0]})",
                    affected_modules=[module_name],
                    confidence=0.8,
                    first_detected=recent_decisions[0]["timestamp"],
                    last_detected=recent_decisions[-1]["timestamp"],
                    occurrences=len(recent_decisions),
                    metadata={
                        "decision_type": list(unique_types)[0],
                        "repetition_count": len(recent_decisions),
                    },
                )
                patterns.append(pattern)

            # Analyser la fréquence des décisions
            timestamps = [d["timestamp"] for d in recent_decisions]
            if len(timestamps) >= 3:
                time_intervals = []
                for i in range(1, len(timestamps)):
                    interval = (timestamps[i] - timestamps[i - 1]).total_seconds()
                    time_intervals.append(interval)

                if time_intervals:
                    mean_interval = statistics.mean(time_intervals)

                    # Décisions trop fréquentes (< 1 seconde entre décisions)
                    if mean_interval < 1.0:
                        pattern = BehaviorPattern(
                            pattern_type="high_frequency_decisions",
                            severity="medium",
                            description=f"Fréquence de décision élevée: {mean_interval:.2f}s entre décisions",
                            affected_modules=[module_name],
                            confidence=0.7,
                            first_detected=timestamps[0],
                            last_detected=timestamps[-1],
                            occurrences=len(time_intervals),
                            metadata={
                                "mean_interval_seconds": mean_interval,
                                "min_interval": min(time_intervals),
                                "max_interval": max(time_intervals),
                            },
                        )
                        patterns.append(pattern)

        return patterns

    def detect_correlation_anomalies(self) -> List[BehaviorPattern]:
        """Détecte des anomalies dans les corrélations entre modules"""
        patterns = []

        # Analyser les corrélations de confiance entre modules
        confidence_metrics = {}
        for metric_key in self.metrics_buffer:
            if "confidence" in metric_key.lower():
                module_name = metric_key.split(".")[0]
                recent_samples = [
                    s["value"] for s in list(self.metrics_buffer[metric_key])[-10:]
                ]
                if recent_samples:
                    confidence_metrics[module_name] = statistics.mean(recent_samples)

        if len(confidence_metrics) >= 2:
            modules = list(confidence_metrics.keys())

            # Vérifier les écarts importants entre modules
            max_confidence = max(confidence_metrics.values())
            min_confidence = min(confidence_metrics.values())
            confidence_gap = max_confidence - min_confidence

            if confidence_gap > 0.3:  # Écart > 30%
                high_conf_modules = [
                    m for m, c in confidence_metrics.items() if c == max_confidence
                ]
                low_conf_modules = [
                    m for m, c in confidence_metrics.items() if c == min_confidence
                ]

                pattern = BehaviorPattern(
                    pattern_type="confidence_divergence",
                    severity="medium",
                    description=f"Divergence de confiance importante: {confidence_gap:.1%} d'écart",
                    affected_modules=modules,
                    confidence=0.8,
                    first_detected=datetime.now() - timedelta(minutes=30),
                    last_detected=datetime.now(),
                    occurrences=1,
                    metadata={
                        "confidence_gap": confidence_gap,
                        "high_confidence_modules": high_conf_modules,
                        "low_confidence_modules": low_conf_modules,
                        "all_confidences": confidence_metrics,
                    },
                )
                patterns.append(pattern)

        return patterns

    def analyze_behavior(self) -> Dict[str, Any]:
        """Exécute une analyse complète des comportements"""
        logger.info("🔍 Starting behavior analysis...")

        # Exécuter toutes les analyses
        all_patterns = []

        all_patterns.extend(self.detect_statistical_anomalies())
        all_patterns.extend(self.detect_performance_regression())
        all_patterns.extend(self.detect_decision_patterns())
        all_patterns.extend(self.detect_correlation_anomalies())

        # Ajouter à l'historique
        self.pattern_history.extend(all_patterns)

        # Limiter l'historique
        max_history = self.config["max_pattern_history"]
        if len(self.pattern_history) > max_history:
            self.pattern_history = self.pattern_history[-max_history:]

        # Calculer des statistiques globales
        severity_counts = defaultdict(int)
        pattern_type_counts = defaultdict(int)
        affected_modules = set()

        for pattern in all_patterns:
            severity_counts[pattern.severity] += 1
            pattern_type_counts[pattern.pattern_type] += 1
            affected_modules.update(pattern.affected_modules)

        # Score de santé comportementale
        health_score = 1.0
        health_score -= severity_counts["critical"] * 0.4
        health_score -= severity_counts["high"] * 0.2
        health_score -= severity_counts["medium"] * 0.1
        health_score = max(0.0, health_score)

        summary = {
            "timestamp": datetime.now().isoformat(),
            "behavioral_health_score": health_score,
            "patterns_detected": len(all_patterns),
            "patterns_by_severity": dict(severity_counts),
            "patterns_by_type": dict(pattern_type_counts),
            "affected_modules": list(affected_modules),
            "patterns_detail": [p.to_dict() for p in all_patterns],
            "metrics_monitored": len(self.metrics_buffer),
            "decisions_analyzed": len(self.decision_history),
            "baseline_stats_available": len(self.baseline_stats),
        }

        logger.info(f"✅ Behavior analysis complete - Health score: {health_score:.3f}")
        return summary

    def get_pattern_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Retourne l'historique des patterns détectés"""
        patterns = self.pattern_history[-limit:] if limit else self.pattern_history
        return [p.to_dict() for p in patterns]

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des métriques surveillées"""
        summary = {}

        for metric_key, samples in self.metrics_buffer.items():
            if samples:
                values = [s["value"] for s in samples]
                summary[metric_key] = {
                    "sample_count": len(values),
                    "latest_value": values[-1],
                    "mean": statistics.mean(values),
                    "min": min(values),
                    "max": max(values),
                    "last_updated": samples[-1]["timestamp"].isoformat(),
                }

        return summary


# CLI pour test
if __name__ == "__main__":
    import argparse
    import random
    import time

    parser = argparse.ArgumentParser(description="BehaviorAnalyzer CLI")
    parser.add_argument(
        "--demo", action="store_true", help="Run demo with synthetic data"
    )
    parser.add_argument("--analyze", action="store_true", help="Run behavior analysis")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    analyzer = BehaviorAnalyzer()

    if args.demo:
        print("🧠 Generating synthetic behavior data...")

        # Générer des données synthétiques
        for i in range(50):
            # Métriques normales
            analyzer.add_metric_sample(
                "reflexia", "confidence_score", random.uniform(0.7, 0.95)
            )
            analyzer.add_metric_sample(
                "zeroia", "confidence_score", random.uniform(0.6, 0.9)
            )

            # Temps de réponse
            analyzer.add_metric_sample(
                "reflexia", "response_time", random.uniform(0.1, 0.5)
            )

            time.sleep(0.01)  # Petit délai

        # Ajouter quelques anomalies
        for i in range(5):
            analyzer.add_metric_sample("reflexia", "confidence_score", 0.2)  # Anomalie
            analyzer.add_metric_sample("reflexia", "response_time", 5.0)  # Régression

        print("📊 Synthetic data generated")

    if args.analyze or args.demo:
        result = analyzer.analyze_behavior()
        print(json.dumps(result, indent=2))
