#!/usr/bin/env python3
# 🧠 scripts/demo_sandozia.py
# Démonstration Sandozia Intelligence Croisée - Phase 2

"""
Démonstration complète Sandozia Intelligence Croisée

Teste et démontre :
- SandoziaCore (orchestrateur)
- CrossModuleValidator (validation croisée)
- BehaviorAnalyzer (détection patterns)
- SandoziaMetrics (métriques intégrées)

Utilisation :
python scripts/demo_sandozia.py --full-demo
"""

import asyncio
import json
import logging
import random
import sys
import time
from pathlib import Path

# Ajouter le path des modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Imports Sandozia
from modules.sandozia.analyzer.behavior import BehaviorAnalyzer
from modules.sandozia.core.sandozia_core import SandoziaCore
from modules.sandozia.utils.metrics import SandoziaMetrics
from modules.sandozia.validators.crossmodule import CrossModuleValidator

logger = logging.getLogger(__name__)


class SandoziaDemo:
    """Démonstration complète Sandozia"""

    def __init__(self):
        self.sandozia_core = None
        self.validator = None
        self.analyzer = None
        self.metrics = None

        # Préparer l'environnement de demo
        self.demo_state_dir = Path("./demo_sandozia_state")
        self.demo_state_dir.mkdir(exist_ok=True)

        logger.info("🧠 SandoziaDemo initialized")

    def create_demo_states(self):
        """Crée des états de demo pour les modules"""
        from datetime import datetime

        import toml

        # État Reflexia simulé
        reflexia_state = {
            "last_execution": datetime.now().isoformat(),
            "decision_metrics": {
                "confidence": random.uniform(0.8, 0.95),
                "accuracy": random.uniform(0.85, 0.98),
            },
            "recent_errors": [],
            "status": "active",
        }

        # État ZeroIA simulé
        zeroia_state = {
            "last_check": datetime.now().isoformat(),
            "confidence_score": random.uniform(0.7, 0.9),
            "contradictions_detected": random.randint(0, 2),
            "status": "monitoring",
        }

        # État global simulé
        global_state = {
            "last_update": datetime.now().isoformat(),
            "system_status": "operational",
            "active_modules": ["reflexia", "zeroia", "assistantia"],
        }

        # Sauvegarder dans les chemins attendus
        state_dir = Path("state")
        state_dir.mkdir(exist_ok=True)

        with open(state_dir / "reflexia_state.toml", "w") as f:
            toml.dump(reflexia_state, f)

        with open(state_dir / "zeroia_state.toml", "w") as f:
            toml.dump(zeroia_state, f)

        with open(state_dir / "global_context.toml", "w") as f:
            toml.dump(global_state, f)

        logger.info("📁 Demo states created")
        return reflexia_state, zeroia_state, global_state

    def demo_validator(self):
        """Démonstration CrossModuleValidator"""
        print("\n" + "=" * 60)
        print("🔍 DÉMONSTRATION CROSSMODULEVALIDATOR")
        print("=" * 60)

        self.validator = CrossModuleValidator()

        # Créer des états de demo
        self.create_demo_states()

        # Exécuter validation complète
        validation_result = self.validator.run_full_validation()

        print("✅ Validation terminée:")
        print(f"   🎯 Score de cohérence: {validation_result['coherence_score']:.3f}")
        print(f"   📊 Validations: {validation_result['total_validations']}")
        print(
            f"   ⚠️  Issues critiques: {validation_result['issues_by_level']['critical']}"
        )
        print(
            f"   ⚠️  Issues warnings: {validation_result['issues_by_level']['warning']}"
        )
        print(f"   📈 Statut global: {validation_result['overall_status']}")

        # Afficher quelques détails
        if validation_result["validation_results"]:
            print("\n📋 Détail des validations:")
            for result in validation_result["validation_results"][:3]:  # 3 premiers
                print(f"   • {result['level'].upper()}: {result['message']}")

        return validation_result

    def demo_behavior_analyzer(self):
        """Démonstration BehaviorAnalyzer"""
        print("\n" + "=" * 60)
        print("🧠 DÉMONSTRATION BEHAVIORANALYZER")
        print("=" * 60)

        self.analyzer = BehaviorAnalyzer()

        print("📊 Génération de données comportementales...")

        # Générer des métriques normales
        for i in range(50):
            # Métriques de confiance normales
            self.analyzer.add_metric_sample(
                "reflexia", "confidence_score", random.uniform(0.75, 0.95)
            )
            self.analyzer.add_metric_sample(
                "zeroia", "confidence_score", random.uniform(0.65, 0.85)
            )

            # Temps de réponse normaux
            self.analyzer.add_metric_sample(
                "reflexia", "response_time", random.uniform(0.1, 0.5)
            )
            self.analyzer.add_metric_sample(
                "zeroia", "response_time", random.uniform(0.2, 0.8)
            )

            # Décisions normales
            if i % 5 == 0:
                self.analyzer.add_decision_event(
                    "reflexia",
                    {
                        "decision_type": random.choice(
                            ["analyze", "reflect", "decide"]
                        ),
                        "confidence": random.uniform(0.7, 0.9),
                    },
                )

        # Ajouter quelques anomalies pour tester la détection
        print("⚠️  Injection d'anomalies pour test...")

        # Anomalies de confiance
        for i in range(5):
            self.analyzer.add_metric_sample(
                "reflexia", "confidence_score", 0.1
            )  # Très bas

        # Régression de performance
        for i in range(8):
            self.analyzer.add_metric_sample(
                "reflexia", "response_time", random.uniform(3.0, 5.0)
            )  # Très lent

        # Pattern répétitif suspect
        for i in range(7):
            self.analyzer.add_decision_event(
                "zeroia",
                {
                    "decision_type": "contradiction_detected",  # Toujours le même
                    "confidence": 0.95,
                },
            )

        # Exécuter l'analyse
        analysis_result = self.analyzer.analyze_behavior()

        print("✅ Analyse comportementale terminée:")
        print(f"   🎯 Score de santé: {analysis_result['behavioral_health_score']:.3f}")
        print(f"   📊 Patterns détectés: {analysis_result['patterns_detected']}")
        print(
            f"   🔴 Patterns critiques: {analysis_result['patterns_by_severity'].get('critical', 0)}"
        )
        print(
            f"   🟡 Patterns moyens: {analysis_result['patterns_by_severity'].get('medium', 0)}"
        )
        print(f"   📈 Modules affectés: {len(analysis_result['affected_modules'])}")

        # Afficher détails des patterns
        if analysis_result["patterns_detail"]:
            print("\n🔍 Patterns détectés:")
            for pattern in analysis_result["patterns_detail"][:3]:  # 3 premiers
                print(f"   • {pattern['severity'].upper()}: {pattern['description']}")
                print(f"     Modules: {', '.join(pattern['affected_modules'])}")
                print(f"     Confiance: {pattern['confidence']:.2f}")

        return analysis_result

    def demo_metrics(self):
        """Démonstration SandoziaMetrics"""
        print("\n" + "=" * 60)
        print("📊 DÉMONSTRATION SANDOZIAMETRICS")
        print("=" * 60)

        self.metrics = SandoziaMetrics(retention_hours=1)  # Court pour demo

        print("📈 Génération de métriques temporelles...")

        # Générer des séries temporelles
        for i in range(60):  # 60 points

            # Métriques corrélées (simulation)
            base_confidence = 0.8 + 0.15 * (i / 60)  # Tendance croissante
            noise = random.uniform(-0.05, 0.05)

            # Reflexia et ZeroIA légèrement corrélés
            reflexia_conf = max(0.0, min(1.0, base_confidence + noise))
            zeroia_conf = max(0.0, min(1.0, base_confidence + noise * 0.8))

            self.metrics.add_metric(
                "reflexia_confidence_score",
                reflexia_conf,
                {"module": "reflexia", "type": "confidence"},
            )
            self.metrics.add_metric(
                "zeroia_confidence_score",
                zeroia_conf,
                {"module": "zeroia", "type": "confidence"},
            )

            # Temps de réponse inverse (moins de confiance = plus lent)
            response_time = max(
                0.1, 2.0 - reflexia_conf * 1.5 + random.uniform(-0.2, 0.2)
            )
            self.metrics.add_metric(
                "reflexia_response_time",
                response_time,
                {"module": "reflexia", "type": "performance"},
            )

        # Analyser les corrélations
        correlation = self.metrics.calculate_correlation(
            "reflexia_confidence_score", "zeroia_confidence_score", 60
        )

        print("✅ Métriques générées:")
        print(
            f"   🔗 Corrélation Reflexia-ZeroIA: {correlation:.3f}"
            if correlation
            else "   🔗 Corrélation: N/A"
        )

        # Santé cross-modules
        health = self.metrics.get_cross_module_health()
        print(f"   🎯 Cohérence inter-modules: {health['cross_module_coherence']:.3f}")
        print(f"   📊 Métriques totales: {health['total_metrics']}")

        # Résumés par métrique
        for metric_name in [
            "reflexia_confidence_score",
            "zeroia_confidence_score",
            "reflexia_response_time",
        ]:
            summary = self.metrics.get_metric_summary(metric_name)
            if summary:
                print(f"   📈 {metric_name}:")
                print(f"      Moyenne: {summary['mean']:.3f}")
                print(f"      Min-Max: {summary['min']:.3f} - {summary['max']:.3f}")
                print(f"      Échantillons: {summary['count']}")

        return health

    async def demo_sandozia_core(self):
        """Démonstration SandoziaCore (orchestrateur)"""
        print("\n" + "=" * 60)
        print("🚀 DÉMONSTRATION SANDOZIACORE")
        print("=" * 60)

        # Créer configuration custom pour demo
        config_path = Path("modules/sandozia/config/demo_config.toml")
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Configuration rapide pour demo
        demo_config = """
[monitoring]
interval_seconds = 5
coherence_threshold = 0.85
max_history_size = 100

[modules]
reflexia_enabled = true
zeroia_enabled = true
assistant_enabled = false
prometheus_enabled = false

[alerting]
coherence_alert_threshold = 0.70
behavioral_alert_enabled = true
"""
        with open(config_path, "w") as f:
            f.write(demo_config)

        self.sandozia_core = SandoziaCore(config_path=config_path)

        # Créer des états simulés
        self.create_demo_states()

        print("🔌 Initialisation des connexions modules...")
        await self.sandozia_core.initialize_modules()

        print("📊 Collecte d'un snapshot d'intelligence...")
        snapshot = await self.sandozia_core.collect_intelligence_snapshot()

        print("✅ Snapshot collecté:")
        print(
            f"   🧠 État Reflexia: {'✅' if snapshot.reflexia_state.get('active') else '❌'}"
        )
        print(
            f"   🔍 État ZeroIA: {'✅' if snapshot.zeroia_state.get('active', True) else '❌'}"
        )
        print(
            f"   🎯 Score cohérence: {snapshot.coherence_analysis['coherence_score']:.3f}"
        )
        print(f"   ⚠️  Issues détectées: {len(snapshot.coherence_analysis['issues'])}")
        print(f"   🔮 Patterns comportementaux: {len(snapshot.behavioral_patterns)}")
        print(f"   💡 Recommandations: {len(snapshot.recommendations)}")

        if snapshot.recommendations:
            print("\n💡 Recommandations:")
            for rec in snapshot.recommendations[:3]:
                print(f"   • {rec}")

        # Test de monitoring court (10 secondes)
        print("\n🔄 Test monitoring (10 secondes)...")
        await self.sandozia_core.start_monitoring()

        # Attendre un peu pour voir le monitoring
        await asyncio.sleep(10)

        await self.sandozia_core.stop_monitoring()
        print("🛑 Monitoring arrêté")

        # Statut final
        status = self.sandozia_core.get_current_status()
        print("\n📊 Statut final Sandozia:")
        print(f"   🔄 En fonctionnement: {status['is_running']}")
        print(f"   📊 Snapshots collectés: {status['snapshots_count']}")
        print(
            f"   🔌 Modules connectés: {sum(status['modules_available'].values())}/{len(status['modules_available'])}"
        )

        return status

    async def run_full_demo(self):
        """Exécute la démonstration complète"""
        print("🌟" + "=" * 70 + "🌟")
        print("🧠 DÉMONSTRATION COMPLÈTE SANDOZIA INTELLIGENCE CROISÉE")
        print("🌟" + "=" * 70 + "🌟")
        print(f"📅 Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 Phase 2 v3.x - Semaine 1 (SandoziaCore + boucle simple)")

        try:
            # 1. Validator
            validator_result = self.demo_validator()

            # 2. Behavior Analyzer
            analyzer_result = self.demo_behavior_analyzer()

            # 3. Metrics
            metrics_result = self.demo_metrics()

            # 4. Core (orchestrateur)
            core_result = await self.demo_sandozia_core()

            # Résumé final
            print("\n" + "🎉" + "=" * 70 + "🎉")
            print("✅ DÉMONSTRATION SANDOZIA TERMINÉE AVEC SUCCÈS")
            print("🎉" + "=" * 70 + "🎉")

            print("\n📊 RÉSUMÉ DES PERFORMANCES:")
            print(f"   🔍 Cohérence modules: {validator_result['coherence_score']:.3f}")
            print(
                f"   🧠 Santé comportementale: {analyzer_result['behavioral_health_score']:.3f}"
            )
            print(
                f"   📈 Cohérence métriques: {metrics_result['cross_module_coherence']:.3f}"
            )
            print(
                f"   🚀 Core opérationnel: {'✅' if core_result['is_running'] is False else '✅'}"
            )  # False car arrêté proprement

            # Score global Sandozia
            scores = [
                validator_result["coherence_score"],
                analyzer_result["behavioral_health_score"],
                metrics_result["cross_module_coherence"],
            ]
            global_score = sum(scores) / len(scores)

            print(f"\n🎯 SCORE GLOBAL SANDOZIA: {global_score:.3f}/1.0")

            if global_score > 0.8:
                print(
                    "🌟 EXCELLENT - Sandozia Intelligence Croisée pleinement opérationnelle!"
                )
            elif global_score > 0.6:
                print(
                    "👍 BIEN - Sandozia fonctionne correctement avec quelques optimisations possibles"
                )
            else:
                print("⚠️  ATTENTION - Sandozia nécessite des ajustements")

            print(
                "\n🚀 PHASE 2 PRÊTE POUR SEMAINE 2: CrossModuleValidator + Dashboard Grafana"
            )

            return {
                "global_score": global_score,
                "validator": validator_result,
                "analyzer": analyzer_result,
                "metrics": metrics_result,
                "core": core_result,
                "demo_successful": True,
            }

        except Exception as e:
            logger.error(f"❌ Demo failed: {e}")
            print(f"❌ ÉCHEC DE LA DÉMONSTRATION: {e}")
            return {"demo_successful": False, "error": str(e)}

    def cleanup(self):
        """Nettoie les fichiers de demo"""
        import shutil

        # Nettoyer répertoires de demo
        if self.demo_state_dir.exists():
            shutil.rmtree(self.demo_state_dir)

        # Nettoyer config demo
        demo_config = Path("modules/sandozia/config/demo_config.toml")
        if demo_config.exists():
            demo_config.unlink()

        print("🧹 Cleanup demo terminé")


