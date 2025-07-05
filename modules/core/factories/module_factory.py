#!/usr/bin/env python3
"""
🏭 ModuleFactory - Factory SOLID pour modules du Core
🎯 Création dynamique de modules compatibles IModule
"""

import logging
from typing import Any, Optional

from ..interfaces.module_interface import IModule


class ModuleFactory:
    """
    🏭 Factory pour créer des modules compatibles IModule
    """

    def __init__(self):
        self.logger = logging.getLogger("arkalia.core.factory.module")
        self._registry: dict[str, type[IModule]] = {}
        self._register_default_modules()

    def _register_default_modules(self) -> None:
        """Enregistre les modules par défaut"""
        try:
            # Enregistrer les adaptateurs
            from ..adapters import (
                create_reflexia_adapter,
                create_sandozia_adapter,
                create_taskia_adapter,
                create_zeroia_adapter,
            )

            # Créer des instances pour obtenir les classes
            zeroia_adapter = create_zeroia_adapter()
            taskia_adapter = create_taskia_adapter()
            reflexia_adapter = create_reflexia_adapter()
            sandozia_adapter = create_sandozia_adapter()

            self.register_module_class("zeroia", type(zeroia_adapter))
            self.register_module_class("taskia", type(taskia_adapter))
            self.register_module_class("reflexia", type(reflexia_adapter))
            self.register_module_class("sandozia", type(sandozia_adapter))

            self.logger.info("✅ Modules par défaut enregistrés")

        except Exception as e:
            self.logger.error(f"❌ Erreur enregistrement modules par défaut: {e}")

    def register_module_class(self, name: str, module_cls: type[IModule]) -> bool:
        if name in self._registry:
            self.logger.warning(f"Classe module déjà enregistrée : {name}")
            return False
        self._registry[name] = module_cls
        self.logger.info(f"Classe module enregistrée : {name}")
        return True

    def unregister_module_class(self, name: str) -> bool:
        if name in self._registry:
            del self._registry[name]
            self.logger.info(f"Classe module désenregistrée : {name}")
            return True
        return False

    def create_module(self, name: str, **kwargs) -> IModule | None:
        if name not in self._registry:
            self.logger.error(f"Classe module inconnue : {name}")
            return None
        try:
            module = self._registry[name](**kwargs)
            self.logger.info(f"Instance module créée : {name}")
            return module
        except Exception as e:
            self.logger.error(f"Erreur création module {name} : {e}")
            return None
