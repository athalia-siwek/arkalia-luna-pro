#!/usr/bin/env python3
"""
🛠️ Helpers Module - Module d'utilitaires consolidé SOLID
Regroupe tous les utilitaires généraux du système Arkalia-LUNA

Principes SOLID appliqués :
- SRP : Chaque helper a une responsabilité unique
- OCP : Helpers extensibles via interfaces
- LSP : Interfaces polymorphiques pour les helpers
- ISP : Interfaces spécialisées par type d'utilitaire
- DIP : Injection de dépendances via factories
"""

from .io_safe import (
    AtomicWriteError,
    LockedReadError,
    atomic_write,
    locked_read,
    read_state_safe,
    save_json_safe,
    save_toml_safe,
)

__all__ = [
    "atomic_write",
    "locked_read",
    "save_toml_safe",
    "save_json_safe",
    "read_state_safe",
    "AtomicWriteError",
    "LockedReadError",
]
