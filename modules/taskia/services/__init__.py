#!/usr/bin/env python3
"""
🌕 TaskIA Services Package
📝 Services avec responsabilités uniques selon le principe SRP
🔧 Version: 2.0.0
👤 Author: Athalia
📅 Created: 2025-01-27
"""

from .health_checker import HealthChecker
from .logger_service import LoggerService
from .task_processor import TaskProcessor

__all__ = ["TaskProcessor", "HealthChecker", "LoggerService"]

__version__ = "2.0.0"
__author__ = "Athalia"
