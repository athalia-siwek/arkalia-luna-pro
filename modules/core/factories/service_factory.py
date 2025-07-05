#!/usr/bin/env python3
"""
🏭 ServiceFactory - Factory SOLID pour services du Core
🎯 Injection de dépendances et création de services
"""

import logging
from typing import Any, Optional


class ServiceFactory:
    """
    🏭 Factory pour créer et injecter des services du Core
    """

    def __init__(self):
        self.logger = logging.getLogger("arkalia.core.factory.service")
        self._services: dict[str, Any] = {}
        self._registry: dict[str, type] = {}

    def register_service_class(self, name: str, service_cls: type) -> bool:
        if name in self._registry:
            self.logger.warning(f"Classe service déjà enregistrée : {name}")
            return False
        self._registry[name] = service_cls
        self.logger.info(f"Classe service enregistrée : {name}")
        return True

    def unregister_service_class(self, name: str) -> bool:
        if name in self._registry:
            del self._registry[name]
            self.logger.info(f"Classe service désenregistrée : {name}")
            return True
        return False

    def get_service(self, name: str) -> Any | None:
        return self._services.get(name)

    def create_service(self, name: str, **kwargs) -> Any | None:
        if name not in self._registry:
            self.logger.error(f"Classe service inconnue : {name}")
            return None
        try:
            service = self._registry[name](**kwargs)
            self._services[name] = service
            self.logger.info(f"Instance service créée : {name}")
            return service
        except Exception as e:
            self.logger.error(f"Erreur création service {name} : {e}")
            return None
