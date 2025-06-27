# 🛡️ modules/security/__init__.py


# Module de sécurité avancée Arkalia-LUNA Phase 4

"""
Module de sécurité paranoïaque Arkalia-LUNA

Composants:
- crypto/: Chiffrement, checksums, merkle chains
- sandbox/: Isolation IA et prompt quarantine
- watchdog/: Surveillance cognitive et auto-healing
"""

__version__ = "4.0.0-security"
__author__ = "Arkalia Security Team"

# Classes principales
from .crypto.checksum_validator import BuildIntegrityValidator, SecurityError

# from .crypto.merkle_chains import SnapshotMerkleChain
# from .sandbox.llm_sandbox import LLMSandbox
# from .watchdog.reflexia_watchdog import ReflexIAWatchdog

# Configuration sécurité
SECURITY_LEVEL = "PARANOID"
COMPLIANCE_STANDARDS = ["ISO_27001", "SOC2_TYPE_II", "AI_GOVERNANCE"]

__all__ = [
    "BuildIntegrityValidator",
    "SecurityError",
    # "SnapshotMerkleChain",
    # "LLMSandbox",
    # "ReflexIAWatchdog",
    "SECURITY_LEVEL",
    "COMPLIANCE_STANDARDS",
]
