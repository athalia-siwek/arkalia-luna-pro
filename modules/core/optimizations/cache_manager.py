#!/usr/bin/env python3
"""
🧠 Cache Manager - Gestionnaire de cache intelligent
🎯 Optimisation des performances avec cache multi-niveaux
"""

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional, Union

logger = logging.getLogger(__name__)


class CacheLevel(Enum):
    """Niveaux de cache"""

    L1 = "l1"  # Cache mémoire rapide
    L2 = "l2"  # Cache persistant
    L3 = "l3"  # Cache distribué (futur)


@dataclass
class CacheEntry:
    """Entrée de cache avec métadonnées"""

    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    accessed_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    ttl: timedelta | None = None
    level: CacheLevel = CacheLevel.L1

    def is_expired(self) -> bool:
        """Vérifie si l'entrée a expiré"""
        if self.ttl is None:
            return False
        return datetime.now() > self.created_at + self.ttl

    def access(self) -> None:
        """Marque l'entrée comme accédée"""
        self.accessed_at = datetime.now()
        self.access_count += 1

    def to_dict(self) -> dict[str, Any]:
        """Convertit en dictionnaire"""
        return {
            "key": self.key,
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "accessed_at": self.accessed_at.isoformat(),
            "access_count": self.access_count,
            "ttl": self.ttl.total_seconds() if self.ttl else None,
            "level": self.level.value,
            "is_expired": self.is_expired(),
        }


