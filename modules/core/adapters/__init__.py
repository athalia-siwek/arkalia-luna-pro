"""
🔗 Adapters - Adaptateurs SOLID pour modules existants
🎯 Interface entre modules existants et architecture SOLID
"""

from .reflexia_adapter import ReflexiaAdapter, create_reflexia_adapter
from .sandozia_adapter import SandoziaAdapter, create_sandozia_adapter
from .taskia_adapter import TaskIAAdapter, create_taskia_adapter
from .zeroia_adapter import ZeroIAAdapter, create_zeroia_adapter

__all__ = [
    "TaskIAAdapter",
    "create_taskia_adapter",
    "ZeroIAAdapter",
    "create_zeroia_adapter",
    "ReflexiaAdapter",
    "create_reflexia_adapter",
    "SandoziaAdapter",
    "create_sandozia_adapter",
]