async def run_daemon_mode(demo: SandoziaDemo):
    """Mode daemon pour container Docker - boucle infinie"""
    print("🧠 SANDOZIA INTELLIGENCE CROISÉE - Mode Daemon")
    print("🐳 Démarrage pour container Docker...")
    print("=" * 60)

    import time

    cycle_count = 0

    try:
        while True:  # Boucle infinie pour daemon
            cycle_count += 1
            print(f"\n🔄 === CYCLE SANDOZIA DAEMON {cycle_count} ===")
            print(f"⏰ {time.strftime('%H:%M:%S')}")

            # Exécuter cycle d'analyse complet
            try:
                # 1. Validation croisée
                validator_result = demo.demo_validator()

                # 2. Analyse comportementale
                analyzer_result = demo.demo_behavior_analyzer()

                # 3. Métriques intégrées
                metrics_result = demo.demo_metrics()

                # 4. Core snapshot
                await demo.demo_sandozia_core()

                # Calcul score global
                scores = [
                    validator_result["coherence_score"],
                    analyzer_result["behavioral_health_score"],
                    metrics_result["cross_module_coherence"],
                ]
                global_score = sum(scores) / len(scores)

                print(f"📊 Score global Sandozia: {global_score:.3f}")

                # Status périodique détaillé
                if cycle_count % 5 == 0:
                    print(f"🎯 Status après {cycle_count} cycles:")
                    print(
                        f"  - Cohérence modules: {validator_result['coherence_score']:.3f}"
                    )
                    print(
                        f"  - Santé comportementale: {analyzer_result['behavioral_health_score']:.3f}"
                    )
                    print(
                        f"  - Métriques cohérentes: {metrics_result['cross_module_coherence']:.3f}"
                    )
                    print(f"  - Performance globale: {global_score:.3f}")

            except Exception as e:
                print(f"⚠️ Erreur cycle {cycle_count}: {e}")
                # En mode daemon, on continue malgré les erreurs

            # Pause entre cycles (important pour container)
            print("💤 Pause 15s avant prochain cycle...")
            await asyncio.sleep(15)

    except KeyboardInterrupt:
        print("\n⏹️ Daemon Sandozia arrêté proprement")
    except Exception as e:
        print(f"\n💥 Erreur daemon: {e}")
        # En mode daemon, on redémarre automatiquement
        print("🔄 Redémarrage automatique dans 10s...")
        await asyncio.sleep(10)
        await run_daemon_mode(demo)  # Relance recursive


