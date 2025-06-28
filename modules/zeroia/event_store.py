#!/usr/bin/env python3
# 📋 modules/zeroia/event_store.py
# Event Sourcing pour ZeroIA

"""
Event Store pour ZeroIA - Traçabilité complète des décisions

Fonctionnalités :
- Event sourcing complet des décisions IA
- Stockage persistant avec diskcache
- Requêtes et analytics sur les événements
- Détection de patterns et anomalies
- Audit trail complet
"""

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from diskcache import Cache

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types d'événements dans ZeroIA"""
    DECISION_MADE = "decision_made"
    CIRCUIT_SUCCESS = "circuit_success"
    CIRCUIT_FAILURE = "circuit_failure"
    STATE_CHANGE = "state_change"
    CALL_BLOCKED = "call_blocked"
    MANUAL_RESET = "manual_reset"
    SYSTEM_ERROR = "system_error"
    CONFIDENCE_UPDATE = "confidence_update"
    THRESHOLD_ADJUSTED = "threshold_adjusted"
    CONTRADICTION_DETECTED = "contradiction_detected"


@dataclass
class Event:
    """Événement dans le système ZeroIA"""
    id: str
    event_type: EventType
    timestamp: datetime
    module: str
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'événement en dictionnaire"""
        return {
            "id": self.id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "module": self.module,
            "data": self.data,
            "correlation_id": self.correlation_id,
            "version": self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Crée un événement depuis un dictionnaire"""
        return cls(
            id=data["id"],
            event_type=EventType(data["event_type"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            module=data["module"],
            data=data["data"],
            correlation_id=data.get("correlation_id"),
            version=data.get("version", "1.0")
        )


class EventStore:
    """
    Event Store pour ZeroIA
    
    Stocke et gère tous les événements du système avec :
    - Persistance sur disque (diskcache)
    - Requêtes par type, période, module
    - Analytics et métriques
    - Détection d'anomalies
    """
    
    def __init__(self, cache_dir: str = "./cache/zeroia_events", size_limit: int = 100_000_000):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache principal pour les événements
        self.events_cache = Cache(
            str(self.cache_dir / "events"),
            size_limit=size_limit
        )
        
        # Index par type d'événement pour recherches rapides
        self.type_index = Cache(
            str(self.cache_dir / "type_index"),
            size_limit=10_000_000
        )
        
        # Compteurs et métriques
        self.event_counter = 0
        self._load_counter()
        
        logger.info(f"📋 EventStore initialisé: {cache_dir} ({self.event_counter} événements)")
    
    def add_event(
        self,
        event_type: EventType,
        data: Dict[str, Any],
        module: str = "zeroia",
        correlation_id: Optional[str] = None
    ) -> str:
        """
        Ajoute un nouvel événement
        
        Args:
            event_type: Type d'événement
            data: Données de l'événement
            module: Module source
            correlation_id: ID de corrélation optionnel
            
        Returns:
            ID de l'événement créé
        """
        # Générer un ID unique
        self.event_counter += 1
        event_id = f"{module}_{event_type.value}_{self.event_counter}_{int(datetime.now().timestamp())}"
        
        # Créer l'événement
        event = Event(
            id=event_id,
            event_type=event_type,
            timestamp=datetime.now(),
            module=module,
            data=data,
            correlation_id=correlation_id
        )
        
        # Stocker dans le cache principal
        self.events_cache[event_id] = event.to_dict()
        
        # Mettre à jour l'index par type
        self._update_type_index(event_type, event_id)
        
        # Sauvegarder le compteur
        self._save_counter()
        
        logger.debug(f"📋 Événement ajouté: {event_type.value} ({event_id})")
        return event_id
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """Récupère un événement par son ID"""
        event_data = self.events_cache.get(event_id)
        if event_data:
            return Event.from_dict(event_data)
        return None
    
    def get_events_by_type(
        self,
        event_type: EventType,
        limit: int = 100,
        since: Optional[datetime] = None
    ) -> List[Event]:
        """
        Récupère les événements par type
        
        Args:
            event_type: Type d'événement
            limit: Nombre maximum d'événements
            since: Date de début (optionnel)
            
        Returns:
            Liste des événements
        """
        event_ids = self.type_index.get(event_type.value, [])
        events = []
        
        for event_id in reversed(event_ids[-limit:]):  # Plus récents en premier
            event = self.get_event(event_id)
            if event:
                if since and event.timestamp < since:
                    continue
                events.append(event)
        
        return events
    
    def get_recent_events(self, limit: int = 50) -> List[Event]:
        """
        Récupère les événements récents
        
        Args:
            limit: Nombre max d'événements
            
        Returns:
            Liste d'événements triée par timestamp décroissant
        """
        all_events = []
        
        # Récupérer tous les événements du cache
        for key in list(self.events_cache):
            if key.startswith("event_"):
                event = self.get_event(key)
                if event:
                    all_events.append(event)
        
        # Trier par timestamp décroissant (plus récent en premier)
        all_events.sort(key=lambda x: x.timestamp, reverse=True)
        
        return all_events[:limit]
    
    def get_events_by_module(self, module: str, limit: int = 100) -> List[Event]:
        """Récupère les événements par module"""
        events = []
        
        for key in self.events_cache:
            if isinstance(key, str) and key.startswith(f"{module}_"):
                event = self.get_event(key)
                if event and len(events) < limit:
                    events.append(event)
        
        # Trier par timestamp décroissant
        events.sort(key=lambda x: x.timestamp, reverse=True)
        return events[:limit]
    
    def get_decision_history(self, limit: int = 50) -> List[Event]:
        """Récupère l'historique des décisions"""
        return self.get_events_by_type(EventType.DECISION_MADE, limit)
    
    def get_system_health_events(self, limit: int = 20) -> List[Event]:
        """Récupère les événements de santé système"""
        health_types = [
            EventType.CIRCUIT_FAILURE,
            EventType.SYSTEM_ERROR,
            EventType.STATE_CHANGE,
            EventType.CALL_BLOCKED
        ]
        
        all_health_events = []
        for event_type in health_types:
            events = self.get_events_by_type(event_type, limit=10)
            all_health_events.extend(events)
        
        # Trier par timestamp décroissant
        all_health_events.sort(key=lambda x: x.timestamp, reverse=True)
        return all_health_events[:limit]
    
    def detect_anomalies(self, window_minutes: int = 60) -> Dict[str, Any]:
        """
        Détecte des anomalies dans les événements récents
        
        Args:
            window_minutes: Fenêtre d'analyse en minutes
            
        Returns:
            Rapport d'anomalies
        """
        since = datetime.now() - timedelta(minutes=window_minutes)
        recent_events = self.get_recent_events(limit=200)
        
        # Filtrer les événements récents
        recent_events = [e for e in recent_events if e.timestamp >= since]
        
        anomalies = {
            "window_minutes": window_minutes,
            "total_events": len(recent_events),
            "anomalies": []
        }
        
        # Détecter trop d'échecs
        failures = [e for e in recent_events if e.event_type == EventType.CIRCUIT_FAILURE]
        if len(failures) > 5:
            anomalies["anomalies"].append({
                "type": "high_failure_rate",
                "severity": "high",
                "count": len(failures),
                "description": f"{len(failures)} échecs circuit en {window_minutes}min"
            })
        
        # Détecter erreurs système
        errors = [e for e in recent_events if e.event_type == EventType.SYSTEM_ERROR]
        if len(errors) > 2:
            anomalies["anomalies"].append({
                "type": "system_errors",
                "severity": "critical",
                "count": len(errors),
                "description": f"{len(errors)} erreurs système en {window_minutes}min"
            })
        
        # Détecter contradictions
        contradictions = [e for e in recent_events if e.event_type == EventType.CONTRADICTION_DETECTED]
        if len(contradictions) > 3:
            anomalies["anomalies"].append({
                "type": "high_contradictions",
                "severity": "medium",
                "count": len(contradictions),
                "description": f"{len(contradictions)} contradictions IA en {window_minutes}min"
            })
        
        return anomalies
    
    def get_analytics(self) -> Dict[str, Any]:
        """Génère des analytics sur les événements"""
        recent_events = self.get_recent_events(limit=1000)
        
        # Compteurs par type
        type_counts = {}
        for event in recent_events:
            type_name = event.event_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        # Compteurs par module
        module_counts = {}
        for event in recent_events:
            module_counts[event.module] = module_counts.get(event.module, 0) + 1
        
        # Événements récents par heure
        hourly_counts = {}
        for event in recent_events:
            hour_key = event.timestamp.strftime("%Y-%m-%d %H:00")
            hourly_counts[hour_key] = hourly_counts.get(hour_key, 0) + 1
        
        return {
            "total_events": self.event_counter,
            "recent_events_analyzed": len(recent_events),
            "events_by_type": type_counts,
            "events_by_module": module_counts,
            "events_by_hour": hourly_counts,
            "cache_info": {
                "events_cache_size": len(self.events_cache),
                "type_index_size": len(self.type_index)
            }
        }
    
    def _update_type_index(self, event_type: EventType, event_id: str) -> None:
        """Met à jour l'index par type d'événement"""
        type_key = event_type.value
        current_ids = self.type_index.get(type_key, [])
        current_ids.append(event_id)
        
        # Garder seulement les 1000 derniers IDs par type
        if len(current_ids) > 1000:
            current_ids = current_ids[-1000:]
        
        self.type_index[type_key] = current_ids
    
    def _load_counter(self) -> None:
        """Charge le compteur d'événements"""
        counter_data = self.events_cache.get("_event_counter", 0)
        self.event_counter = counter_data
    
    def _save_counter(self) -> None:
        """Sauvegarde le compteur d'événements"""
        self.events_cache["_event_counter"] = self.event_counter
    
    def clear_old_events(self, days_to_keep: int = 30) -> int:
        """
        Nettoie les anciens événements
        
        Args:
            days_to_keep: Nombre de jours à conserver
            
        Returns:
            Nombre d'événements supprimés
        """
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted_count = 0
        
        # Récupérer toutes les clés du cache
        for key in list(self.events_cache):
            if key.startswith("event_"):
                event = self.get_event(key)
                if event and event.timestamp < cutoff_date:
                    del self.events_cache[key]
                    deleted_count += 1
        
        logger.info(f"📋 Nettoyage EventStore: {deleted_count} événements supprimés (> {days_to_keep} jours)")
        return deleted_count
    
    def export_events(self, filepath: Path, event_type: Optional[EventType] = None) -> int:
        """
        Exporte les événements vers un fichier JSON
        
        Args:
            filepath: Chemin du fichier d'export
            event_type: Type d'événement à exporter (tous si None)
            
        Returns:
            Nombre d'événements exportés
        """
        if event_type:
            events = self.get_events_by_type(event_type, limit=10000)
        else:
            events = self.get_recent_events(limit=10000)
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "event_type_filter": event_type.value if event_type else "all",
            "total_events": len(events),
            "events": [event.to_dict() for event in events]
        }
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📋 Export EventStore: {len(events)} événements → {filepath}")
        return len(events) 