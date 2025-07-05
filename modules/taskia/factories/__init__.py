#!/usr/bin/env python3
"""
🌕 TaskIA Factories Package
📝 Factories pour l'injection de dépendances selon le principe DIP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

from .formatter_factory import FormatterFactory
from .service_factory import ServiceFactory

__all__ = ["FormatterFactory", "ServiceFactory"]

__version__ = "2.0.0"
__author__ = "Athalia"
