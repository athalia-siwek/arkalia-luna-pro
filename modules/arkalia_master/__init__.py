#!/usr/bin/env python3
"""
🌕 ARKALIA MASTER ORCHESTRATOR v4.0.0
Orchestrateur Maître de l'écosystème Arkalia-LUNA

Coordonne intelligemment les 10 modules IA :
- ZeroIA, ReflexIA, AssistantIA, SandozIA, TaskIA
- HellorIA, NyxalIA, Security, Monitoring, Utils

Architecture :
- Cycles adaptatifs (5s urgent, 30s normal, 300s deep)
- Circuit breaker global
- Communication inter-modules optimisée
- Global State Master unifié
"""

from .orchestrator_ultimate import (
    ArkaliaOrchestrator,
    OrchestratorConfig,
    ModuleStatus,
    CycleMode,
    orchestrate_full_ecosystem,
)

__version__ = "4.0.0"
__author__ = "Athalia - Arkalia-LUNA"

__all__ = [
    "ArkaliaOrchestrator",
    "OrchestratorConfig", 
    "ModuleStatus",
    "CycleMode",
    "orchestrate_full_ecosystem",
] 