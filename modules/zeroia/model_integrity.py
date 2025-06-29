#!/usr/bin/env python3

"""
🛡️ modules/zeroia/model_integrity.py
Model Integrity Monitor for ZeroIA - Roadmap S2 Integration

Module d'intégrité intégré à ZeroIA pour détection temps réel
des tentatives d'empoisonnement de modèle.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Configuration
INTEGRITY_LOG = Path("modules/zeroia/logs/model_integrity.log")
INTEGRITY_STATE = Path("modules/zeroia/state/integrity_state.toml")


class ModelIntegrityMonitor:
    """Monitor d'intégrité temps réel pour ZeroIA"""

    def __init__(self, history_limit: int = 50):
        self.history_limit = history_limit
        self.decision_history: list[dict] = []
        self.anomaly_threshold = 0.6
        self.confidence_baseline = 0.6
        self.logger = self._setup_logger()
        self.suspicious_context_hashes = set()
        self.stealth_attack_counter = 0

    def _setup_logger(self) -> logging.Logger:
        """Configure le logger spécifique à l'intégrité"""
        logger = logging.getLogger("zeroia_integrity")
        logger.setLevel(logging.INFO)

        # Éviter duplication des handlers
        if not logger.handlers:
            INTEGRITY_LOG.parent.mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(INTEGRITY_LOG)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def validate_context_integrity(self, context: dict) -> tuple[bool, str, float]:
        """
        Valide l'intégrité du contexte d'entrée en temps réel

        Returns:
            (is_valid, reason, confidence)
        """
        try:
            # Validation structure basique
            if not self._validate_structure(context):
                return False, "Invalid context structure", 1.0

            # Validation valeurs
            if not self._validate_values(context):
                return False, "Invalid or malicious values detected", 0.9

            # Validation cohérence
            coherence_score = self._check_coherence(context)
            if coherence_score < 0.3:
                return (
                    False,
                    f"Low coherence score: {coherence_score:.2f}",
                    coherence_score,
                )

            return True, "Context integrity validated", coherence_score

        except Exception as e:
            self.logger.error(f"Integrity validation error: {e}")
            return False, f"Validation error: {e}", 0.0

    def _validate_structure(self, context: dict) -> bool:
        """Valide la structure du contexte - Compatible tests existants"""
        if not isinstance(context, dict):
            return False

        status = context.get("status", {})
        if not isinstance(status, dict):
            return False

        # Validation flexible: CPU requis + (severity OU ram) pour compatibilité
        required_cpu = "cpu" in status
        has_severity_or_ram = "severity" in status or "ram" in status

        return required_cpu and has_severity_or_ram

    def _validate_values(self, context: dict) -> bool:
        """Valide les valeurs pour détecter injections"""
        status = context.get("status", {})

        # Validation CPU
        cpu = status.get("cpu")
        if not isinstance(cpu, int | float) or cpu < 0 or cpu > 100:
            self.logger.warning(f"Suspicious CPU value: {cpu}")
            return False

        # Validation severity (optionnelle pour compatibilité)
        severity = status.get("severity")
        if severity is not None:
            valid_severities = ["none", "low", "medium", "high", "critical"]
            if severity not in valid_severities:
                self.logger.warning(f"Invalid severity: {severity}")
                return False

        # Détection patterns d'injection communs
        str_values = [str(v) for v in context.values() if isinstance(v, str)]
        injection_patterns = [
            "{{",
            "}}",
            "'; DROP",
            "--",
            "<script>",
            "echo ",
            "rm -rf",
            "DELETE FROM",
            "INSERT INTO",
            "UPDATE SET",
        ]

        for value in str_values:
            if any(pattern in value for pattern in injection_patterns):
                self.logger.error(f"Injection pattern detected: {value}")
                return False

        return True

    def _check_coherence(self, context: dict) -> float:
        """Vérifie la cohérence du contexte avec l'historique"""
        status = context.get("status", {})
        cpu = status.get("cpu", 0)
        severity = status.get("severity", "none")

        # Scores de cohérence basés sur logique métier
        coherence_score = 1.0

        # CPU vs Severity coherence (plus précis)
        if cpu > 90 and severity == "none":
            coherence_score -= 0.4  # Très suspect
        elif cpu > 80 and severity == "none":
            coherence_score -= 0.2  # Modérément suspect
        elif cpu < 20 and severity == "critical":
            coherence_score -= 0.5  # Très incohérent

        # Cohérence avec ReflexIA si présent
        reflexia = context.get("reflexia", {})
        if reflexia:
            reflexia_decision = reflexia.get("last_decision", "")
            reflexia_confidence = reflexia.get("confidence", 0.5)

            # Détection injection sophistiquée
            if cpu > 90 and reflexia_decision == "normal" and reflexia_confidence > 0.8:
                coherence_score -= 0.3  # Très suspect
            elif cpu < 40 and reflexia_decision == "emergency_shutdown":
                coherence_score -= 0.4  # Incohérent

        return max(0.0, coherence_score)

    def record_decision(self, context: dict, decision: str, confidence: float) -> None:
        """Enregistre une décision pour analyse de pattern"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "confidence": confidence,
            "context_hash": self._hash_context(context),
            "cpu": context.get("status", {}).get("cpu", 0),
            "severity": context.get("status", {}).get("severity", "unknown"),
        }

        self.decision_history.append(record)

        # Limiter l'historique
        if len(self.decision_history) > self.history_limit:
            self.decision_history = self.decision_history[-self.history_limit :]

        # Analyse pattern en temps réel
        self._analyze_pattern()

    def _hash_context(self, context: dict) -> str:
        """Génère un hash simple du contexte pour détection répétition"""
        status = context.get("status", {})
        key_data = f"{status.get('cpu', 0)}_{status.get('severity', 'none')}"
        return str(hash(key_data))

    def _analyze_pattern(self) -> None:
        """Analyse les patterns de décision pour détecter anomalies"""
        if len(self.decision_history) < 3:  # Plus sensible (était 5)
            return

        recent_decisions = [r["decision"] for r in self.decision_history[-10:]]
        recent_contexts = [r["context_hash"] for r in self.decision_history[-10:]]
        recent_cpus = [r["cpu"] for r in self.decision_history[-10:]]

        # Détection répétition excessive même contexte (équilibré)
        if len(recent_contexts) >= 4 and len(set(recent_contexts[-4:])) == 1:
            context_hash = recent_contexts[-1]
            self.suspicious_context_hashes.add(context_hash)
            self.stealth_attack_counter += 1
            msg = (
                f"Identical context repeated 4+ times - "
                f"possible stealth attack (count: {self.stealth_attack_counter})"
            )
            self.logger.warning(msg)

        # Détection oscillation rapide (plus sensible)
        if len(recent_decisions) >= 5:
            decision_changes = sum(
                1
                for i in range(1, len(recent_decisions))
                if recent_decisions[i] != recent_decisions[i - 1]
            )
            if decision_changes > len(recent_decisions) * 0.6:
                msg = (
                    f"Rapid decision oscillation detected: "
                    f"{decision_changes} changes in {len(recent_decisions)} decisions"
                )
                self.logger.warning(msg)

        # Détection emergency_shutdown fréquent (plus strict)
        emergency_count = recent_decisions.count("emergency_shutdown")
        if emergency_count > 2:  # Plus strict (était 3)
            msg = f"Excessive emergency shutdowns: " f"{emergency_count}/{len(recent_decisions)}"
            self.logger.error(msg)

        # Nouvelle détection: CPU élevé mais décision normale
        for _i, (decision, cpu) in enumerate(
            zip(recent_decisions[-5:], recent_cpus[-5:], strict=False)
        ):
            if cpu > 85 and decision == "normal":
                msg = f"Suspicious: High CPU ({cpu}%) but normal decision " f"- possible injection"
                self.logger.warning(msg)

        # Nouvelle détection: Répétition même décision avec CPU variable
        if len(recent_decisions) >= 4:
            same_decision_count = sum(1 for d in recent_decisions[-4:] if d == recent_decisions[-1])
            if same_decision_count >= 3:
                cpu_variance = max(recent_cpus[-4:]) - min(recent_cpus[-4:])
                if cpu_variance > 20:  # CPU très variable
                    msg = (
                        f"Same decision despite CPU variance: "
                        f"{cpu_variance}% - possible poisoning"
                    )
                    self.logger.warning(msg)

    def get_integrity_status(self) -> dict:
        """Retourne le statut d'intégrité actuel"""
        if len(self.decision_history) < 3:
            return {
                "status": "INITIALIZING",
                "confidence": 0.5,
                "decisions_analyzed": len(self.decision_history),
                "anomalies_detected": 0,
            }

        recent_decisions = [r["decision"] for r in self.decision_history[-10:]]
        recent_confidences = [r["confidence"] for r in self.decision_history[-10:]]

        # Calcul métriques
        avg_confidence = sum(recent_confidences) / len(recent_confidences)
        decision_diversity = len(set(recent_decisions)) / len(recent_decisions)

        # Détection anomalies (équilibré)
        anomalies = 0
        if avg_confidence < 0.4:  # Revenu à l'original
            anomalies += 1
        if decision_diversity > 0.8:  # Revenu à l'original
            anomalies += 1
        if decision_diversity < 0.2:  # Revenu à l'original pour éviter faux positifs
            anomalies += 1

        # Métrique stealth attack plus précise
        if self.stealth_attack_counter >= 2:  # Seulement si attaques répétées
            anomalies += 1

        status = "HEALTHY"
        if anomalies >= 2:
            status = "COMPROMISED"
        elif anomalies == 1:
            status = "SUSPICIOUS"

        return {
            "status": status,
            "confidence": avg_confidence,
            "decisions_analyzed": len(self.decision_history),
            "anomalies_detected": anomalies,
            "decision_diversity": decision_diversity,
            "last_updated": datetime.now().isoformat(),
        }

    def create_integrity_report(self) -> dict:
        """Génère un rapport d'intégrité complet"""
        status = self.get_integrity_status()

        if len(self.decision_history) >= 5:
            recent_decisions = [r["decision"] for r in self.decision_history[-20:]]
            decision_counts = {}
            for decision in recent_decisions:
                decision_counts[decision] = decision_counts.get(decision, 0) + 1

            status["decision_distribution"] = decision_counts
            status["most_frequent_decision"] = max(decision_counts.items(), key=lambda x: x[1])

        return status


