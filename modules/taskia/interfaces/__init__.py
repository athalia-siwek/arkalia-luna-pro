#!/usr/bin/env python3
"""
🌕 TaskIA Interfaces Package
📝 Définit les contrats SOLID pour le module TaskIA
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

from .formatter_interface import IFormatter
from .task_processor_interface import ITaskProcessor
from .health_check_interface import IHealthChecker

__all__ = [
    "IFormatter",
    "ITaskProcessor", 
    "IHealthChecker"
]

__version__ = "2.0.0"
__author__ = "Athalia" 