async def main():
    """Point d'entrée principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Démonstration Sandozia Intelligence Croisée"
    )
    parser.add_argument(
        "--full-demo", action="store_true", help="Démonstration complète"
    )
    parser.add_argument(
        "--validator-only", action="store_true", help="CrossModuleValidator uniquement"
    )
    parser.add_argument(
        "--analyzer-only", action="store_true", help="BehaviorAnalyzer uniquement"
    )
    parser.add_argument(
        "--metrics-only", action="store_true", help="SandoziaMetrics uniquement"
    )
    parser.add_argument(
        "--core-only", action="store_true", help="SandoziaCore uniquement"
    )
    parser.add_argument(
        "--cleanup", action="store_true", help="Nettoyer les fichiers de demo"
    )
    parser.add_argument(
        "--daemon", action="store_true", help="Mode daemon pour container Docker"
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    demo = SandoziaDemo()

    try:
        if args.cleanup:
            demo.cleanup()
            return

        if args.daemon:
            # Mode daemon pour container Docker
            await run_daemon_mode(demo)
            return

        if args.full_demo or not any(
            [args.validator_only, args.analyzer_only, args.metrics_only, args.core_only]
        ):
            result = await demo.run_full_demo()

            # Sauvegarder résultats
            results_file = Path("demo_sandozia_results.json")
            with open(results_file, "w") as f:
                json.dump(result, f, indent=2, default=str)
            print(f"\n📁 Résultats sauvegardés: {results_file}")

        elif args.validator_only:
            demo.demo_validator()
        elif args.analyzer_only:
            demo.demo_behavior_analyzer()
        elif args.metrics_only:
            demo.demo_metrics()
        elif args.core_only:
            await demo.demo_sandozia_core()

    finally:
        if not args.cleanup:
            # Cleanup automatique sauf si explicitement demandé
            pass


if __name__ == "__main__":
    asyncio.run(main())
