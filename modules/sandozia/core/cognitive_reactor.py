#!/usr/bin/env python3
# 🔥 modules/sandozia/core/cognitive_reactor.py
# Réacteur Cognitif - Actions automatiques basées sur patterns

"""
Cognitive Reactor pour Arkalia-LUNA Enhanced v3.0-phase1+

Fonctionnalités automatiques :
- Réaction aux patterns répétitifs (7+ décisions identiques → pause cognitive)
- Mode quarantine pour modules instables (confiance < 0.5)
- Mode berserk/panic pour effondrements brutaux (score global < 0.1)
- Intégration parfaite avec BehaviorAnalyzer existant
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from modules.sandozia.analyzer.behavior import BehaviorAnalyzer
from modules.zeroia.event_store import EventStore, EventType

logger = logging.getLogger(__name__)


class ReactionSeverity(Enum):
    """Niveaux de sévérité des réactions"""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    BERSERK = "berserk"


class QuarantineReason(Enum):
    """Raisons de mise en quarantine"""

    LOW_CONFIDENCE = "low_confidence"
    EXCESSIVE_PATTERNS = "excessive_patterns"
    CONTRADICTIONS = "contradictions"
    INSTABILITY = "instability"
    MANUAL = "manual"


@dataclass
class CognitiveReaction:
    """Représente une réaction cognitive automatique"""

    reaction_id: str
    trigger_pattern: str
    action: str
    severity: ReactionSeverity
    module_target: Optional[str] = None
    parameters: Dict = field(default_factory=dict)
    executed_at: Optional[datetime] = None
    success: bool = False
    error_message: Optional[str] = None


@dataclass
class ModuleQuarantine:
    """État de quarantine d'un module"""

    module_name: str
    reason: QuarantineReason
    quarantined_at: datetime
    until: Optional[datetime] = None
    attempts_count: int = 0
    max_attempts: int = 3
    metadata: Dict = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        if self.until is None:
            return False
        return datetime.now() > self.until

    @property
    def can_retry(self) -> bool:
        return self.attempts_count < self.max_attempts


