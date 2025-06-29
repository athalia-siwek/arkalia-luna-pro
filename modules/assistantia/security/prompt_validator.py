# 🛡️ Validateur de Prompts - Sécurité LLM Arkalia-LUNA
# Protection contre prompt injection, code injection, et attaques DOS

import hashlib
import re
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class SecurityLevel(Enum):
    """Niveaux de sécurité pour la validation"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    PARANOID = "paranoid"


@dataclass
class ValidationResult:
    """Résultat de validation d'un prompt"""

    is_valid: bool
    security_score: float  # 0.0 = dangereux, 1.0 = sûr
    issues: list[str]
    sanitized_prompt: str
    blocked_patterns: list[str]


class PromptValidator:
    """Validateur principal pour les prompts LLM"""

    def __init__(self, security_level: SecurityLevel = SecurityLevel.MEDIUM) -> None:
        self.security_level = security_level
        self._load_patterns()
        self._rate_limit_cache: dict[str, list[float]] = {}

    def _load_patterns(self):
        """Charge les patterns d'injection selon le niveau de sécurité"""

        # Patterns de base - toujours actifs
        self.injection_patterns = [
            # Prompt injection classiques
            r"ignore.*previous.*instructions",
            r"disregard.*the.*above",
            r"forget.*everything.*before",
            r"new\s+instructions?:",
            r"system\s*:\s*",
            r"assistant\s*:\s*",
            r"human\s*:\s*",
            r"user\s*:\s*",
            # Jailbreak patterns
            r"act\s+as\s+(?:a\s+)?(?:an\s+)?(?:evil|malicious|harmful)",
            r"pretend\s+(?:to\s+be|you\s+are)",
            r"roleplay\s+as",
            r"simulate\s+(?:a\s+)?(?:an\s+)?(?:evil|harmful|malicious)",
            r"bypass\s+(?:your\s+)?(?:safety|security|guidelines)",
            # Code injection basique
            r"<script\b[^>]*>",
            r"javascript\s*:",
            r"eval\s*\(",
            r"exec\s*\(",
            r"import\s+os",
            r"subprocess\.",
            r"__import__",
            # Command injection
            r";\s*(?:rm|del|format|shutdown)",
            r"\|\s*(?:rm|del|cat|ls)",
            r"&&\s*(?:rm|del|cat)",
            r"`[^`]*`",  # Backticks
            r"\$\([^)]+\)",  # Command substitution
        ]

        # Patterns avancés selon le niveau
        if self.security_level in [SecurityLevel.HIGH, SecurityLevel.PARANOID]:
            self.injection_patterns.extend(
                [
                    # Encoding bypass attempts
                    r"&#x[0-9a-f]+;",  # Hex encoding
                    r"&#[0-9]+;",  # Decimal encoding
                    r"%[0-9a-f]{2}",  # URL encoding
                    r"\\u[0-9a-f]{4}",  # Unicode escape
                    r"\\x[0-9a-f]{2}",  # Hex escape
                    # Advanced prompt manipulation
                    r"template\s*:\s*",
                    r"format\s*:\s*",
                    r"render\s*\(",
                    r"\.format\s*\(",
                    r"f['\"][^'\"]*\{",  # f-strings
                    # System access attempts
                    r"(?:/etc/|/proc/|/sys/|c:\\windows)",
                    r"(?:passwd|shadow|hosts|config)",
                    r"\.\.+/",  # Directory traversal
                    # Data extraction attempts
                    r"print\s*\(",
                    r"console\.log",
                    r"document\.",
                    r"window\.",
                    r"alert\s*\(",
                ]
            )

        if self.security_level == SecurityLevel.PARANOID:
            self.injection_patterns.extend(
                [
                    # Suspicious keywords
                    r"(?:hack|exploit|vulnerability|bypass|override)",
                    r"(?:admin|root|sudo|privilege)",
                    r"(?:password|token|key|secret|api_key)",
                    r"(?:database|sql|query|select|insert|update|delete)",
                    # Obfuscation attempts
                    r"[a-zA-Z0-9+/]{20,}={0,2}",  # Base64-like
                    r"(?:[0-9a-f]{2}\s*){10,}",  # Hex strings
                    r"(?:\\[0-7]{3}\s*){5,}",  # Octal sequences
                ]
            )

    def validate_input(self, prompt: str) -> ValidationResult:
        """
        Valide un prompt en entrée

        Args:
            prompt: Le prompt à valider

        Returns:
            ValidationResult: Résultat de la validation
        """
        if not prompt or not prompt.strip():
            return ValidationResult(
                is_valid=False,
                security_score=0.0,
                issues=["Prompt vide"],
                sanitized_prompt="",
                blocked_patterns=[],
            )

        # Vérifications de base
        issues: list[Any] = []
        blocked_patterns: list[Any] = []
        security_score = 1.0

        # 1. Vérification de longueur
        if len(prompt) > 10000:  # 10KB max
            issues.append("Prompt trop long (> 10KB)")
            security_score -= 0.3

        # 2. Vérification des patterns d'injection
        prompt_lower = prompt.lower()
        for pattern in self.injection_patterns:
            if re.search(pattern, prompt_lower, re.IGNORECASE | re.MULTILINE):
                issues.append(f"Pattern suspect détecté: {pattern}")
                blocked_patterns.append(pattern)
                security_score -= 0.2

        # 3. Vérification du rate limiting
        if not self._check_rate_limit(prompt):
            issues.append("Rate limit dépassé")
            security_score -= 0.5

        # 4. Entropie suspecte (obfuscation)
        entropy = self._calculate_entropy(prompt)
        if entropy > 4.5:  # Seuil d'entropie élevée
            issues.append("Entropie élevée - possible obfuscation")
            security_score -= 0.2

        # 5. Caractères suspects
        suspicious_chars = len(re.findall(r"[<>{}()\[\]`$|&;]", prompt))
        if suspicious_chars > len(prompt) * 0.1:  # Plus de 10% de caractères suspects
            issues.append("Trop de caractères suspects")
            security_score -= 0.1

        # Sanitization
        sanitized_prompt = self.sanitize_prompt(prompt)

        # Détermination finale
        is_valid = security_score >= 0.5 and len(blocked_patterns) == 0

        return ValidationResult(
            is_valid=is_valid,
            security_score=max(0.0, security_score),
            issues=issues,
            sanitized_prompt=sanitized_prompt,
            blocked_patterns=blocked_patterns,
        )

    def sanitize_prompt(self, prompt: str) -> str:
        """
        Nettoie et sanitise un prompt

        Args:
            prompt: Le prompt à nettoyer

        Returns:
            str: Prompt nettoyé
        """
        if not prompt:
            return ""

        # 1. Normalisation des espaces
        sanitized = re.sub(r"\s+", " ", prompt.strip())

        # 2. Suppression des caractères de contrôle
        sanitized = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", sanitized)

        # 3. Échappement des caractères dangereux (ordre important : & en premier)
        sanitized = sanitized.replace("&", "&amp;")
        sanitized = sanitized.replace("<", "&lt;")
        sanitized = sanitized.replace(">", "&gt;")
        sanitized = sanitized.replace('"', "&quot;")
        sanitized = sanitized.replace("'", "&#x27;")
        sanitized = sanitized.replace("`", "&#x60;")

        # 4. Limitation de longueur
        if len(sanitized) > 5000:
            sanitized = sanitized[:5000] + " [TRONQUÉ]"

        return sanitized

    def detect_injection_patterns(self, text: str) -> list[str]:
        """
        Détecte les patterns d'injection dans un texte

        Args:
            text: Texte à analyser

        Returns:
            list[str]: Liste des patterns détectés
        """
        detected: list[Any] = []
        text_lower = text.lower()

        for pattern in self.injection_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE | re.MULTILINE):
                detected.append(pattern)

        return detected

    def _check_rate_limit(
        self, prompt: str, max_requests: int = 10, window_seconds: int = 60
    ) -> bool:
        """Vérifie le rate limiting basé sur le hash du prompt"""
        prompt_hash = hashlib.md5(prompt.encode(), usedforsecurity=False).hexdigest()  # nosec B324
        current_time = time.time()

        if prompt_hash not in self._rate_limit_cache:
            self._rate_limit_cache[prompt_hash] = []

        # Nettoie les anciens timestamps
        self._rate_limit_cache[prompt_hash] = [
            ts for ts in self._rate_limit_cache[prompt_hash] if current_time - ts < window_seconds
        ]

        # Vérifie la limite
        if len(self._rate_limit_cache[prompt_hash]) >= max_requests:
            return False

        # Ajoute le timestamp actuel
        self._rate_limit_cache[prompt_hash].append(current_time)
        return True

    def _calculate_entropy(self, text: str) -> float:
        """Calcule l'entropie d'un texte (détection d'obfuscation)"""
        if not text:
            return 0.0

        import math

        # Compte la fréquence des caractères
        char_counts: dict[str, Any] = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1

        # Calcule l'entropie de Shannon
        length = len(text)
        entropy = 0.0

        for count in char_counts.values():
            probability = count / length
            if probability > 0:
                entropy -= probability * math.log2(probability)

        return entropy


# Instance globale par défaut
default_validator = PromptValidator(SecurityLevel.MEDIUM)


def validate_input(prompt: str) -> bool:
    """
    Fonction simple de validation (interface de compatibilité)

    Args:
        prompt: Prompt à valider

    Returns:
        bool: True si valide, False sinon
    """
    result = default_validator.validate_input(prompt)
    return result.is_valid


def sanitize_prompt(prompt: str) -> str:
    """
    Fonction simple de sanitisation (interface de compatibilité)

    Args:
        prompt: Prompt à nettoyer

    Returns:
        str: Prompt nettoyé
    """
    return default_validator.sanitize_prompt(prompt)


def detect_injection_patterns(text: str) -> list[str]:
    """
    Fonction simple de détection (interface de compatibilité)

    Args:
        text: Texte à analyser

    Returns:
        list[str]: Patterns détectés
    """
    return default_validator.detect_injection_patterns(text)
