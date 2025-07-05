#!/usr/bin/env python3
"""
⚖️ Load Balancer - Équilibrage de charge intelligent
🎯 Distribution optimale des requêtes entre les modules
"""

import logging
import random
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from statistics import mean, median
from typing import Any, Optional

logger = logging.getLogger(__name__)


class LoadBalancingStrategy(Enum):
    """Stratégies d'équilibrage de charge"""

    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_LEAST_CONNECTIONS = "weighted_least_connections"
    RESPONSE_TIME = "response_time"
    ADAPTIVE = "adaptive"


@dataclass
class BackendNode:
    """Nœud backend avec métriques"""

    id: str
    name: str
    weight: int = 1
    max_connections: int = 100
    current_connections: int = 0
    response_time: float = 0.0
    error_rate: float = 0.0
    health_score: float = 1.0
    last_health_check: datetime = field(default_factory=datetime.now)
    is_healthy: bool = True
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0

    def update_metrics(self, response_time: float, success: bool) -> None:
        """Met à jour les métriques du nœud"""
        self.response_time = response_time
        self.total_requests += 1

        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

        # Calculer le taux d'erreur
        self.error_rate = (
            self.failed_requests / self.total_requests if self.total_requests > 0 else 0.0
        )

        # Calculer le score de santé
        self.health_score = max(0.0, 1.0 - self.error_rate - (self.response_time / 1000.0))

    def increment_connections(self) -> bool:
        """Incrémente le nombre de connexions actives"""
        if self.current_connections < self.max_connections:
            self.current_connections += 1
            return True
        return False

    def decrement_connections(self) -> None:
        """Décrémente le nombre de connexions actives"""
        self.current_connections = max(0, self.current_connections - 1)

    def to_dict(self) -> dict[str, Any]:
        """Convertit en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "weight": self.weight,
            "max_connections": self.max_connections,
            "current_connections": self.current_connections,
            "response_time": self.response_time,
            "error_rate": self.error_rate,
            "health_score": self.health_score,
            "is_healthy": self.is_healthy,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "last_health_check": self.last_health_check.isoformat(),
        }


class LoadBalancer:
    """
    ⚖️ Équilibreur de charge intelligent
    🎯 Distribution optimale avec monitoring en temps réel
    """

    def __init__(self, strategy: LoadBalancingStrategy = LoadBalancingStrategy.ADAPTIVE):
        self.strategy = strategy
        self.backends: list[BackendNode] = []
        self.current_index = 0
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0,
        }

        # Configuration
        self.config = {
            "health_check_interval": 30,  # secondes
            "response_time_threshold": 1000,  # ms
            "error_rate_threshold": 0.1,  # 10%
            "adaptive_weight_factor": 0.1,
        }

        logger.info(f"⚖️ LoadBalancer initialisé avec stratégie: {strategy.value}")

    def add_backend(self, backend: BackendNode) -> bool:
        """Ajoute un backend à l'équilibreur"""
        try:
            # Vérifier si le backend existe déjà
            if any(b.id == backend.id for b in self.backends):
                logger.warning(f"⚠️ Backend déjà existant: {backend.id}")
                return False

            self.backends.append(backend)
            logger.info(f"✅ Backend ajouté: {backend.name} ({backend.id})")
            return True

        except Exception as e:
            logger.error(f"❌ Erreur ajout backend: {e}")
            return False

    def remove_backend(self, backend_id: str) -> bool:
        """Supprime un backend de l'équilibreur"""
        try:
            for i, backend in enumerate(self.backends):
                if backend.id == backend_id:
                    del self.backends[i]
                    logger.info(f"✅ Backend supprimé: {backend_id}")
                    return True

            logger.warning(f"⚠️ Backend non trouvé: {backend_id}")
            return False

        except Exception as e:
            logger.error(f"❌ Erreur suppression backend: {e}")
            return False

    def get_backend(self) -> BackendNode | None:
        """Sélectionne un backend selon la stratégie"""
        if not self.backends:
            logger.warning("⚠️ Aucun backend disponible")
            return None

        # Filtrer les backends sains
        healthy_backends = [b for b in self.backends if b.is_healthy]
        if not healthy_backends:
            logger.error("❌ Aucun backend sain disponible")
            return None

        # Sélectionner selon la stratégie
        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._round_robin(healthy_backends)
        elif self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
            return self._weighted_round_robin(healthy_backends)
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._least_connections(healthy_backends)
        elif self.strategy == LoadBalancingStrategy.WEIGHTED_LEAST_CONNECTIONS:
            return self._weighted_least_connections(healthy_backends)
        elif self.strategy == LoadBalancingStrategy.RESPONSE_TIME:
            return self._response_time(healthy_backends)
        elif self.strategy == LoadBalancingStrategy.ADAPTIVE:
            return self._adaptive(healthy_backends)
        else:
            return self._round_robin(healthy_backends)

    def execute_request(self, request_func: Callable, *args, **kwargs) -> Any:
        """Exécute une requête via l'équilibreur de charge"""
        backend = self.get_backend()
        if not backend:
            raise Exception("Aucun backend disponible")

        start_time = time.time()
        success = False

        try:
            # Incrémenter les connexions
            if not backend.increment_connections():
                raise Exception(f"Backend {backend.id} au maximum de connexions")

            # Exécuter la requête
            result = request_func(*args, **kwargs)
            success = True
            return result

        except Exception as e:
            logger.error(f"❌ Erreur requête backend {backend.id}: {e}")
            raise

        finally:
            # Mettre à jour les métriques
            response_time = (time.time() - start_time) * 1000  # ms
            backend.update_metrics(response_time, success)
            backend.decrement_connections()

            # Mettre à jour les métriques globales
            self.metrics["total_requests"] += 1
            if success:
                self.metrics["successful_requests"] += 1
            else:
                self.metrics["failed_requests"] += 1

            # Mettre à jour le temps de réponse moyen
            total_successful = self.metrics["successful_requests"]
            if total_successful > 0:
                self.metrics["average_response_time"] = (
                    self.metrics["average_response_time"] * (total_successful - 1) + response_time
                ) / total_successful

    def health_check(self) -> dict[str, Any]:
        """Effectue un contrôle de santé des backends"""
        results = {}

        for backend in self.backends:
            try:
                # Vérifier les métriques
                is_healthy = (
                    backend.error_rate < self.config["error_rate_threshold"]
                    and backend.response_time < self.config["response_time_threshold"]
                    and backend.health_score > 0.5
                )

                backend.is_healthy = is_healthy
                backend.last_health_check = datetime.now()

                results[backend.id] = {
                    "healthy": is_healthy,
                    "health_score": backend.health_score,
                    "error_rate": backend.error_rate,
                    "response_time": backend.response_time,
                }

                if not is_healthy:
                    logger.warning(
                        f"⚠️ Backend {backend.id} non sain: score={backend.health_score:.2f}"
                    )

            except Exception as e:
                logger.error(f"❌ Erreur health check backend {backend.id}: {e}")
                backend.is_healthy = False
                results[backend.id] = {"healthy": False, "error": str(e)}

        return results

    def get_stats(self) -> dict[str, Any]:
        """Récupère les statistiques de l'équilibreur"""
        total_requests = self.metrics["total_requests"]
        success_rate = (
            self.metrics["successful_requests"] / total_requests * 100
            if total_requests > 0
            else 0.0
        )

        return {
            "strategy": self.strategy.value,
            "total_backends": len(self.backends),
            "healthy_backends": len([b for b in self.backends if b.is_healthy]),
            "total_requests": total_requests,
            "successful_requests": self.metrics["successful_requests"],
            "failed_requests": self.metrics["failed_requests"],
            "success_rate": round(success_rate, 2),
            "average_response_time": round(self.metrics["average_response_time"], 2),
            "backends": [b.to_dict() for b in self.backends],
        }

    def _round_robin(self, backends: list[BackendNode]) -> BackendNode:
        """Sélection round-robin simple"""
        backend = backends[self.current_index % len(backends)]
        self.current_index += 1
        return backend

    def _weighted_round_robin(self, backends: list[BackendNode]) -> BackendNode:
        """Sélection round-robin pondérée"""
        # Calculer le poids total
        total_weight = sum(b.weight for b in backends)

        # Sélectionner selon les poids
        current_weight = 0
        for backend in backends:
            current_weight += backend.weight
            if self.current_index < current_weight:
                self.current_index += 1
                return backend

        # Fallback
        self.current_index += 1
        return backends[0]

    def _least_connections(self, backends: list[BackendNode]) -> BackendNode:
        """Sélection par nombre de connexions minimal"""
        return min(backends, key=lambda b: b.current_connections)

    def _weighted_least_connections(self, backends: list[BackendNode]) -> BackendNode:
        """Sélection par nombre de connexions pondéré"""
        return min(backends, key=lambda b: b.current_connections / b.weight)

    def _response_time(self, backends: list[BackendNode]) -> BackendNode:
        """Sélection par temps de réponse minimal"""
        return min(backends, key=lambda b: b.response_time)

    def _adaptive(self, backends: list[BackendNode]) -> BackendNode:
        """Sélection adaptative basée sur plusieurs critères"""
        # Calculer un score pour chaque backend
        scores = []
        for backend in backends:
            # Score basé sur la santé, les connexions et le temps de réponse
            connection_score = 1.0 - (backend.current_connections / backend.max_connections)
            response_score = max(
                0.0, 1.0 - (backend.response_time / self.config["response_time_threshold"])
            )

            # Score combiné
            score = backend.health_score * 0.4 + connection_score * 0.3 + response_score * 0.3

            scores.append((backend, score))

        # Sélectionner le backend avec le meilleur score
        best_backend, best_score = max(scores, key=lambda x: x[1])

        # Ajuster les poids de manière adaptative
        for backend, score in scores:
            if score > 0.8:  # Backend performant
                backend.weight = min(backend.weight + self.config["adaptive_weight_factor"], 10)
            elif score < 0.5:  # Backend peu performant
                backend.weight = max(backend.weight - self.config["adaptive_weight_factor"], 1)

        return best_backend


# Instance globale
_load_balancer: LoadBalancer | None = None


def get_load_balancer() -> LoadBalancer:
    """Récupère l'instance globale du load balancer"""
    global _load_balancer
    if _load_balancer is None:
        _load_balancer = LoadBalancer()
    return _load_balancer


def load_balanced_request():
    """Décorateur pour exécuter une requête via le load balancer"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            load_balancer = get_load_balancer()
            return load_balancer.execute_request(func, *args, **kwargs)

        return wrapper

    return decorator
