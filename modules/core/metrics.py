"""
📊 Métriques Prometheus standardisées pour Core

Métriques requises :
- arkalia_module_name
- arkalia_uptime_seconds  
- arkalia_last_successful_interaction_timestamp
- arkalia_cognitive_score
"""

import time
from prometheus_client import Gauge, Counter, Histogram

# Métriques standardisées Arkalia-LUNA
arkalia_module_name = Gauge(
    "arkalia_module_name",
    "Nom du module Arkalia",
    ["module"]
)

arkalia_uptime_seconds = Gauge(
    "arkalia_uptime_seconds",
    "Temps de fonctionnement du module en secondes",
    ["module"]
)

arkalia_last_successful_interaction_timestamp = Gauge(
    "arkalia_last_successful_interaction_timestamp",
    "Timestamp de la dernière interaction réussie",
    ["module"]
)

arkalia_cognitive_score = Gauge(
    "arkalia_cognitive_score",
    "Score cognitif du module (0.0-1.0)",
    ["module"]
)

# Métriques spécifiques Core
core_orchestrations_total = Counter(
    "core_orchestrations_total",
    "Nombre total d'orchestrations",
    ["orchestration_type", "status"]
)

core_module_health_checks = Gauge(
    "core_module_health_checks",
    "État de santé des modules (1=healthy, 0=unhealthy)",
    ["module_name"]
)

core_configuration_changes = Counter(
    "core_configuration_changes_total",
    "Nombre de changements de configuration",
    ["config_type", "status"]
)

core_optimization_events = Counter(
    "core_optimization_events_total",
    "Nombre d'événements d'optimisation",
    ["optimization_type", "impact"]
)

core_storage_operations = Histogram(
    "core_storage_operation_duration_seconds",
    "Durée des opérations de stockage",
    ["operation_type"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# Initialisation des métriques standardisées
def init_core_metrics():
    """Initialise les métriques standardisées pour Core"""
    module_name = "core"
    
    # Définir le nom du module
    arkalia_module_name.labels(module=module_name).set(1)
    
    # Initialiser l'uptime
    start_time = time.time()
    arkalia_uptime_seconds.labels(module=module_name).set(start_time)
    
    # Initialiser le timestamp de dernière interaction
    arkalia_last_successful_interaction_timestamp.labels(module=module_name).set(start_time)
    
    # Initialiser le score cognitif (sera mis à jour par la logique)
    arkalia_cognitive_score.labels(module=module_name).set(0.75)

def update_core_metrics(operation_type: str, status: str, duration: float | None = None, cognitive_score: float | None = None):
    """Met à jour les métriques Core"""
    module_name = "core"
    
    # Mettre à jour l'uptime
    arkalia_uptime_seconds.labels(module=module_name).set(time.time())
    
    # Mettre à jour le timestamp de dernière interaction si succès
    if status == "success":
        arkalia_last_successful_interaction_timestamp.labels(module=module_name).set(time.time())
    
    # Mettre à jour le score cognitif si fourni
    if cognitive_score is not None:
        arkalia_cognitive_score.labels(module=module_name).set(cognitive_score)
    
    # Enregistrer la durée si fournie
    if duration is not None:
        core_storage_operations.labels(operation_type=operation_type).observe(duration)

def record_orchestration(orchestration_type: str, status: str):
    """Enregistre une orchestration"""
    core_orchestrations_total.labels(orchestration_type=orchestration_type, status=status).inc()

def update_module_health(module_name: str, is_healthy: bool):
    """Met à jour la santé d'un module"""
    core_module_health_checks.labels(module_name=module_name).set(1 if is_healthy else 0)

def record_configuration_change(config_type: str, status: str):
    """Enregistre un changement de configuration"""
    core_configuration_changes.labels(config_type=config_type, status=status).inc()

def record_optimization_event(optimization_type: str, impact: str):
    """Enregistre un événement d'optimisation"""
    core_optimization_events.labels(optimization_type=optimization_type, impact=impact).inc() 