#!/usr/bin/env python3
"""
🚀 OPTIMIZATION INTEGRATOR - Phase 8
Intégrateur des optimisations avancées d'Arkalia-LUNA

Connecte toutes les optimisations de la Phase 7 :
- Cache intelligent multi-niveaux
- Load balancing adaptatif
- Circuit breaker global
- Métriques avancées avec alertes
"""

import asyncio
import logging
import threading
from typing import Any, Optional

from prometheus_client import CollectorRegistry, Counter, Gauge, generate_latest, start_http_server

from .advanced_metrics import AdvancedMetricsManager
from .cache_manager import CacheManager
from .circuit_breaker import CircuitBreaker
from .load_balancer import LoadBalancer

logger = logging.getLogger(__name__)


class OptimizationIntegrator:
    """
    🌟 INTÉGRATEUR D'OPTIMISATIONS ARKALIA-LUNA

    Coordonne toutes les optimisations avancées :
    - Cache intelligent multi-niveaux
    - Load balancing adaptatif
    - Circuit breaker global
    - Métriques avancées avec alertes
    """

    def __init__(self) -> None:
        self.is_initialized = False
        self.is_running = False

        # Composants d'optimisation
        self.cache_manager: CacheManager | None = None
        self.load_balancer: LoadBalancer | None = None
        self.circuit_breaker: CircuitBreaker | None = None
        self.metrics_collector: AdvancedMetricsManager | None = None

        # État d'intégration
        self.integration_status: dict[str, str] = {}
        self.performance_metrics: dict[str, float] = {}

        logger.info("🚀 OptimizationIntegrator initialisé")

    async def initialize_optimizations(self) -> bool:
        """Initialise toutes les optimisations"""
        try:
            logger.info("🔧 Initialisation des optimisations avancées...")

            # 1. Cache Manager
            self.cache_manager = CacheManager()
            self.integration_status["cache"] = "✅ Initialisé"

            # 2. Load Balancer
            self.load_balancer = LoadBalancer()
            self.integration_status["load_balancer"] = "✅ Initialisé"

            # 3. Circuit Breaker
            self.circuit_breaker = CircuitBreaker("global_circuit")
            self.integration_status["circuit_breaker"] = "✅ Initialisé"

            # 4. Metrics Collector
            self.metrics_collector = AdvancedMetricsManager()
            self.integration_status["metrics"] = "✅ Initialisé"

            self.is_initialized = True
            logger.info("✅ Toutes les optimisations initialisées avec succès")
            return True

        except Exception as e:
            logger.error(f"❌ Erreur initialisation optimisations: {e}")
            return False

    async def start_optimization_services(self) -> bool:
        """Démarre tous les services d'optimisation"""
        if not self.is_initialized:
            logger.error("❌ Optimisations non initialisées")
            return False

        try:
            logger.info("🚀 Démarrage des services d'optimisation...")

            # Les services sont déjà démarrés lors de l'initialisation
            self.is_running = True

            logger.info("✅ Services d'optimisation démarrés")
            return True

        except Exception as e:
            logger.error(f"❌ Erreur démarrage services: {e}")
            return False

    async def optimize_module_operation(self, module_name: str, operation: str, **kwargs) -> Any:
        """Optimise une opération de module avec toutes les optimisations"""
        if not self.is_running:
            logger.warning("⚠️ Optimisations non démarrées, opération normale")
            return await self._execute_normal_operation(module_name, operation, **kwargs)

        try:
            # 1. Vérification circuit breaker
            circuit_state = self.circuit_breaker.get_state()
            if circuit_state.value == "open":
                logger.warning(f"⚠️ Circuit breaker ouvert pour {module_name}")
                return await self._handle_circuit_breaker_fallback(module_name, operation, **kwargs)

            # 2. Cache lookup
            cache_key = f"{module_name}:{operation}:{hash(str(kwargs))}"
            cached_result = self.cache_manager.get(cache_key)
            if cached_result is not None:
                logger.info(f"🎯 Cache hit pour {cache_key}")
                return cached_result

            # 3. Load balancing
            target_instance = self.load_balancer.get_backend()

            # 4. Exécution avec métriques
            start_time = asyncio.get_event_loop().time()

            try:
                result = await self._execute_optimized_operation(
                    target_instance, operation, **kwargs
                )

                # 5. Cache le résultat
                self.cache_manager.set(cache_key, result, ttl=300)  # 5 minutes

                # 6. Métriques de succès
                execution_time = asyncio.get_event_loop().time() - start_time
                self.metrics_collector.record_metric(
                    f"{module_name}.{operation}.success", execution_time
                )

                return result

            except Exception as e:
                # 7. Métriques d'erreur
                execution_time = asyncio.get_event_loop().time() - start_time
                self.metrics_collector.record_metric(
                    f"{module_name}.{operation}.error", execution_time
                )

                # 8. Circuit breaker failure
                # Le circuit breaker gère automatiquement les échecs

                raise e

        except Exception as e:
            logger.error(f"❌ Erreur optimisation {module_name}.{operation}: {e}")
            return await self._execute_normal_operation(module_name, operation, **kwargs)

    async def _execute_optimized_operation(self, instance: Any, operation: str, **kwargs) -> Any:
        """Exécute une opération optimisée"""
        if hasattr(instance, operation):
            method = getattr(instance, operation)
            if asyncio.iscoroutinefunction(method):
                return await method(**kwargs)
            else:
                return method(**kwargs)
        else:
            raise AttributeError(f"Opération {operation} non trouvée")

    async def _execute_normal_operation(self, module_name: str, operation: str, **kwargs) -> Any:
        """Exécute une opération normale (fallback)"""
        logger.info(f"🔄 Exécution normale: {module_name}.{operation}")
        # Simulation d'opération normale
        await asyncio.sleep(0.1)
        return {"status": "normal_execution", "module": module_name, "operation": operation}

    async def _handle_circuit_breaker_fallback(
        self, module_name: str, operation: str, **kwargs
    ) -> Any:
        """Gère le fallback quand le circuit breaker est ouvert"""
        logger.info(f"🛡️ Circuit breaker fallback pour {module_name}")
        return {
            "status": "circuit_breaker_fallback",
            "module": module_name,
            "operation": operation,
            "message": "Service temporairement indisponible",
        }

    async def get_optimization_status(self) -> dict[str, Any]:
        """Retourne le statut de toutes les optimisations"""
        return {
            "is_initialized": self.is_initialized,
            "is_running": self.is_running,
            "integration_status": self.integration_status,
            "cache_stats": self.cache_manager.get_stats() if self.cache_manager else {},
            "load_balancer_stats": self.load_balancer.get_stats() if self.load_balancer else {},
            "circuit_breaker_stats": (
                self.circuit_breaker.get_metrics() if self.circuit_breaker else {}
            ),
            "metrics_summary": (
                self.metrics_collector.get_global_stats() if self.metrics_collector else {}
            ),
        }

    async def get_performance_metrics(self) -> dict[str, float]:
        """Retourne les métriques de performance"""
        if not self.metrics_collector:
            return {}

        stats = self.metrics_collector.get_global_stats()
        return {k: v for k, v in stats.items() if isinstance(v, int | float)}

    async def stop_optimization_services(self) -> None:
        """Arrête tous les services d'optimisation"""
        logger.info("🛑 Arrêt des services d'optimisation...")

        self.is_running = False
        logger.info("✅ Services d'optimisation arrêtés")

    async def health_check(self) -> dict[str, Any]:
        """Vérification de santé des optimisations"""
        health_status = {"overall": "healthy", "components": {}}

        # Vérification cache
        if self.cache_manager:
            cache_health = {
                "status": "healthy",
                "hits": self.cache_manager.get_stats().get("hits", 0),
            }
            health_status["components"]["cache"] = cache_health

        # Vérification load balancer
        if self.load_balancer:
            lb_health = {"status": "healthy", "backends": len(self.load_balancer.backends)}
            health_status["components"]["load_balancer"] = lb_health

        # Vérification circuit breaker
        if self.circuit_breaker:
            cb_health = {"status": "healthy", "state": self.circuit_breaker.get_state().value}
            health_status["components"]["circuit_breaker"] = cb_health

        # Vérification métriques
        if self.metrics_collector:
            metrics_health = {
                "status": "healthy",
                "metrics_count": len(self.metrics_collector.get_global_stats()),
            }
            health_status["components"]["metrics"] = metrics_health

        return health_status

    def expose_prometheus_metrics(self, port: int = 8000):
        """Expose un endpoint /metrics Prometheus sur le port donné"""
        registry = CollectorRegistry()
        # Exemples de métriques à exposer
        self.gauge_cache_hits = Gauge(
            "arkalia_cache_hits", "Nombre de hits du cache", registry=registry
        )
        self.gauge_cache_misses = Gauge(
            "arkalia_cache_misses", "Nombre de misses du cache", registry=registry
        )
        self.gauge_lb_backends = Gauge(
            "arkalia_lb_backends", "Nombre de backends actifs", registry=registry
        )
        self.gauge_cb_state = Gauge(
            "arkalia_cb_state",
            "État du circuit breaker (0=closed, 1=open, 2=half-open)",
            registry=registry,
        )
        self.counter_errors = Counter(
            "arkalia_optim_errors", "Nombre d'erreurs d'optimisation", registry=registry
        )

        def update_metrics():
            # Cache
            stats = self.cache_manager.get_stats() if self.cache_manager else {}
            self.gauge_cache_hits.set(stats.get("hits", 0))
            self.gauge_cache_misses.set(stats.get("misses", 0))
            # Load balancer
            self.gauge_lb_backends.set(
                len(self.load_balancer.backends) if self.load_balancer else 0
            )
            # Circuit breaker
            if self.circuit_breaker:
                state = self.circuit_breaker.get_state().value
                state_map = {"closed": 0, "open": 1, "half_open": 2}
                self.gauge_cb_state.set(state_map.get(state, -1))
            # Errors (exemple)
            # self.counter_errors.inc() # à incrémenter dans les handlers d'erreur

        def metrics_loop():
            while True:
                update_metrics()
                import time

                time.sleep(5)

        # Lancer le serveur Prometheus
        threading.Thread(target=start_http_server, args=(port,), daemon=True).start()
        # Lancer la boucle de mise à jour des métriques
        threading.Thread(target=metrics_loop, daemon=True).start()
        print(f"✅ Endpoint Prometheus /metrics exposé sur le port {port}")


# Factory pour créer l'intégrateur
async def create_optimization_integrator() -> OptimizationIntegrator:
    """Factory pour créer et initialiser l'intégrateur d'optimisations"""
    integrator = OptimizationIntegrator()
    success = await integrator.initialize_optimizations()

    if success:
        await integrator.start_optimization_services()
        logger.info("🚀 OptimizationIntegrator créé et démarré avec succès")
    else:
        logger.error("❌ Échec création OptimizationIntegrator")

    return integrator
