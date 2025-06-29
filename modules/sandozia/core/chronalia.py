#!/usr/bin/env python3
# 🕰️ modules/sandozia/core/chronalia.py
# Timeline Cognitive (Chronalia) - Mémoire continue pour apprentissage IA

"""
Chronalia - Timeline Cognitive pour Arkalia-LUNA Enhanced v3.0-phase1+

Implémente exactement tes recommandations :
- Timeline JSONL pour apprentissage machine
- Format cycle exact que tu as spécifié
- Export pour heatmap Grafana
- Détection patterns temporels
"""

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class CognitiveCycle:
    """
    🧠 Cycle cognitif - Format exact de tes recommandations

    [[cycle]]
    timestamp = "2025-06-29T23:37:14"
    reflexia_score = 1.0
    sandozia_health = 0.798
    contradiction = true
    decision_pattern = "identical"
    """

    timestamp: str
    reflexia_score: float
    sandozia_health: float
    contradiction: bool
    decision_pattern: str
    zeroia_decision: str
    confidence: float
    system_cpu: int
    system_ram: int
    modules_active: list[str]
    quarantined_modules: list[str]
    berserk_mode: bool
    cognitive_reactions: list[str]

    # Métadonnées pour analyse
    cycle_duration_ms: int | None = None
    pattern_repetition_count: int | None = None
    global_health_score: float | None = None


