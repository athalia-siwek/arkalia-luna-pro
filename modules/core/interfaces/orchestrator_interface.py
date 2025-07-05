#!/usr/bin/env python3
"""
🔗 Interface IOrchestrator - Principe SOLID SRP
🎯 Contrat pour l'orchestration des modules
🛡️ Responsabilité unique : Orchestration
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from .module_interface import IModule


class IOrchestrator(ABC):
    """
    🎯 Interface pour l'orchestration des modules
    🛡️ Principe SRP : Single Responsibility Principle
    """

    @abstractmethod
    def register_module(self, name: str, module: IModule) -> bool:
        """
        📝 Enregistrement d'un module
        :param name: Nom unique du module
        :param module: Instance du module
        :return: True si enregistrement réussi
        """
        pass

    @abstractmethod
    def unregister_module(self, name: str) -> bool:
        """
        🗑️ Désenregistrement d'un module
        :param name: Nom du module à désenregistrer
        :return: True si désenregistrement réussi
        """
        pass

    @abstractmethod
    def get_module(self, name: str) -> IModule | None:
        """
        🔍 Récupération d'un module
        :param name: Nom du module
        :return: Instance du module ou None
        """
        pass

    @abstractmethod
    def list_modules(self) -> list[str]:
        """
        📋 Liste des modules enregistrés
        :return: Liste des noms de modules
        """
        pass

    @abstractmethod
    def initialize_all_modules(self) -> dict[str, bool]:
        """
        🚀 Initialisation de tous les modules
        :return: Dictionnaire {nom_module: succès}
        """
        pass

    @abstractmethod
    def shutdown_all_modules(self) -> dict[str, bool]:
        """
        🔌 Arrêt de tous les modules
        :return: Dictionnaire {nom_module: succès}
        """
        pass

    @abstractmethod
    def health_check_all(self) -> dict[str, dict[str, Any]]:
        """
        🏥 Vérification de santé de tous les modules
        :return: Dictionnaire {nom_module: health_data}
        """
        pass

    @abstractmethod
    def get_system_status(self) -> dict[str, Any]:
        """
        📊 Statut global du système
        :return: Métriques système complètes
        """
        pass


class IOrchestratorWithDependencyManagement(IOrchestrator):
    """
    🔗 Interface étendue pour gestion des dépendances
    🎯 Orchestrateur avec résolution automatique des dépendances
    """

    @abstractmethod
    def resolve_dependencies(self) -> dict[str, list[str]]:
        """
        🔍 Résolution des dépendances entre modules
        :return: Dictionnaire {module: [dépendances]}
        """
        pass

    @abstractmethod
    def get_dependency_graph(self) -> dict[str, list[str]]:
        """
        📊 Graphe des dépendances
        :return: Représentation des dépendances
        """
        pass

    @abstractmethod
    def validate_dependencies(self) -> bool:
        """
        ✅ Validation de toutes les dépendances
        :return: True si toutes les dépendances sont satisfaites
        """
        pass


class IOrchestratorWithLifecycle(IOrchestrator):
    """
    🔄 Interface étendue pour gestion du cycle de vie
    🎯 Orchestrateur avec contrôle du cycle de vie
    """

    @abstractmethod
    def start_module(self, name: str) -> bool:
        """
        ▶️ Démarrage d'un module
        :param name: Nom du module
        :return: True si démarrage réussi
        """
        pass

    @abstractmethod
    def stop_module(self, name: str) -> bool:
        """
        ⏹️ Arrêt d'un module
        :param name: Nom du module
        :return: True si arrêt réussi
        """
        pass

    @abstractmethod
    def restart_module(self, name: str) -> bool:
        """
        🔄 Redémarrage d'un module
        :param name: Nom du module
        :return: True si redémarrage réussi
        """
        pass

    @abstractmethod
    def get_module_status(self, name: str) -> str:
        """
        📊 Statut d'un module
        :param name: Nom du module
        :return: Statut (running, stopped, error, etc.)
        """
        pass
