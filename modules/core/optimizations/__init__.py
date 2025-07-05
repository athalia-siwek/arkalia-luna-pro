#!/usr/bin/env python3
"""
🚀 Optimisations Avancées - Module de performance
🎯 Cache intelligent, load balancing, circuit breaker et métriques
"""

from .advanced_metrics import (
    AdvancedMetricsManager,
    Alert,
    AlertManager,
    AlertRule,
    AlertSeverity,
    Metric,
    MetricType,
    get_metrics_manager,
    record_metric,
)
from .cache_manager import (
    CacheEntry,
    CacheLevel,
    CacheManager,
    cache_result,
    get_cache_manager,
)
from .circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerRegistry,
    CircuitState,
    circuit_breaker,
    get_circuit_breaker_registry,
)
from .load_balancer import (
    BackendNode,
    LoadBalancer,
    LoadBalancingStrategy,
    get_load_balancer,
    load_balanced_request,
)

__all__ = [
    # Cache Manager
    "CacheManager",
    "CacheLevel",
    "CacheEntry",
    "get_cache_manager",
    "cache_result",
    # Load Balancer
    "LoadBalancer",
    "LoadBalancingStrategy",
    "BackendNode",
    "get_load_balancer",
    "load_balanced_request",
    # Circuit Breaker
    "CircuitBreaker",
    "CircuitBreakerRegistry",
    "CircuitBreakerConfig",
    "CircuitState",
    "get_circuit_breaker_registry",
    "circuit_breaker",
    # Advanced Metrics
    "AdvancedMetricsManager",
    "Metric",
    "MetricType",
    "AlertManager",
    "AlertRule",
    "Alert",
    "AlertSeverity",
    "get_metrics_manager",
    "record_metric",
]