class CognitiveReactor:
    """
    🔥 Réacteur Cognitif - Actions automatiques intelligentes

    Intégration avec ton architecture existante :
    - BehaviorAnalyzer (détection patterns)
    - EventStore (persistance événements)
    - ZeroIA Circuit Breaker (protection)
    """

    def __init__(self, behavior_analyzer: Optional[BehaviorAnalyzer] = None):
        self.behavior_analyzer = behavior_analyzer or BehaviorAnalyzer()
        self.event_store = EventStore()

        # État des quarantines actives
        self.quarantined_modules: Dict[str, ModuleQuarantine] = {}

        # Historique des réactions
        self.reaction_history: List[CognitiveReaction] = []

        # Configuration seuils
        self.config = {
            "repetition_threshold": 7,  # 7 décisions identiques → réaction
            "confidence_threshold": 0.5,  # < 0.5 → quarantine
            "pattern_frequency_limit": 10,  # patterns/minute max
            "berserk_threshold": 0.1,  # Score global < 0.1 → panic
            "quarantine_duration_minutes": 30,
            "berserk_cooldown_minutes": 60,
        }

        # État berserk
        self.berserk_mode_active = False
        self.last_berserk_trigger: Optional[datetime] = None

        logger.info("🔥 CognitiveReactor initialized - Réactions automatiques activées")

    async def check_and_react(
        self, context: Dict, decision_pattern_count: int = 0
    ) -> List[CognitiveReaction]:
        """
        🎯 FONCTION PRINCIPALE - Vérifie et déclenche des réactions automatiques

        Args:
            context: Contexte système actuel
            decision_pattern_count: Nombre de répétitions détectées

        Returns:
            Liste des réactions déclenchées
        """
        reactions = []

        try:
            # 1. Nettoyer les quarantines expirées
            self._cleanup_expired_quarantines()

            # 2. Vérifier le mode berserk en premier
            berserk_reaction = await self._check_berserk_mode(context)
            if berserk_reaction:
                reactions.append(berserk_reaction)
                return reactions  # Mode berserk override tout

            # 3. Réaction aux patterns répétitifs
            if decision_pattern_count >= self.config["repetition_threshold"]:
                reaction = await self._trigger_cognitive_pause(decision_pattern_count)
                if reaction:
                    reactions.append(reaction)

            # 4. Vérifier la santé des modules
            health_reactions = await self._check_module_health(context)
            reactions.extend(health_reactions)

            # 5. Enregistrer dans l'Event Store
            for reaction in reactions:
                await self._log_reaction(reaction)

            return reactions

        except Exception as e:
            logger.error(f"❌ Erreur CognitiveReactor: {e}")
            return []

    async def _trigger_cognitive_pause(
        self, repetition_count: int
    ) -> Optional[CognitiveReaction]:
        """🔥 IMPLÉMENTATION - Pause cognitive automatique"""

        reaction = CognitiveReaction(
            reaction_id=f"cognitive_pause_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            trigger_pattern="repetitive_decisions",
            action="cognitive_pause",
            severity=ReactionSeverity.WARNING,
            parameters={
                "pause_duration_seconds": 60,
                "repetition_count": repetition_count,
                "trigger_threshold": self.config["repetition_threshold"],
            },
        )

        # Exécuter la pause cognitive
        try:
            # Créer un marker pour ZeroIA
            pause_file = Path("state/cognitive_pause_active.marker")
            pause_file.write_text(f"cognitive_pause:{datetime.now().isoformat()}")

            reaction.executed_at = datetime.now()
            reaction.success = True

            logger.warning(
                f"⏸️ PAUSE COGNITIVE ACTIVÉE - {repetition_count} répétitions détectées"
            )

            # Auto-cleanup après 60 secondes
            asyncio.create_task(self._cleanup_pause_marker(pause_file, 60))

            return reaction

        except Exception as e:
            reaction.success = False
            logger.error(f"❌ Échec pause cognitive: {e}")
            return reaction

    async def _check_berserk_mode(self, context: Dict) -> Optional[CognitiveReaction]:
        """🚨 MODE BERSERK - Fail-safe autonome pour effondrements brutaux"""

        # Cooldown berserk mode
        if self.last_berserk_trigger:
            cooldown_delta = datetime.now() - self.last_berserk_trigger
            if cooldown_delta < timedelta(
                minutes=self.config["berserk_cooldown_minutes"]
            ):
                return None

        # Calcul score global système
        global_score = self._calculate_global_health_score(context)

        if global_score < self.config["berserk_threshold"]:
            self.berserk_mode_active = True
            self.last_berserk_trigger = datetime.now()

            reaction = CognitiveReaction(
                reaction_id=f"berserk_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                trigger_pattern="global_health_collapse",
                action="berserk_mode_activation",
                severity=ReactionSeverity.BERSERK,
                parameters={
                    "global_score": global_score,
                    "threshold": self.config["berserk_threshold"],
                },
            )

            # Exécuter le mode berserk
            try:
                # Actions d'urgence
                emergency_file = Path("state/berserk_mode_active.emergency")
                emergency_file.write_text(
                    f"berserk_mode:{datetime.now().isoformat()}:score_{global_score}"
                )

                # Quarantine automatique tous modules instables
                for module in ["reflexia", "sandozia", "assistantia"]:
                    await self.quarantine_module(
                        module, QuarantineReason.INSTABILITY, 10
                    )

                reaction.executed_at = datetime.now()
                reaction.success = True

                logger.critical(
                    f"🚨 MODE BERSERK ACTIVÉ - Score global: {global_score}"
                )

            except Exception as e:
                reaction.success = False
                logger.error(f"❌ Échec mode berserk: {e}")

            return reaction

        return None

    async def quarantine_module(
        self,
        module_name: str,
        reason: QuarantineReason,
        duration_minutes: Optional[int] = None,
        metadata: Optional[Dict] = None,
    ):
        """🔒 Met un module en quarantine"""

        duration = duration_minutes or self.config["quarantine_duration_minutes"]
        until = datetime.now() + timedelta(minutes=duration)

        quarantine = ModuleQuarantine(
            module_name=module_name,
            reason=reason,
            quarantined_at=datetime.now(),
            until=until,
            metadata=metadata or {},
        )

        self.quarantined_modules[module_name] = quarantine

        # Enregistrer dans Event Store
        self.event_store.add_event(
            EventType.STATE_CHANGE,
            {
                "action": "module_quarantined",
                "module": module_name,
                "reason": reason.value,
                "duration_minutes": duration,
                "until": until.isoformat(),
            },
            module="cognitive_reactor",
        )

        # Créer fichier de quarantine pour les autres modules
        quarantine_file = Path(f"state/{module_name}_quarantined.marker")
        quarantine_file.write_text(f"quarantine:{reason.value}:{until.isoformat()}")

        logger.warning(
            f"🔒 MODULE EN QUARANTINE: {module_name} - Raison: {reason.value} - {duration}min"
        )

    def is_module_quarantined(self, module_name: str) -> bool:
        """Vérifie si un module est en quarantine"""
        if module_name not in self.quarantined_modules:
            return False

        quarantine = self.quarantined_modules[module_name]
        if quarantine.is_expired:
            self._release_quarantine(module_name)
            return False

        return True

    def get_quarantine_status(self) -> Dict[str, Dict]:
        """Retourne l'état de toutes les quarantines"""
        status = {}
        for module, quarantine in self.quarantined_modules.items():
            status[module] = {
                "reason": quarantine.reason.value,
                "since": quarantine.quarantined_at.isoformat(),
                "until": quarantine.until.isoformat() if quarantine.until else None,
                "expired": quarantine.is_expired,
                "attempts": quarantine.attempts_count,
                "can_retry": quarantine.can_retry,
            }
        return status

    def _calculate_global_health_score(self, context: Dict) -> float:
        """Calcule un score de santé global du système"""
        try:
            factors = []

            # CPU/RAM/Disk
            status = context.get("status", {})
            cpu = status.get("cpu", 50)
            ram = status.get("ram", 50)

            # Score système (inversé : plus bas = meilleur)
            system_score = max(0, 1.0 - (cpu + ram) / 200)
            factors.append(system_score)

            # Score confiance modules
            for module in ["zeroia", "reflexia", "sandozia"]:
                confidence = context.get(f"{module}_confidence", 0.5)
                factors.append(confidence)

            # Pénalité quarantines
            quarantine_penalty = len(self.quarantined_modules) * 0.1
            quarantine_score = max(0, 1.0 - quarantine_penalty)
            factors.append(quarantine_score)

            return sum(factors) / len(factors) if factors else 0.5

        except Exception as e:
            logger.error(f"❌ Erreur calcul score global: {e}")
            return 0.5

    def _cleanup_expired_quarantines(self):
        """Nettoie les quarantines expirées"""
        expired = [
            module
            for module, quarantine in self.quarantined_modules.items()
            if quarantine.is_expired
        ]

        for module in expired:
            self._release_quarantine(module)

    def _release_quarantine(self, module_name: str):
        """Libère un module de quarantine"""
        if module_name in self.quarantined_modules:
            quarantine = self.quarantined_modules.pop(module_name)

            self.event_store.add_event(
                EventType.STATE_CHANGE,
                {
                    "action": "module_released_from_quarantine",
                    "module": module_name,
                    "quarantine_duration_minutes": (
                        datetime.now() - quarantine.quarantined_at
                    ).total_seconds()
                    / 60,
                },
                module="cognitive_reactor",
            )

            # Supprimer le fichier de quarantine
            quarantine_file = Path(f"state/{module_name}_quarantined.marker")
            if quarantine_file.exists():
                quarantine_file.unlink()

            logger.info(f"🔓 MODULE LIBÉRÉ: {module_name} - Quarantine terminée")

    async def _log_reaction(self, reaction: CognitiveReaction):
        """Enregistre une réaction dans l'historique et Event Store"""
        self.reaction_history.append(reaction)

        # Limiter l'historique
        if len(self.reaction_history) > 1000:
            self.reaction_history = self.reaction_history[-500:]

        # Event Store
        self.event_store.add_event(
            EventType.DECISION_MADE,
            {
                "reaction_id": reaction.reaction_id,
                "trigger_pattern": reaction.trigger_pattern,
                "action": reaction.action,
                "severity": reaction.severity.value,
                "module_target": reaction.module_target,
                "success": reaction.success,
                "parameters": reaction.parameters,
            },
            module="cognitive_reactor",
        )

    async def _cleanup_pause_marker(self, pause_file: Path, delay_seconds: int):
        """Nettoie automatiquement le marker de pause après délai"""
        await asyncio.sleep(delay_seconds)
        if pause_file.exists():
            pause_file.unlink()
            logger.info("⏸️ Pause cognitive terminée automatiquement")

    async def _check_module_health(self, context: Dict) -> List[CognitiveReaction]:
        """Vérifie la santé des modules et déclenche des quarantines si nécessaire"""
        reactions = []

        for module in ["zeroia", "reflexia", "sandozia"]:
            confidence = context.get(f"{module}_confidence", 0.5)

            if confidence < self.config[
                "confidence_threshold"
            ] and not self.is_module_quarantined(module):
                await self.quarantine_module(
                    module,
                    QuarantineReason.LOW_CONFIDENCE,
                    metadata={"confidence": confidence},
                )

                reaction = CognitiveReaction(
                    reaction_id=f"quarantine_{module}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    trigger_pattern="low_confidence",
                    action="quarantine_module",
                    severity=ReactionSeverity.WARNING,
                    module_target=module,
                    parameters={"confidence": confidence},
                )
                reaction.executed_at = datetime.now()
                reaction.success = True
                reactions.append(reaction)

        return reactions


