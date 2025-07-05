"""
📊 Métriques Prometheus standardisées pour Cognitive Reactor

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

# Métriques spécifiques Cognitive Reactor
cognitive_reactions_total = Counter(
    "cognitive_reactions_total",
    "Nombre total de réactions cognitives",
    ["reaction_type", "status"]
)

cognitive_quarantine_events = Counter(
    "cognitive_quarantine_events_total",
    "Nombre d'événements de quarantaine",
    ["quarantine_type", "reason"]
)

cognitive_learning_progress = Gauge(
    "cognitive_learning_progress",
    "Progression de l'apprentissage (0.0-1.0)",
    ["learning_type"]
)

cognitive_pattern_detections = Counter(
    "cognitive_pattern_detections_total",
    "Nombre de détections de patterns",
    ["pattern_type", "confidence"]
)

cognitive_reaction_duration = Histogram(
    "cognitive_reaction_duration_seconds",
    "Durée des réactions cognitives",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# Initialisation des métriques standardisées
def init_cognitive_metrics():
    """Initialise les métriques standardisées pour Cognitive Reactor"""
    module_name = "cognitive_reactor"
    
    # Définir le nom du module
    arkalia_module_name.labels(module=module_name).set(1)
    
    # Initialiser l'uptime
    start_time = time.time()
    arkalia_uptime_seconds.labels(module=module_name).set(start_time)
    
    # Initialiser le timestamp de dernière interaction
    arkalia_last_successful_interaction_timestamp.labels(module=module_name).set(start_time)
    
    # Initialiser le score cognitif (sera mis à jour par la logique)
    arkalia_cognitive_score.labels(module=module_name).set(0.88)

def update_cognitive_metrics(reaction_type: str, status: str, duration: float | None = None, cognitive_score: float | None = None):
    """Met à jour les métriques Cognitive Reactor"""
    module_name = "cognitive_reactor"
    
    # Incrémenter le compteur de réactions
    cognitive_reactions_total.labels(reaction_type=reaction_type, status=status).inc()
    
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
        cognitive_reaction_duration.observe(duration)

def record_quarantine_event(quarantine_type: str, reason: str):
    """Enregistre un événement de quarantaine"""
    cognitive_quarantine_events.labels(quarantine_type=quarantine_type, reason=reason).inc()

def update_learning_progress(learning_type: str, progress: float):
    """Met à jour la progression de l'apprentissage"""
    cognitive_learning_progress.labels(learning_type=learning_type).set(progress)

def record_pattern_detection(pattern_type: str, confidence: str):
    """Enregistre une détection de pattern"""
    cognitive_pattern_detections.labels(pattern_type=pattern_type, confidence=confidence).inc() 