class Chronalia:
    """
    🕰️ Timeline Cognitive - Mémoire continue d'Arkalia

    Capture l'histoire cognitive complète selon tes spécifications :
    - Format JSONL pour apprentissage post-analyse
    - Cycles complets avec toutes métriques
    - Heatmap data pour Grafana
    - Patterns temporels automatiques
    """

    def __init__(self, timeline_dir: str = "state/chronalia"):
        self.timeline_dir = Path(timeline_dir)
        self.timeline_dir.mkdir(parents=True, exist_ok=True)

        # Fichier timeline principal (JSONL)
        self.cycles_file = self.timeline_dir / "mind_timeline.jsonl"
        self.patterns_file = self.timeline_dir / "detected_patterns.jsonl"

        # État en mémoire pour performance
        self.recent_cycles: list[CognitiveCycle] = []
        self.current_cycle_start: datetime | None = None

        logger.info(f"🕰️ Chronalia initialized - Timeline: {timeline_dir}")

    def start_cycle(self) -> str:
        """🔄 Démarre un nouveau cycle cognitif"""
        self.current_cycle_start = datetime.now()
        cycle_id = f"cycle_{self.current_cycle_start.strftime('%Y%m%d_%H%M%S_%f')}"
        logger.debug(f"🔄 Cycle cognitif démarré: {cycle_id}")
        return cycle_id

    def complete_cycle(
        self, context: dict[str, Any], cognitive_reactions: list[str] | None = None
    ) -> CognitiveCycle:
        """✅ Complète et persiste un cycle cognitif"""

        if not self.current_cycle_start:
            logger.warning("⚠️ Aucun cycle en cours - création automatique")
            self.start_cycle()

        # Calcul durée cycle
        if self.current_cycle_start is None:
            cycle_duration_ms = 0
        else:
            cycle_duration = datetime.now() - self.current_cycle_start
            cycle_duration_ms = int(cycle_duration.total_seconds() * 1000)

        # Construction du cycle selon tes spécifications exactes
        cycle = CognitiveCycle(
            timestamp=self.current_cycle_start.isoformat(),
            reflexia_score=context.get("reflexia_score", 0.5),
            sandozia_health=context.get("sandozia_health", 0.5),
            contradiction=context.get("contradiction", False),
            decision_pattern=context.get("decision_pattern", "normal"),
            zeroia_decision=context.get("zeroia_decision", "monitor"),
            confidence=context.get("confidence", 0.5),
            system_cpu=context.get("system_cpu", 50),
            system_ram=context.get("system_ram", 50),
            modules_active=context.get("modules_active", ["zeroia", "reflexia", "sandozia"]),
            quarantined_modules=context.get("quarantined_modules", []),
            berserk_mode=context.get("berserk_mode", False),
            cognitive_reactions=(cognitive_reactions if cognitive_reactions is not None else []),
            cycle_duration_ms=cycle_duration_ms,
            pattern_repetition_count=context.get("pattern_repetition_count", 0),
            global_health_score=context.get("global_health_score", 0.5),
        )

        # Persister au format JSONL
        self._persist_cycle(cycle)

        # Ajouter en mémoire
        self.recent_cycles.append(cycle)
        if len(self.recent_cycles) > 1000:  # Limite mémoire
            self.recent_cycles.pop(0)

        # Reset état
        self.current_cycle_start = None

        logger.info(f"✅ Cycle cognitif complété - Durée: {cycle_duration_ms}ms")
        return cycle

    def get_heatmap_data(self, hours_back: int = 24) -> dict[str, Any]:
        """📊 Génère données heatmap cognitive pour Grafana"""

        since = datetime.now() - timedelta(hours=hours_back)
        cycles = self._load_cycles_since(since)

        # Heatmap par intervalles de 5 minutes
        heatmap = {}
        resolution_minutes = 5

        for cycle in cycles:
            cycle_time = datetime.fromisoformat(cycle.timestamp)

            # Bucket temporel
            bucket_time = cycle_time.replace(
                minute=(cycle_time.minute // resolution_minutes) * resolution_minutes,
                second=0,
                microsecond=0,
            )
            bucket_key = bucket_time.isoformat()

            if bucket_key not in heatmap:
                heatmap[bucket_key] = {
                    "timestamp": bucket_key,
                    "cycles_count": 0,
                    "avg_confidence": 0,
                    "contradictions_count": 0,
                    "berserk_count": 0,
                    "quarantined_modules": 0,
                    "modules_noise_level": 0,  # Niveau "bruit" modules
                    "decisions": {},
                }

            bucket = heatmap[bucket_key]
            bucket["cycles_count"] += 1
            bucket["avg_confidence"] += cycle.confidence

            if cycle.contradiction:
                bucket["contradictions_count"] += 1
            if cycle.berserk_mode:
                bucket["berserk_count"] += 1

            bucket["quarantined_modules"] += len(cycle.quarantined_modules)

            # Comptage décisions
            decision = cycle.zeroia_decision
            bucket["decisions"][decision] = bucket["decisions"].get(decision, 0) + 1

            # 🎯 Calcul "bruit" des modules (instabilité)
            noise = (
                len(cycle.cognitive_reactions) * 0.1
                + len(cycle.quarantined_modules) * 0.2
                + (1 if cycle.contradiction else 0) * 0.3
                + (1 if cycle.berserk_mode else 0) * 0.5
            )
            bucket["modules_noise_level"] += noise

        # Moyennes finales
        for bucket in heatmap.values():
            count = bucket["cycles_count"]
            if count > 0:
                bucket["avg_confidence"] /= count
                bucket["modules_noise_level"] /= count

        return {
            "heatmap_data": list(heatmap.values()),
            "summary": {
                "total_cycles": len(cycles),
                "time_range_hours": hours_back,
                "resolution_minutes": resolution_minutes,
                "generated_at": datetime.now().isoformat(),
            },
        }

    def detect_patterns(self, window_minutes: int = 30) -> list[dict[str, Any]]:
        """🔍 Détecte patterns temporels automatiquement"""

        since = datetime.now() - timedelta(minutes=window_minutes)
        cycles = self._load_cycles_since(since)
        patterns = []

        if len(cycles) < 3:
            return patterns

        # 🎯 Pattern 1: Décisions répétitives (ton cas d'usage principal)
        recent_decisions = [cycle.zeroia_decision for cycle in cycles[-10:]]
        unique_decisions = set(recent_decisions)

        if len(unique_decisions) == 1 and len(recent_decisions) >= 7:
            pattern = {
                "pattern_type": "repetitive_decisions",
                "severity": "high",
                "description": f"{len(recent_decisions)} décisions identiques: {list(unique_decisions)[0]}",
                "detected_at": datetime.now().isoformat(),
                "repetition_count": len(recent_decisions),
                "trigger_cognitive_pause": True,
            }
            patterns.append(pattern)
            self._persist_pattern(pattern)

        # 🎯 Pattern 2: Confiance en chute libre
        confidences = [cycle.confidence for cycle in cycles[-5:]]
        if len(confidences) >= 3:
            trend_down = all(
                confidences[i] > confidences[i + 1] for i in range(len(confidences) - 1)
            )
            if trend_down and confidences[-1] < 0.3:
                pattern = {
                    "pattern_type": "confidence_collapse",
                    "severity": "critical",
                    "description": f"Confiance effondrée: {confidences[0]:.2f} → {confidences[-1]:.2f}",
                    "detected_at": datetime.now().isoformat(),
                    "trigger_berserk_check": True,
                }
                patterns.append(pattern)
                self._persist_pattern(pattern)

        return patterns

    def export_timeline(self, hours_back: int = 24) -> Path:
        """📤 Exporte timeline complète pour analyse"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.timeline_dir / f"mind_timeline_export_{timestamp}.json"

        since = datetime.now() - timedelta(hours=hours_back)
        cycles = self._load_cycles_since(since)

        export_data = {
            "export_metadata": {
                "generated_at": datetime.now().isoformat(),
                "time_range_hours": hours_back,
                "total_cycles": len(cycles),
                "arkalia_version": "v3.0-phase1",
            },
            "cognitive_cycles": [asdict(cycle) for cycle in cycles],
            "heatmap_data": self.get_heatmap_data(hours_back),
        }

        with output_file.open("w") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        logger.info(f"📤 Timeline exportée: {output_file} ({len(cycles)} cycles)")
        return output_file

    def _persist_cycle(self, cycle: CognitiveCycle):
        """💾 Persiste cycle au format JSONL"""
        try:
            with self.cycles_file.open("a") as f:
                f.write(json.dumps(asdict(cycle), ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"❌ Erreur persistence cycle: {e}")

    def _persist_pattern(self, pattern: dict[str, Any]):
        """💾 Persiste pattern détecté"""
        try:
            with self.patterns_file.open("a") as f:
                f.write(json.dumps(pattern, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"❌ Erreur persistence pattern: {e}")

    def _load_cycles_since(self, since: datetime) -> list[CognitiveCycle]:
        """📖 Charge cycles depuis une date"""
        cycles = []

        if not self.cycles_file.exists():
            return cycles

        try:
            with self.cycles_file.open("r") as f:
                for line in f:
                    cycle_data = json.loads(line.strip())
                    cycle_time = datetime.fromisoformat(cycle_data["timestamp"])

                    if cycle_time >= since:
                        cycles.append(CognitiveCycle(**cycle_data))
        except Exception as e:
            logger.error(f"❌ Erreur chargement cycles: {e}")

        return cycles


# 🚀 Factory et intégration
def create_chronalia(timeline_dir: str = "state/chronalia") -> Chronalia:
    """Crée une instance de Chronalia"""
    return Chronalia(timeline_dir)


def log_cognitive_cycle(
    context: dict[str, Any], cognitive_reactions: list[str] | None = None
) -> CognitiveCycle:
    """
    🧪 INTÉGRATION SIMPLE avec ton reason_loop

    Usage dans reason_loop_enhanced.py :

    from modules.sandozia.core.chronalia import log_cognitive_cycle

    # À la fin de chaque décision :
    cycle = log_cognitive_cycle({
        "reflexia_score": 0.85,
        "sandozia_health": 0.92,
        "contradiction": False,
        "decision_pattern": "adaptive",
        "zeroia_decision": decision,
        "confidence": confidence,
        "system_cpu": cpu_usage,
        "system_ram": ram_usage,
        "modules_active": ["zeroia", "reflexia", "sandozia"],
        "quarantined_modules": quarantined_list,
        "berserk_mode": berserk_active
    }, cognitive_reactions)
    """
    chronalia = create_chronalia()

    # Auto-start cycle si pas en cours
    if not chronalia.current_cycle_start:
        chronalia.start_cycle()

    return chronalia.complete_cycle(context, cognitive_reactions)