# 🚀 Factory function pour intégration facile
def create_cognitive_reactor(
    behavior_analyzer: Optional[BehaviorAnalyzer] = None,
) -> CognitiveReactor:
    """Crée une instance de CognitiveReactor"""
    return CognitiveReactor(behavior_analyzer)


# 🧪 Fonction d'intégration avec ton reason_loop existant
def trigger_cognitive_reaction(
    context: Dict, decision_pattern_count: int = 0
) -> List[str]:
    """
    🎯 INTÉGRATION SIMPLE - Appelle depuis ton reason_loop

    Usage dans reason_loop_enhanced.py :

    from modules.sandozia.core.cognitive_reactor import trigger_cognitive_reaction

    # Après détection pattern répétitif :
    if decision_pattern_count >= 7:
        reactions = trigger_cognitive_reaction(context, decision_pattern_count)
        for reaction in reactions:
            logger.info(f"🔥 Réaction automatique: {reaction}")
    """
    reactor = create_cognitive_reactor()

    try:
        # Appel synchrone simple pour intégration
        import asyncio

        reactions = asyncio.run(
            reactor.check_and_react(context, decision_pattern_count)
        )

        return [f"{r.action}:{r.severity.value}" for r in reactions]

    except Exception as e:
        logger.error(f"❌ Erreur trigger_cognitive_reaction: {e}")
        return []


