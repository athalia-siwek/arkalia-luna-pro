#!/usr/bin/env python3
# 🧠 modules/sandozia/utils/metrics.py
# Utilitaires métriques Sandozia

"""
SandoziaMetrics - Utilitaires métriques pour Sandozia

Collecte et traite les métriques d'intelligence croisée :
- Métriques Prometheus
- Corrélations temporelles
- Agrégations cross-modules
- Export Grafana
"""

import logging
import statistics
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class MetricPoint:
    """Point de métrique avec timestamp"""

    timestamp: datetime
    value: float
    labels: dict[str, str]

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "labels": self.labels,
        }


class SandoziaMetrics:
    """
    Collecteur et processeur de métriques Sandozia

    Fonctionnalités :
    - Collecte cross-modules
    - Calculs de corrélation
    - Agrégations temporelles
    - Export formats Grafana/Prometheus
    """

    def __init__(self, retention_hours: int = 24) -> None:
        self.retention_hours = retention_hours
        self.metrics_store: dict[str, list[MetricPoint]] = defaultdict(list)
        self.correlations_cache: dict[str, float] = {}

        logger.info("📊 SandoziaMetrics initialized")

    def add_metric(self, name: str, value: float, labels: dict[str, str] | None = None):
        """Ajoute une métrique"""
        labels = labels or {}
        timestamp = datetime.now()

        metric_point = MetricPoint(timestamp=timestamp, value=value, labels=labels)

        self.metrics_store[name].append(metric_point)

        # Nettoyer les anciennes métriques
        self._cleanup_old_metrics(name)

    def _cleanup_old_metrics(self, metric_name: str):
        """Nettoie les métriques anciennes"""
        cutoff = datetime.now() - timedelta(hours=self.retention_hours)

        self.metrics_store[metric_name] = [
            point for point in self.metrics_store[metric_name] if point.timestamp > cutoff
        ]

    def get_metric_values(self, name: str, time_window_minutes: int | None = None) -> list[float]:
        """Récupère les valeurs d'une métrique"""
        if name not in self.metrics_store:
            return []

        points = self.metrics_store[name]

        if time_window_minutes:
            cutoff = datetime.now() - timedelta(minutes=time_window_minutes)
            points = [p for p in points if p.timestamp > cutoff]

        return [p.value for p in points]

    def calculate_correlation(
        self, metric1: str, metric2: str, time_window_minutes: int = 60
    ) -> float | None:
        """Calcule la corrélation entre deux métriques"""
        values1 = self.get_metric_values(metric1, time_window_minutes)
        values2 = self.get_metric_values(metric2, time_window_minutes)

        if len(values1) < 3 or len(values2) < 3 or len(values1) != len(values2):
            return None

        try:
            # Calcul corrélation de Pearson simple
            mean1 = statistics.mean(values1)
            mean2 = statistics.mean(values2)

            numerator = sum(
                (x - mean1) * (y - mean2) for x, y in zip(values1, values2, strict=False)
            )

            sum_sq1 = sum((x - mean1) ** 2 for x in values1)
            sum_sq2 = sum((y - mean2) ** 2 for y in values2)

            denominator = (sum_sq1 * sum_sq2) ** 0.5

            if denominator == 0:
                return 0.0

            correlation = numerator / denominator

            # Cache le résultat
            cache_key = f"{metric1}_{metric2}_{time_window_minutes}"
            self.correlations_cache[cache_key] = correlation

            return correlation

        except Exception as e:
            logger.warning(f"⚠️ Correlation calculation failed: {e}")
            return None

    def get_metric_summary(self, name: str) -> dict[str, Any] | None:
        """Résumé statistique d'une métrique"""
        values = self.get_metric_values(name)

        if not values:
            return None

        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
            "latest": values[-1] if values else None,
            "first_timestamp": (
                self.metrics_store[name][0].timestamp.isoformat()
                if self.metrics_store[name]
                else None
            ),
            "last_timestamp": (
                self.metrics_store[name][-1].timestamp.isoformat()
                if self.metrics_store[name]
                else None
            ),
        }

    def export_prometheus_format(self) -> str:
        """Exporte au format Prometheus"""
        lines = []

        for metric_name, points in self.metrics_store.items():
            if not points:
                continue

            # Métrique la plus récente
            latest_point = points[-1]

            # Format Prometheus avec labels
            labels_str = ""
            if latest_point.labels:
                label_pairs = [f'{k}="{v}"' for k, v in latest_point.labels.items()]
                labels_str = "{" + ",".join(label_pairs) + "}"

            line = f"sandozia_{metric_name}{labels_str} {latest_point.value}"
            lines.append(line)

        return "\n".join(lines)

    def export_grafana_json(self) -> dict[str, Any]:
        """Exporte au format JSON pour Grafana"""
        series = []

        for metric_name, points in self.metrics_store.items():
            if not points:
                continue

            datapoints = []
            for point in points:
                # Format Grafana: [value, timestamp_ms]
                timestamp_ms = int(point.timestamp.timestamp() * 1000)
                datapoints.append([point.value, timestamp_ms])

            series.append({"target": metric_name, "datapoints": datapoints})

        return {
            "series": series,
            "exported_at": datetime.now().isoformat(),
            "retention_hours": self.retention_hours,
        }

    def get_cross_module_health(self) -> dict[str, Any]:
        """Calcule la santé cross-modules"""
        health_metrics = {}

        # Métriques de base par module
        modules = ["reflexia", "zeroia", "assistantia"]
        base_metrics = ["confidence_score", "response_time", "success_rate"]

        for module in modules:
            module_health = {}

            for metric in base_metrics:
                metric_key = f"{module}_{metric}"
                summary = self.get_metric_summary(metric_key)

                if summary:
                    # Score de santé basé sur les valeurs récentes
                    if metric == "confidence_score":
                        health_score = summary["mean"]  # Plus c'est haut, mieux c'est
                    elif metric in ["response_time"]:
                        # Inverser pour temps de réponse (moins = mieux)
                        max_acceptable = 2.0  # 2 secondes max
                        health_score = max(0.0, 1.0 - (summary["mean"] / max_acceptable))
                    elif metric == "success_rate":
                        health_score = summary["mean"]
                    else:
                        health_score = 0.5  # Valeur neutre par défaut

                    module_health[metric] = {"score": health_score, "summary": summary}

            if module_health:
                # Score global du module
                scores = [m["score"] for m in module_health.values()]
                overall_score = statistics.mean(scores) if scores else 0.0

                health_metrics[module] = {
                    "overall_health": overall_score,
                    "metrics": module_health,
                }

        # Score de cohérence inter-modules
        coherence_scores = []
        for module in modules:
            if module in health_metrics:
                coherence_scores.append(health_metrics[module]["overall_health"])

        if len(coherence_scores) >= 2:
            coherence_variance = statistics.variance(coherence_scores)
            coherence_score = max(
                0.0, 1.0 - coherence_variance
            )  # Moins de variance = plus de cohérence
        else:
            coherence_score = 0.0

        return {
            "timestamp": datetime.now().isoformat(),
            "modules": health_metrics,
            "cross_module_coherence": coherence_score,
            "available_correlations": len(self.correlations_cache),
            "total_metrics": len(self.metrics_store),
        }

    def get_all_metrics(self) -> dict[str, Any]:
        """Retourne toutes les métriques et métadonnées"""
        return {
            "metrics_count": len(self.metrics_store),
            "metrics_names": list(self.metrics_store.keys()),
            "retention_hours": self.retention_hours,
            "correlations_cached": len(self.correlations_cache),
            "oldest_metric": min(
                (points[0].timestamp for points in self.metrics_store.values() if points),
                default=datetime.now(),
            ).isoformat(),
            "latest_metric": max(
                (points[-1].timestamp for points in self.metrics_store.values() if points),
                default=datetime.now(),
            ).isoformat(),
        }


