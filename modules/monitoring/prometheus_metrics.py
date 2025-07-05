"""Module de métriques Prometheus pour Arkalia-LUNA"""

from typing import Optional

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram


class ArkaliaMetrics:
    """Classe de gestion des métriques Prometheus"""

    def __init__(self, registry: CollectorRegistry | None = None) -> None:
        # Utiliser le registre fourni ou créer un nouveau
        self._registry = registry or CollectorRegistry()

        # Métriques système
        self.arkalia_system_uptime = Gauge(
            "arkalia_system_uptime",
            "Temps d'activité du système en secondes",
            registry=self._registry,
        )

        self.arkalia_cpu_usage = Gauge(
            "arkalia_cpu_usage", "Utilisation CPU en pourcentage", registry=self._registry
        )

        self.arkalia_memory_usage = Gauge(
            "arkalia_memory_usage", "Utilisation mémoire en bytes", registry=self._registry
        )

        # Métriques des modules
        self.arkalia_modules_status = Gauge(
            "arkalia_modules_status",
            "Statut des modules (1=actif, 0=inactif)",
            ["module_name"],
            registry=self._registry,
        )

        # Métriques des requêtes
        self.arkalia_requests_total = Counter(
            "arkalia_requests_total",
            "Nombre total de requêtes",
            ["method", "endpoint", "status"],
            registry=self._registry,
        )

        self.arkalia_request_duration = Histogram(
            "arkalia_request_duration",
            "Durée des requêtes en secondes",
            ["method", "endpoint"],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
            registry=self._registry,
        )

    def get_registry(self) -> CollectorRegistry:
        """Retourne le registre de métriques"""
        return self._registry