# 🚀 Mode daemon pour conteneur Docker
async def run_daemon():
    """Lance le CognitiveReactor en mode daemon"""
    import argparse
    import signal
    import sys

    parser = argparse.ArgumentParser(description="CognitiveReactor Daemon")
    parser.add_argument("--daemon", action="store_true", help="Mode daemon")
    args = parser.parse_args()

    if not args.daemon:
        print("Usage: python -m modules.sandozia.core.cognitive_reactor --daemon")
        sys.exit(1)

    reactor = create_cognitive_reactor()
    logger.info("🔥 CognitiveReactor daemon démarré")

    # Gestion signal d'arrêt
    def signal_handler(signum, frame):
        logger.info("🛑 Arrêt du daemon CognitiveReactor")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        while True:
            # Cycle de monitoring toutes les 30 secondes
            context = {
                "timestamp": datetime.now().isoformat(),
                "system_cpu": 50,
                "system_ram": 60,
                "zeroia_confidence": 0.8,
                "reflexia_confidence": 0.7,
                "sandozia_confidence": 0.9,
            }

            reactions = await reactor.check_and_react(context, 0)
            if reactions:
                logger.info(f"🔥 {len(reactions)} réactions déclenchées")

            await asyncio.sleep(30)

    except KeyboardInterrupt:
        logger.info("🛑 Daemon arrêté par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur daemon: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_daemon())
