#!/usr/bin/env python3
# 🚀 scripts/arkalia_enhanced_integration.py
# Intégration complète des recommandations Arkalia-LUNA Enhanced v3.0-phase1+

"""
🎯 INTÉGRATION COMPLÈTE - Toutes tes recommandations implémentées

✅ 1. Réaction automatique (7+ décisions identiques → pause cognitive)
✅ 2. Timeline cognitive (Chronalia  # noqa: F401  JSONL)
✅ 3. Mode quarantine cognitive
✅ 4. Heatmap cognitive Grafana
✅ 5. Mode Berserk/Recovery pour effondrements brutaux

Usage:
    python scripts/arkalia_enhanced_integration.py --demo
    python scripts/arkalia_enhanced_integration.py --integrate-with-zeroia
    python scripts/arkalia_enhanced_integration.py --generate-heatmap-data
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Configuration logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Ajout du chemin des modules
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from modules.sandozia.core.chronalia import Chronalia  # noqa: F401
    from modules.sandozia.core.cognitive_reactor import (  # noqa: F401,  # noqa: F401,
        CognitiveReactor,
        QuarantineReason,
        ReactionSeverity,
    )
    from modules.zeroia.event_store import (  # noqa: F401,  # noqa: F401,  # noqa: F401,  # noqa: F401,; noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401
        EventStore,
        EventType,
    )
    from modules.zeroia.reason_loop_enhanced import (  # noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401# noqa: F401
        reason_loop_enhanced_with_recovery,
    )
except ImportError as e:
    logger.error(f"❌ Erreur import modules: {e}")
    logger.error("Assurez-vous d'être dans le répertoire arkalia-luna-pro")
    sys.exit(1)


class ArkaliaEnhancedEngine:
    """
    🚀 Moteur Arkalia Enhanced - Intégration complète

    Combine toutes tes recommandations :
    - CognitiveReactor  # noqa: F401  (réactions automatiques)
    - Chronalia  # noqa: F401  (timeline cognitive)
    - ZeroIA Enhanced (décisions)
    - Métriques pour Grafana heatmap
    """

    def __init__(self) -> None:
        self.cognitive_reactor = CognitiveReactor  # noqa: F401
        self.chronalia = Chronalia  # noqa: F401
        self.event_store = EventStore()  # noqa: F401

        # État système
        self.decision_pattern_count = 0
        self.last_decision = None
        self.global_stats = {
            "total_cycles": 0,
            "cognitive_reactions_triggered": 0,
            "berserk_activations": 0,
            "patterns_detected": 0,
        }

        logger.info("🚀 ArkaliaEnhancedEngine initialisé")

    async def run_enhanced_cycle(self, context: dict | None = None) -> dict:
        """
        🎯 CYCLE ENHANCED COMPLET - Implémentation de tes recommandations

        Flux :
        1. Démarrer cycle Chronalia  # noqa: F401
        2. Analyser contexte et détecter patterns
        3. Décision ZeroIA Enhanced
        4. Réactions automatiques (CognitiveReactor  # noqa: F401 )
        5. Enregistrer timeline
        6. Métriques heatmap
        """

        # 1. Démarrer cycle cognitif
        cycle_id = self.chronalia.start_cycle()

        # 2. Contexte par défaut si non fourni
        if not context:
            context = self._generate_demo_context()

        # 3. Décision ZeroIA Enhanced
        try:
            decision, confidence = reason_loop_enhanced_with_recovery()
            logger.info(f"🧠 Décision ZeroIA: {decision} (confiance: {confidence})")
        except Exception as e:
            raise RuntimeError(f"Erreur d'intégration Arkalia: {e}") from e

        # 4. Détection pattern répétitif (TA RECOMMANDATION CLEF)
        if decision == self.last_decision:
            self.decision_pattern_count += 1
        else:
            self.decision_pattern_count = 1
            self.last_decision = decision

        # 5. Mise à jour contexte avec résultat
        enhanced_context = {
            **context,
            "zeroia_decision": decision,
            "confidence": confidence,
            "decision_pattern": ("identical" if self.decision_pattern_count >= 3 else "normal"),
            "pattern_repetition_count": self.decision_pattern_count,
            "cycle_id": cycle_id,
        }

        # 6. 🔥 RÉACTIONS AUTOMATIQUES (TA RECOMMANDATION 1)
        cognitive_reactions = await self.cognitive_reactor.check_and_react(
            enhanced_context, self.decision_pattern_count
        )

        # 7. Traitement réactions
        reaction_descriptions = []
        for reaction in cognitive_reactions:
            reaction_descriptions.append(f"{reaction.action}:{reaction.severity.value}")
            self.global_stats["cognitive_reactions_triggered"] += 1

            if reaction.severity == ReactionSeverity.BERSERK:
                self.global_stats["berserk_activations"] += 1
                logger.critical(f"🚨 MODE BERSERK DÉCLENCHÉ: {reaction.action}")

        # 8. 🕰️ TIMELINE CHRONALIA (TA RECOMMANDATION 2)
        self.chronalia.complete_cycle(enhanced_context, reaction_descriptions)

        # 9. 🔍 DÉTECTION PATTERNS TEMPORELS
        patterns = self.chronalia.detect_patterns()
        self.global_stats["patterns_detected"] += len(patterns)

        # 10. Métriques pour heatmap Grafana
        heatmap_data = self._generate_heatmap_metrics(enhanced_context, cognitive_reactions)

        # 11. Stats globales
        self.global_stats["total_cycles"] += 1

        # 12. Résultat complet
        result = {
            "cycle_id": cycle_id,
            "decision": decision,
            "confidence": confidence,
            "pattern_count": self.decision_pattern_count,
            "cognitive_reactions": reaction_descriptions,
            "patterns_detected": len(patterns),
            "quarantined_modules": list(self.cognitive_reactor.quarantined_modules.keys()),
            "berserk_mode": self.cognitive_reactor.berserk_mode_active,
            "global_stats": self.global_stats.copy(),
            "heatmap_data": heatmap_data,
            "timeline_recorded": True,
        }

        logger.info(f"✅ Cycle Enhanced complété: {cycle_id}")
        return result

    def _generate_demo_context(self) -> dict:
        """Génère un contexte de démo réaliste"""
        import random

        # Simulation réaliste
        base_cpu = 45 + random.randint(-15, 35)  # 30-80% CPU
        base_ram = 40 + random.randint(-10, 30)  # 30-70% RAM

        return {
            "timestamp": datetime.now().isoformat(),
            "system_cpu": base_cpu,
            "system_ram": base_ram,
            "reflexia_score": round(random.uniform(0.6, 1.0), 3),
            "sandozia_health": round(random.uniform(0.7, 0.95), 3),
            "contradiction": random.choice([False, False, False, True]),  # 25% contradictions
            "modules_active": ["zeroia", "reflexia", "sandozia"],
            "quarantined_modules": [],
            "berserk_mode": False,
            "global_health_score": round(random.uniform(0.5, 0.9), 3),
        }

    def _generate_heatmap_metrics(self, context: dict, reactions: list) -> dict:
        """
        📊 GÉNÈRE MÉTRIQUES HEATMAP (TA RECOMMANDATION 4)

        Format pour Grafana :
        - Niveau de bruit des modules
        - Réactions par type
        - Santé globale
        """

        # Calcul niveau de bruit modules
        noise_level = (
            len(reactions) * 0.1
            + len(context.get("quarantined_modules", [])) * 0.2
            + (1 if context.get("contradiction", False) else 0) * 0.3
            + (1 if context.get("berserk_mode", False) else 0) * 0.5
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "modules_noise_level": round(noise_level, 3),
            "cognitive_reactions_count": len(reactions),
            "quarantined_modules_count": len(context.get("quarantined_modules", [])),
            "contradiction_active": context.get("contradiction", False),
            "berserk_mode_active": context.get("berserk_mode", False),
            "global_health_score": context.get("global_health_score", 0.5),
            "confidence": context.get("confidence", 0.5),
            "cpu_usage": context.get("system_cpu", 50),
            "ram_usage": context.get("system_ram", 50),
        }

    async def run_stress_test(self, cycles: int = 20, force_patterns: bool = True):
        """🧪 Test de stress pour déclencher toutes les réactions"""

        logger.info(f"🧪 Début test de stress - {cycles} cycles")

        results = []

        for i in range(cycles):
            # Contexte de stress progressif
            stress_context = self._generate_demo_context()

            # Force des patterns répétitifs après cycle 10
            if force_patterns and i > 10:
                stress_context.update(
                    {
                        "system_cpu": 85,  # CPU élevé
                        "system_ram": 80,  # RAM élevée
                        "reflexia_score": 0.3,  # Score faible
                        "sandozia_health": 0.2,  # Santé dégradée
                        "contradiction": True,  # Force contradictions
                        "global_health_score": 0.15,  # Proche seuil berserk
                    }
                )

            # Cycle enhanced
            result = await self.run_enhanced_cycle(stress_context)
            results.append(result)

            # Log progression
            if result["cognitive_reactions"]:
                logger.warning(
                    f"🔥 Cycle {i+1}: Réactions déclenchées: {result['cognitive_reactions']}"
                )

            if result["berserk_mode"]:
                logger.critical(f"🚨 Cycle {i+1}: MODE BERSERK ACTIVÉ!")

            # Délai entre cycles
            await asyncio.sleep(0.1)

        # Résumé final
        total_reactions = sum(len(r["cognitive_reactions"]) for r in results)
        berserk_count = sum(1 for r in results if r["berserk_mode"])

        logger.info("🎯 Test de stress terminé:")
        logger.info(f"   - {cycles} cycles exécutés")
        logger.info(f"   - {total_reactions} réactions déclenchées")
        logger.info(f"   - {berserk_count} activations berserk")
        logger.info(f"   - {len(self.cognitive_reactor.quarantined_modules)} modules en quarantine")

        return results

    def export_timeline_and_heatmap(self, hours_back: int = 1) -> dict[str, str]:
        """📤 Exporte timeline et données heatmap"""

        # Export timeline Chronalia  # noqa: F401
        timeline_file = self.chronalia.export_timeline(hours_back)

        # Export données heatmap pour Grafana
        heatmap_data = self.chronalia.get_heatmap_data(hours_back)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        heatmap_file = Path(f"state/chronalia/heatmap_data_{timestamp}.json")

        with heatmap_file.open("w") as f:
            json.dump(heatmap_data, f, indent=2, ensure_ascii=False)

        logger.info("📤 Exports terminés:")
        logger.info(f"   - Timeline: {timeline_file}")
        logger.info(f"   - Heatmap: {heatmap_file}")

        return {"timeline_file": str(timeline_file), "heatmap_file": str(heatmap_file)}

    def get_quarantine_status(self) -> dict:
        """🔒 État complet des quarantines"""
        return self.cognitive_reactor.get_quarantine_status()

    def get_system_summary(self) -> dict:
        """📊 Résumé système complet"""
        return {
            "arkalia_version": "v3.0-phase1",
            "enhanced_features_active": True,
            "global_stats": self.global_stats,
            "quarantined_modules": list(self.cognitive_reactor.quarantined_modules.keys()),
            "berserk_mode_active": self.cognitive_reactor.berserk_mode_active,
            "recent_cycles_count": len(self.chronalia.recent_cycles),
            "last_decision": self.last_decision,
            "pattern_count": self.decision_pattern_count,
            "cognitive_reactor_active": True,
            "chronalia_active": True,
            "timeline_file": str(self.chronalia.cycles_file),
        }


# 🚀 FONCTIONS UTILITAIRES
async def demo_complete_workflow():
    """🎯 Démo workflow complet des recommandations"""

    print("\n🚀 DÉMO ARKALIA-LUNA ENHANCED v3.0-phase1+")
    print("=" * 60)
    print("🎯 Implémentation complète de tes recommandations :")
    print("   ✅ 1. Réactions automatiques (7+ répétitions → pause)")
    print("   ✅ 2. Timeline cognitive (Chronalia  # noqa: F401  JSONL)")
    print("   ✅ 3. Mode quarantine cognitive")
    print("   ✅ 4. Données heatmap Grafana")
    print("   ✅ 5. Mode Berserk/Recovery pour panics")
    print()

    engine = ArkaliaEnhancedEngine()

    # Test cycles normaux
    print("🔄 Exécution 5 cycles normaux...")
    for i in range(5):
        result = await engine.run_enhanced_cycle()
        print(f"   Cycle {i+1}: {result['decision']} (confiance: {result['confidence']:.2f})")

    print()

    # Test de stress pour déclencher réactions
    print("🧪 Test de stress (patterns répétitifs + dégradation)...")
    await engine.run_stress_test(cycles=15, force_patterns=True)

    print()

    # Résumé final
    summary = engine.get_system_summary()
    print("📊 RÉSUMÉ FINAL:")
    print(f"   - Cycles totaux: {summary['global_stats']['total_cycles']}")
    print(f"   - Réactions déclenchées: {summary['global_stats']['cognitive_reactions_triggered']}")
    print(f"   - Activations berserk: {summary['global_stats']['berserk_activations']}")
    print(f"   - Modules en quarantine: {len(summary['quarantined_modules'])}")
    print(f"   - Patterns détectés: {summary['global_stats']['patterns_detected']}")

    # Export timeline et heatmap
    print("\n📤 Export timeline et données heatmap...")
    exports = engine.export_timeline_and_heatmap()
    print(f"   - Timeline: {exports['timeline_file']}")
    print(f"   - Heatmap: {exports['heatmap_file']}")

    print("\n🎉 DÉMO TERMINÉE - Toutes tes recommandations fonctionnelles !")
    print(f"📋 Timeline disponible: {summary['timeline_file']}")

    return engine


async def integrate_with_zeroia():
    """🔗 Intégration avec le reason_loop ZeroIA existant"""

    print("🔗 Intégration avec ZeroIA Enhanced...")

    engine = ArkaliaEnhancedEngine()

    # Simulation intégration
    for i in range(10):
        context = {
            "real_integration": True,
            "zeroia_call": True,
            "timestamp": datetime.now().isoformat(),
        }

        result = await engine.run_enhanced_cycle(context)

        if result["cognitive_reactions"]:
            print(f"🔥 Réactions automatiques cycle {i+1}: {result['cognitive_reactions']}")

    print("✅ Intégration ZeroIA testée avec succès")


def generate_heatmap_sample():
    """📊 Génère échantillon données heatmap pour Grafana"""

    print("📊 Génération données heatmap pour Grafana...")

    chronalia = Chronalia  # noqa: F401
    heatmap_data = chronalia.get_heatmap_data(hours_back=24)

    output_file = Path("state/chronalia/grafana_heatmap_sample.json")
    with output_file.open("w") as f:
        json.dump(heatmap_data, f, indent=2, ensure_ascii=False)

    print(f"📊 Données heatmap générées: {output_file}")
    print(f"   - {len(heatmap_data['heatmap_data'])} points de données")
    print(f"   - Résolution: {heatmap_data['summary']['resolution_minutes']} minutes")


# 🎯 MAIN
async def main():
    """Point d'entrée principal"""

    import argparse

    parser = argparse.ArgumentParser(description="🚀 Arkalia-LUNA Enhanced Integration")
    parser.add_argument("--demo", action="store_true", help="Démo workflow complet")
    parser.add_argument(
        "--integrate-with-zeroia", action="store_true", help="Test intégration ZeroIA"
    )
    parser.add_argument(
        "--generate-heatmap-data", action="store_true", help="Génère données heatmap"
    )
    parser.add_argument("--stress-test", type=int, help="Test de stress (nombre de cycles)")

    args = parser.parse_args()

    if args.demo:
        await demo_complete_workflow()
    elif args.integrate_with_zeroia:
        await integrate_with_zeroia()
    elif args.generate_heatmap_data:
        generate_heatmap_sample()
    elif args.stress_test:
        engine = ArkaliaEnhancedEngine()
        await engine.run_stress_test(cycles=args.stress_test)
    else:
        # Par défaut : démo
        await demo_complete_workflow()


if __name__ == "__main__":
    asyncio.run(main())
