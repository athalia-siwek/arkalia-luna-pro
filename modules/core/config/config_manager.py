#!/usr/bin/env python3
"""
🔧 ConfigManager - Gestion intelligente de la configuration
🎯 Principe SOLID SRP : Responsabilité unique - Configuration
🛡️ Préservation des mécanismes de sécurité
"""

import json
import logging
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional, Union


@dataclass
class CoreConfig:
    """Configuration de base du Core"""

    debug_mode: bool = False
    log_level: str = "INFO"
    max_retries: int = 3
    timeout: float = 30.0
    enable_watchdogs: bool = True
    enable_metrics: bool = True
    enable_alerts: bool = True


class ConfigManager:
    """
    🎯 Gestionnaire de configuration centralisé
    🛡️ Préservation des mécanismes de sécurité
    """

    def __init__(self, config_path: str | None = None):
        self.logger = logging.getLogger("arkalia.core.config")
        self.config_path = config_path or self._get_default_config_path()
        self._config: dict[str, Any] = {}
        self._core_config = CoreConfig()
        self._initialized = False

        # Initialisation automatique
        self.initialize()

    def _get_default_config_path(self) -> str:
        """Chemin par défaut de la configuration"""
        return str(Path(__file__).parent.parent.parent.parent / "config" / "core_config.json")

    def initialize(self) -> bool:
        """
        🚀 Initialisation de la configuration
        ✅ Chargement intelligent avec fallbacks
        """
        try:
            self.logger.info("🔧 Initialisation ConfigManager...")

            # Chargement de la configuration
            self._load_config()

            # Validation de la configuration
            self._validate_config()

            # Application des paramètres
            self._apply_config()

            self._initialized = True
            self.logger.info("✅ ConfigManager initialisé avec succès")
            return True

        except Exception as e:
            self.logger.error(f"❌ Erreur initialisation ConfigManager : {e}")
            # Fallback vers configuration par défaut
            self._load_default_config()
            return False

    def _load_config(self) -> None:
        """Chargement de la configuration depuis le fichier"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, encoding="utf-8") as f:
                    self._config = json.load(f)
                self.logger.info(f"📄 Configuration chargée depuis {self.config_path}")
            else:
                self.logger.warning(f"⚠️ Fichier de config non trouvé : {self.config_path}")
                self._load_default_config()
        except Exception as e:
            self.logger.error(f"❌ Erreur chargement config : {e}")
            self._load_default_config()

    def _load_default_config(self) -> None:
        """Chargement de la configuration par défaut"""
        self._config = {
            "core": asdict(self._core_config),
            "modules": {
                "zeroia": {"enabled": True, "max_decisions": 1000},
                "sandozia": {"enabled": True, "analysis_depth": "medium"},
                "reflexia": {"enabled": True, "panic_threshold": 0.8},
                "assistantia": {"enabled": True, "max_conversations": 100},
                "helloria": {"enabled": True, "port": 8000},
                "monitoring": {"enabled": True, "metrics_interval": 30},
                "security": {"enabled": True, "encryption_level": "high"},
            },
            "watchdogs": {
                "reflexia_panic": {"enabled": True, "threshold": 0.9},
                "zeroia_circuit": {"enabled": True, "failure_threshold": 5},
                "sandozia_anomaly": {"enabled": True, "sensitivity": 0.7},
            },
        }
        self.logger.info("📄 Configuration par défaut chargée")

    def _validate_config(self) -> None:
        """Validation de la configuration"""
        required_sections = ["core", "modules", "watchdogs"]
        for section in required_sections:
            if section not in self._config:
                self.logger.warning(f"⚠️ Section manquante : {section}")
                self._config[section] = {}

    def _apply_config(self) -> None:
        """Application de la configuration"""
        # Configuration du logging
        if "core" in self._config:
            core_config = self._config["core"]
            if "log_level" in core_config:
                logging.getLogger().setLevel(getattr(logging, core_config["log_level"]))

    def get_config(self, section: str | None = None) -> dict[str, Any]:
        """
        📄 Récupération de la configuration
        :param section: Section spécifique (None = tout)
        :return: Configuration
        """
        if not self._initialized:
            self.initialize()

        if section is None:
            return self._config.copy()

        return self._config.get(section, {}).copy()

    def get_module_config(self, module_name: str) -> dict[str, Any]:
        """
        📄 Configuration d'un module spécifique
        :param module_name: Nom du module
        :return: Configuration du module
        """
        modules_config = self.get_config("modules")
        return modules_config.get(module_name, {})

    def get_watchdog_config(self, watchdog_name: str) -> dict[str, Any]:
        """
        🛡️ Configuration d'un watchdog spécifique
        :param watchdog_name: Nom du watchdog
        :return: Configuration du watchdog
        """
        watchdogs_config = self.get_config("watchdogs")
        return watchdogs_config.get(watchdog_name, {})

    def set_config(self, section: str, key: str, value: Any) -> bool:
        """
        ✏️ Modification de la configuration
        :param section: Section de configuration
        :param key: Clé à modifier
        :param value: Nouvelle valeur
        :return: True si modification réussie
        """
        try:
            if section not in self._config:
                self._config[section] = {}

            self._config[section][key] = value
            self.logger.info(f"✏️ Configuration mise à jour : {section}.{key} = {value}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Erreur modification config : {e}")
            return False

    def save_config(self) -> bool:
        """
        💾 Sauvegarde de la configuration
        :return: True si sauvegarde réussie
        """
        try:
            # Création du répertoire si nécessaire
            config_dir = Path(self.config_path).parent
            config_dir.mkdir(parents=True, exist_ok=True)

            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)

            self.logger.info(f"💾 Configuration sauvegardée : {self.config_path}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde config : {e}")
            return False

    def reload_config(self) -> bool:
        """
        🔄 Rechargement de la configuration
        :return: True si rechargement réussi
        """
        self.logger.info("🔄 Rechargement de la configuration...")
        return self.initialize()

    def health_check(self) -> dict[str, Any]:
        """
        🏥 Vérification de santé du ConfigManager
        :return: Statut de santé
        """
        return {
            "module": "config_manager",
            "status": "healthy" if self._initialized else "uninitialized",
            "config_path": self.config_path,
            "sections": list(self._config.keys()),
            "modules_configured": len(self.get_config("modules")),
            "watchdogs_configured": len(self.get_config("watchdogs")),
        }

    def get_environment_config(self) -> dict[str, str]:
        """
        🌍 Configuration depuis les variables d'environnement
        :return: Configuration environnement
        """
        env_config = {}
        env_mappings = {
            "ARKALIA_DEBUG": "core.debug_mode",
            "ARKALIA_LOG_LEVEL": "core.log_level",
            "ARKALIA_MAX_RETRIES": "core.max_retries",
            "ARKALIA_TIMEOUT": "core.timeout",
        }

        for env_var, config_path in env_mappings.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                # Conversion des types
                if config_path.endswith("debug_mode"):
                    value = value.lower() in ("true", "1", "yes")
                elif config_path.endswith(("max_retries", "timeout")):
                    value = float(value) if "." in value else int(value)

                env_config[config_path] = value

        return env_config


# Instance par défaut
default_config_manager = ConfigManager()
