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
import sqlite3
import time
from dataclasses import dataclass
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
            "version": self.version,
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
            version=data.get("version", "1.0"),
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

    def __init__(
        self, cache_dir: str = "./cache/zeroia_events", size_limit: int = 100_000_000
    ):
        """
        Initialise l'Event Store avec gestion d'erreur robuste

        Args:
            cache_dir: Répertoire de cache
            size_limit: Limite de taille du cache
        """
        self.cache_dir = cache_dir

        # Créer le répertoire s'il n'existe pas
        Path(cache_dir).mkdir(parents=True, exist_ok=True)

        # Initialiser les caches avec gestion d'erreur
        self.events_cache = self._initialize_cache(f"{cache_dir}/events", size_limit)
        self.type_index = self._initialize_cache(
            f"{cache_dir}/type_index", size_limit // 10
        )

        # Compteur d'événements
        self.event_counter = 0
        self._load_counter()

        logger.info(
            f"🗄️ EventStore initialisé: {cache_dir}, compteur: {self.event_counter}"
        )

    def _initialize_cache(self, cache_path: str, size_limit: int) -> Cache:
        """Initialise un cache avec gestion d'erreur pour corruption SQLite"""
        try:
            return Cache(cache_path, size_limit=size_limit)
        except sqlite3.DatabaseError:
            logger.warning(f"🔧 Cache corrompu détecté: {cache_path}, recréation...")

            # Supprimer le cache corrompu de façon plus robuste
            self._safe_remove_cache(cache_path)

            # Recréer le cache
            Path(cache_path).mkdir(parents=True, exist_ok=True)
            return Cache(cache_path, size_limit=size_limit)
        except Exception as e:
            logger.error(f"❌ Erreur inattendue initialisation cache {cache_path}: {e}")
            # Fallback: créer un cache temporaire
            import tempfile

            temp_dir = tempfile.mkdtemp()
            logger.warning(f"🔧 Utilisation cache temporaire: {temp_dir}")
            return Cache(temp_dir, size_limit=size_limit)

    def _safe_remove_cache(self, cache_path: str) -> None:
        """Supprime un cache de façon sécurisée en ignorant les fichiers cachés macOS"""
        import os
        import shutil

        if not Path(cache_path).exists():
            return

        try:
            # Supprimer d'abord les fichiers cachés macOS qui causent des problèmes
            for root, dirs, files in os.walk(cache_path):
                for file in files:
                    if file.startswith("._"):
                        try:
                            os.remove(os.path.join(root, file))
                        except FileNotFoundError:
                            pass  # Ignorer si déjà supprimé

            # Maintenant supprimer le répertoire
            shutil.rmtree(cache_path, ignore_errors=True)

        except Exception as e:
            logger.warning(
                f"⚠️ Erreur suppression cache {cache_path}: {e}, continuons..."
            )

            # Fallback: renommer le répertoire pour l'ignorer
            try:
                backup_path = f"{cache_path}_corrupted_{int(time.time())}"
                os.rename(cache_path, backup_path)
                logger.warning(f"🔄 Cache renommé vers {backup_path}")
            except Exception:
                pass  # Ignorer si même le renommage échoue

    def add_event(
        self,
        event_type: EventType,
        data: Dict[str, Any],
        module: str = "zeroia",
        correlation_id: Optional[str] = None,
    ) -> str:
        """
        Ajoute un événement au store avec gestion d'erreur robuste

        Args:
            event_type: Type d'événement
            data: Données de l'événement
            module: Module source
            correlation_id: ID de corrélation

        Returns:
            ID de l'événement créé
        """
        # Format attendu par les tests: module_eventtype_counter
        event_id = f"{module}_{event_type.value}_{self.event_counter:06d}"
        self.event_counter += 1

        event = Event(
            id=event_id,
            event_type=event_type,
            timestamp=datetime.now(),
            module=module,
            data=data,
            correlation_id=correlation_id,
        )

        # Stocker dans le cache avec gestion d'erreur SQLite
        try:
            self.events_cache[event_id] = event.to_dict()
        except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
            logger.warning(f"⚠️ Erreur cache événement {event_id}: {e}")
            # Continuer sans stocker - l'événement sera perdu mais le système continue
            return event_id

        # Mettre à jour l'index par type
        try:
            self._update_type_index(event_type, event_id)
        except Exception as e:
            logger.warning(f"⚠️ Erreur index type {event_type}: {e}")

        # Sauvegarder le compteur
        try:
            self._save_counter()
        except Exception as e:
            logger.warning(f"⚠️ Erreur sauvegarde compteur: {e}")

        return event_id

    def get_event(self, event_id: str) -> Optional[Event]:
        """Récupère un événement par son ID"""
        try:
            event_data = self.events_cache.get(event_id)
            if event_data and isinstance(event_data, dict):
                return Event.from_dict(event_data)
        except Exception as e:
            logger.warning(f"Erreur récupération événement {event_id}: {e}")
        return None

    def get_events_by_type(
        self, event_type: EventType, limit: int = 100, since: Optional[datetime] = None
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
        try:
            event_ids_data = self.type_index.get(event_type.value, [])
            # S'assurer que c'est une liste
            if not isinstance(event_ids_data, list):
                return []

            events = []
            for event_id in reversed(
                event_ids_data[-limit:]
            ):  # Plus récents en premier
                if isinstance(event_id, str):
                    event = self.get_event(event_id)
                    if event:
                        if since and event.timestamp < since:
                            continue
                        events.append(event)

            return events
        except Exception as e:
            logger.warning(f"Erreur récupération événements par type {event_type}: {e}")
            return []

    def get_recent_events(self, limit: int = 50) -> List[Event]:
        """
        Récupère les événements récents

        Args:
            limit: Nombre max d'événements

        Returns:
            Liste d'événements triée par timestamp décroissant
        """
        all_events = []

        # Utiliser l'approche correcte pour diskcache - parcours sécurisé
        try:
            # Parcourir le cache de manière sécurisée
            for key in self.events_cache:
                if isinstance(key, str) and key.startswith(
                    ("zeroia_", "reflexia_", "sandozia_")
                ):
                    try:
                        value = self.events_cache.get(key)
                        if value and isinstance(value, dict):
                            event = Event.from_dict(value)
                            all_events.append(event)
                    except Exception as e:
                        # Ignorer les événements corrompus
                        logger.warning(f"Event corrompu ignoré {key}: {e}")
                        continue
        except Exception as e:
            logger.error(f"Erreur accès cache events: {e}")
            return []

        # Trier par timestamp décroissant et limiter
        all_events.sort(key=lambda x: x.timestamp, reverse=True)
        return all_events[:limit]

    def get_events_by_module(self, module: str, limit: int = 100) -> List[Event]:
        """Récupère les événements par module"""
        events = []

        try:
            for key in self.events_cache:
                if isinstance(key, str) and key.startswith(f"{module}_"):
                    event = self.get_event(key)
                    if event and len(events) < limit:
                        events.append(event)
        except Exception as e:
            logger.warning(f"Erreur récupération événements module {module}: {e}")

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
            EventType.CALL_BLOCKED,
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
            "anomalies": [],
        }

        # Détecter trop d'échecs
        failures = [
            e for e in recent_events if e.event_type == EventType.CIRCUIT_FAILURE
        ]
        if len(failures) > 5:
            anomalies["anomalies"].append(
                {
                    "type": "high_failure_rate",
                    "severity": "high",
                    "count": len(failures),
                    "description": f"{len(failures)} échecs circuit en {window_minutes}min",
                }
            )

        # Détecter erreurs système
        errors = [e for e in recent_events if e.event_type == EventType.SYSTEM_ERROR]
        if len(errors) > 2:
            anomalies["anomalies"].append(
                {
                    "type": "system_errors",
                    "severity": "critical",
                    "count": len(errors),
                    "description": f"{len(errors)} erreurs système en {window_minutes}min",
                }
            )

        # Détecter contradictions
        contradictions = [
            e for e in recent_events if e.event_type == EventType.CONTRADICTION_DETECTED
        ]
        if len(contradictions) > 3:
            anomalies["anomalies"].append(
                {
                    "type": "high_contradictions",
                    "severity": "medium",
                    "count": len(contradictions),
                    "description": f"{len(contradictions)} contradictions IA en {window_minutes}min",
                }
            )

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

        # Calculer les tailles de cache de manière sécurisée
        try:
            events_cache_size = 0
            for _ in self.events_cache:
                events_cache_size += 1
        except Exception:
            events_cache_size = 0

        try:
            type_index_size = 0
            for _ in self.type_index:
                type_index_size += 1
        except Exception:
            type_index_size = 0

        return {
            "total_events": self.event_counter,
            "recent_events_analyzed": len(recent_events),
            "events_by_type": type_counts,
            "events_by_module": module_counts,
            "events_by_hour": hourly_counts,
            "cache_info": {
                "events_cache_size": events_cache_size,
                "type_index_size": type_index_size,
            },
        }

    def _update_type_index(self, event_type: EventType, event_id: str) -> None:
        """Met à jour l'index par type d'événement"""
        try:
            type_key = event_type.value
            current_ids_data = self.type_index.get(type_key, [])

            # S'assurer que c'est une liste
            if isinstance(current_ids_data, list):
                current_ids = current_ids_data
            else:
                current_ids = []

            current_ids.append(event_id)

            # Garder seulement les 1000 derniers IDs par type
            if len(current_ids) > 1000:
                current_ids = current_ids[-1000:]

            self.type_index[type_key] = current_ids
        except Exception as e:
            logger.warning(f"Erreur mise à jour index type {event_type}: {e}")

    def _load_counter(self) -> None:
        """Charge le compteur d'événements"""
        try:
            counter_data = self.events_cache.get("_event_counter", 0)
            # S'assurer que le compteur est toujours un entier
            if isinstance(counter_data, int):
                self.event_counter = counter_data
            elif isinstance(counter_data, str) and counter_data.isdigit():
                self.event_counter = int(counter_data)
            else:
                self.event_counter = 0
        except Exception:
            # Si erreur, repartir de 0
            self.event_counter = 0

    def _save_counter(self) -> None:
        """Sauvegarde le compteur d'événements"""
        try:
            self.events_cache["_event_counter"] = self.event_counter
        except Exception as e:
            logger.warning(f"Erreur sauvegarde compteur: {e}")

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

        try:
            # Récupérer toutes les clés du cache de manière sécurisée
            keys_to_check = []
            for key in self.events_cache:
                if isinstance(key, str) and key.startswith("event_"):
                    keys_to_check.append(key)

            for key in keys_to_check:
                event = self.get_event(key)
                if event and event.timestamp < cutoff_date:
                    try:
                        del self.events_cache[key]
                        deleted_count += 1
                    except Exception:
                        continue
        except Exception as e:
            logger.warning(f"Erreur nettoyage événements: {e}")

        logger.info(
            f"📋 Nettoyage EventStore: {deleted_count} événements supprimés (> {days_to_keep} jours)"
        )
        return deleted_count

    def export_events(
        self, filepath: Path, event_type: Optional[EventType] = None
    ) -> int:
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
            "events": [event.to_dict() for event in events],
        }

        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        logger.info(f"📋 Export EventStore: {len(events)} événements → {filepath}")
        return len(events)