class CacheManager:
    """
    🧠 Gestionnaire de cache intelligent multi-niveaux
    🎯 Optimisation automatique des performances
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {
            "l1_max_size": 1000,
            "l2_max_size": 10000,
            "default_ttl": 300,  # 5 minutes
            "cleanup_interval": 60,  # 1 minute
            "enable_metrics": True,
        }

        # Caches par niveau
        self.l1_cache: dict[str, CacheEntry] = {}
        self.l2_cache: dict[str, CacheEntry] = {}

        # Métriques
        self.metrics = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "total_requests": 0,
        }

        # Dernier nettoyage
        self.last_cleanup = datetime.now()

        logger.info("🧠 CacheManager initialisé")

    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur du cache"""
        self.metrics["total_requests"] += 1

        # Essayer L1 d'abord
        if key in self.l1_cache:
            entry = self.l1_cache[key]
            if not entry.is_expired():
                entry.access()
                self.metrics["hits"] += 1
                logger.debug(f"🧠 Cache L1 hit: {key}")
                return entry.value
            else:
                del self.l1_cache[key]

        # Essayer L2
        if key in self.l2_cache:
            entry = self.l2_cache[key]
            if not entry.is_expired():
                entry.access()
                # Promouvoir vers L1
                self._promote_to_l1(key, entry)
                self.metrics["hits"] += 1
                logger.debug(f"🧠 Cache L2 hit: {key}")
                return entry.value
            else:
                del self.l2_cache[key]

        self.metrics["misses"] += 1
        logger.debug(f"🧠 Cache miss: {key}")
        return default

    def set(
        self, key: str, value: Any, ttl: int | None = None, level: CacheLevel = CacheLevel.L1
    ) -> bool:
        """Stocke une valeur dans le cache"""
        try:
            # Nettoyer si nécessaire
            self._cleanup_if_needed()

            # Créer l'entrée
            ttl_delta = timedelta(seconds=ttl or self.config["default_ttl"])
            entry = CacheEntry(
                key=key,
                value=value,
                ttl=ttl_delta,
                level=level,
            )

            # Stocker selon le niveau
            if level == CacheLevel.L1:
                if len(self.l1_cache) >= self.config["l1_max_size"]:
                    self._evict_l1()
                self.l1_cache[key] = entry
            elif level == CacheLevel.L2:
                if len(self.l2_cache) >= self.config["l2_max_size"]:
                    self._evict_l2()
                self.l2_cache[key] = entry

            logger.debug(f"🧠 Cache set: {key} (level: {level.value})")
            return True

        except Exception as e:
            logger.error(f"❌ Erreur cache set: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Supprime une entrée du cache"""
        try:
            deleted = False
            if key in self.l1_cache:
                del self.l1_cache[key]
                deleted = True
            if key in self.l2_cache:
                del self.l2_cache[key]
                deleted = True

            if deleted:
                logger.debug(f"🧠 Cache delete: {key}")

            return deleted

        except Exception as e:
            logger.error(f"❌ Erreur cache delete: {e}")
            return False

    def clear(self, level: CacheLevel | None = None) -> bool:
        """Vide le cache"""
        try:
            if level is None or level == CacheLevel.L1:
                self.l1_cache.clear()
            if level is None or level == CacheLevel.L2:
                self.l2_cache.clear()

            logger.info(f"🧠 Cache cleared (level: {level.value if level else 'all'})")
            return True

        except Exception as e:
            logger.error(f"❌ Erreur cache clear: {e}")
            return False

    def get_stats(self) -> dict[str, Any]:
        """Récupère les statistiques du cache"""
        total_requests = self.metrics["total_requests"]
        hit_rate = self.metrics["hits"] / total_requests * 100 if total_requests > 0 else 0.0

        return {
            "l1_size": len(self.l1_cache),
            "l2_size": len(self.l2_cache),
            "total_size": len(self.l1_cache) + len(self.l2_cache),
            "hits": self.metrics["hits"],
            "misses": self.metrics["misses"],
            "evictions": self.metrics["evictions"],
            "total_requests": total_requests,
            "hit_rate": round(hit_rate, 2),
            "last_cleanup": self.last_cleanup.isoformat(),
        }

    def _cleanup_if_needed(self) -> None:
        """Nettoie le cache si nécessaire"""
        now = datetime.now()
        if (now - self.last_cleanup).total_seconds() < self.config["cleanup_interval"]:
            return

        self._cleanup()
        self.last_cleanup = now

    def _cleanup(self) -> None:
        """Nettoie les entrées expirées"""
        # Nettoyer L1
        expired_keys = [key for key, entry in self.l1_cache.items() if entry.is_expired()]
        for key in expired_keys:
            del self.l1_cache[key]

        # Nettoyer L2
        expired_keys = [key for key, entry in self.l2_cache.items() if entry.is_expired()]
        for key in expired_keys:
            del self.l2_cache[key]

        if expired_keys:
            logger.debug(f"🧠 Cache cleanup: {len(expired_keys)} entrées expirées")

    def _evict_l1(self) -> None:
        """Évince une entrée de L1 (LRU)"""
        if not self.l1_cache:
            return

        # Trouver l'entrée la moins récemment utilisée
        lru_key = min(self.l1_cache.keys(), key=lambda k: self.l1_cache[k].accessed_at)

        # Déplacer vers L2 si possible
        entry = self.l1_cache[lru_key]
        if len(self.l2_cache) < self.config["l2_max_size"]:
            self.l2_cache[lru_key] = entry
            logger.debug(f"🧠 Cache L1->L2: {lru_key}")
        else:
            # Évincer de L2 aussi si nécessaire
            self._evict_l2()
            self.l2_cache[lru_key] = entry

        del self.l1_cache[lru_key]
        self.metrics["evictions"] += 1

    def _evict_l2(self) -> None:
        """Évince une entrée de L2 (LRU)"""
        if not self.l2_cache:
            return

        # Trouver l'entrée la moins récemment utilisée
        lru_key = min(self.l2_cache.keys(), key=lambda k: self.l2_cache[k].accessed_at)

        del self.l2_cache[lru_key]
        self.metrics["evictions"] += 1
        logger.debug(f"🧠 Cache L2 eviction: {lru_key}")

    def _promote_to_l1(self, key: str, entry: CacheEntry) -> None:
        """Promouvoit une entrée de L2 vers L1"""
        if len(self.l1_cache) >= self.config["l1_max_size"]:
            self._evict_l1()

        self.l1_cache[key] = entry
        logger.debug(f"🧠 Cache L2->L1 promotion: {key}")


# Instance globale
_cache_manager: CacheManager | None = None


def get_cache_manager() -> CacheManager:
    """Récupère l'instance globale du cache manager"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def cache_result(ttl: int | None = None, level: CacheLevel = CacheLevel.L1):
    """Décorateur pour mettre en cache le résultat d'une fonction"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_manager = get_cache_manager()

            # Créer une clé unique basée sur la fonction et ses arguments
            import hashlib

            key_parts = [func.__name__, str(args), str(sorted(kwargs.items()))]
            key = hashlib.md5(":".join(key_parts).encode(), usedforsecurity=False).hexdigest()

            # Essayer de récupérer du cache
            cached_result = cache_manager.get(key)
            if cached_result is not None:
                return cached_result

            # Exécuter la fonction et mettre en cache
            result = func(*args, **kwargs)
            cache_manager.set(key, result, ttl, level)

            return result

        return wrapper

    return decorator