# Instance globale pour intégration avec reason_loop
_integrity_monitor = None


def get_integrity_monitor() -> ModelIntegrityMonitor:
    """Retourne l'instance singleton du monitor d'intégrité"""
    global _integrity_monitor
    if _integrity_monitor is None:
        _integrity_monitor = ModelIntegrityMonitor()
    return _integrity_monitor


def validate_decision_integrity(
    context: dict, decision: str, confidence: float
) -> tuple[bool, str]:
    """
    Point d'entrée principal pour validation d'intégrité
    À appeler depuis reason_loop avant chaque décision
    """
    monitor = get_integrity_monitor()

    # Validation contexte
    is_valid, reason, integrity_confidence = monitor.validate_context_integrity(context)
    if not is_valid:
        monitor.logger.error(f"Context integrity violation: {reason}")
        return False, reason

    # Enregistrement décision
    monitor.record_decision(context, decision, confidence)

    # Vérification status général
    status = monitor.get_integrity_status()
    if status["status"] == "COMPROMISED":
        monitor.logger.critical("Model integrity compromised - potential poisoning detected")
        return False, "Model integrity compromised"

    return True, "Integrity validated"


# Export pour utilisation externe
__all__ = [
    "ModelIntegrityMonitor",
    "get_integrity_monitor",
    "validate_decision_integrity",
]