# Fonctions helper
def create_sandozia_metrics() -> SandoziaMetrics:
    """Crée une instance SandoziaMetrics avec config par défaut"""
    return SandoziaMetrics(retention_hours=24)


def demo_metrics():
    """Démonstration avec données synthétiques"""
    import random
    import time

    metrics = create_sandozia_metrics()

    print("📊 Generating demo metrics...")

    # Générer des métriques synthétiques
    for _i in range(100):
        # Metrics Reflexia
        metrics.add_metric(
            "reflexia_confidence_score",
            random.uniform(0.7, 0.95),
            {"module": "reflexia", "type": "confidence"},
        )

        # Metrics ZeroIA
        metrics.add_metric(
            "zeroia_confidence_score",
            random.uniform(0.6, 0.9),
            {"module": "zeroia", "type": "confidence"},
        )

        # Response times
        metrics.add_metric(
            "reflexia_response_time",
            random.uniform(0.1, 0.8),
            {"module": "reflexia", "type": "performance"},
        )

        time.sleep(0.01)

    # Analyser les résultats
    print("\n🔍 Analysis results:")

    # Corrélation entre confiances
    correlation = metrics.calculate_correlation(
        "reflexia_confidence_score", "zeroia_confidence_score"
    )
    if correlation:
        print(f"Corrélation confiance Reflexia-ZeroIA: {correlation:.3f}")

    # Santé cross-modules
    health = metrics.get_cross_module_health()
    print(f"Cohérence inter-modules: {health['cross_module_coherence']:.3f}")

    # Export Prometheus
    prometheus_data = metrics.export_prometheus_format()
    print(f"\n📤 Prometheus export ({len(prometheus_data.split())} metrics):")
    print(prometheus_data[:200] + "..." if len(prometheus_data) > 200 else prometheus_data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo_metrics()
