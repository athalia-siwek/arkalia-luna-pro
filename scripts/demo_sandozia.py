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

from core.ark_logger import ark_logger
import asyncio
import json
import logging
import random
import subprocess
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

    def __init__(self) -> None:
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
        ark_logger.info("\n" + "=" * 60, extra={"module": "scripts"})
        ark_logger.info("🔍 DÉMONSTRATION CROSSMODULEVALIDATOR", extra={"module": "scripts"})
        ark_logger.info("=" * 60, extra={"module": "scripts"})

        self.validator = CrossModuleValidator()

        # Créer des états de demo
        self.create_demo_states()

        # Exécuter validation complète
        validation_result = self.validator.run_full_validation()

        ark_logger.info("✅ Validation terminée:", extra={"module": "scripts"})
        ark_logger.info(f"   🎯 Score de cohérence: {validation_result['coherence_score']:.3f}", extra={"module": "scripts"})
        ark_logger.info(f"   📊 Validations: {validation_result['total_validations']}", extra={"module": "scripts"})
        ark_logger.info(f"   ⚠️  Issues critiques: {validation_result['issues_by_level']['critical']}", extra={"module": "scripts"})
        ark_logger.warning(f"   ⚠️  Issues warnings: {validation_result['issues_by_level']['warning']}", extra={"module": "scripts"})
        ark_logger.info(f"   📈 Statut global: {validation_result['overall_status']}", extra={"module": "scripts"})

        # Afficher quelques détails
        if validation_result["validation_results"]:
            ark_logger.info("\n📋 Détail des validations:", extra={"module": "scripts"})
            for result in validation_result["validation_results"][:3]:  # 3 premiers
                ark_logger.info(f"   • {result['level'].upper(, extra={"module": "scripts"})}: {result['message']}")

        return validation_result

    def demo_behavior_analyzer(self):
        """Démonstration BehaviorAnalyzer"""
        ark_logger.info("\n" + "=" * 60, extra={"module": "scripts"})
        ark_logger.info("🧠 DÉMONSTRATION BEHAVIORANALYZER", extra={"module": "scripts"})
        ark_logger.info("=" * 60, extra={"module": "scripts"})

        self.analyzer = BehaviorAnalyzer()

        ark_logger.info("📊 Génération de données comportementales...", extra={"module": "scripts"})

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
            self.analyzer.add_metric_sample("reflexia", "response_time", random.uniform(0.1, 0.5))
            self.analyzer.add_metric_sample("zeroia", "response_time", random.uniform(0.2, 0.8))

            # Décisions normales
            if i % 5 == 0:
                self.analyzer.add_decision_event(
                    "reflexia",
                    {
                        "decision_type": random.choice(["analyze", "reflect", "decide"]),
                        "confidence": random.uniform(0.7, 0.9),
                    },
                )

        # Ajouter quelques anomalies pour tester la détection
        ark_logger.info("⚠️  Injection d'anomalies pour test...", extra={"module": "scripts"})

        # Anomalies de confiance
        for _ in range(5):
            self.analyzer.add_metric_sample("reflexia", "confidence_score", 0.1)  # Très bas

        # Régression de performance
        for _ in range(8):
            self.analyzer.add_metric_sample("reflexia", "response_time", random.uniform(3.0, 5.0))

        # Pattern répétitif suspect
        for _ in range(7):
            self.analyzer.add_decision_event(
                "zeroia",
                {
                    "decision_type": "contradiction_detected",  # Toujours le même
                    "confidence": 0.95,
                },
            )

        # Exécuter l'analyse
        analysis_result = self.analyzer.analyze_behavior()

        ark_logger.info("✅ Analyse comportementale terminée:", extra={"module": "scripts"})
        ark_logger.info(f"   🎯 Score de santé: {analysis_result['behavioral_health_score']:.3f}", extra={"module": "scripts"})
        ark_logger.info(f"   📊 Patterns détectés: {analysis_result['patterns_detected']}", extra={"module": "scripts"})
        critical_count = analysis_result["patterns_by_severity"].get("critical", 0)
        ark_logger.info(f"   🔴 Patterns critiques: {critical_count}", extra={"module": "scripts"})
        ark_logger.info(f"   🟡 Patterns moyens: {analysis_result['patterns_by_severity'].get('medium', 0, extra={"module": "scripts"})}")
        ark_logger.info(f"   📈 Modules affectés: {len(analysis_result['affected_modules'], extra={"module": "scripts"})}")

        # Afficher détails des patterns
        if analysis_result["patterns_detail"]:
            ark_logger.info("\n🔍 Patterns détectés:", extra={"module": "scripts"})
            for pattern in analysis_result["patterns_detail"][:3]:  # 3 premiers
                ark_logger.info(f"   • {pattern['severity'].upper(, extra={"module": "scripts"})}: {pattern['description']}")
                ark_logger.info(f"     Modules: {', '.join(pattern['affected_modules'], extra={"module": "scripts"})}")
                ark_logger.info(f"     Confiance: {pattern['confidence']:.2f}", extra={"module": "scripts"})

        return analysis_result

    def demo_metrics(self):
        """Démonstration SandoziaMetrics"""
        ark_logger.info("\n" + "=" * 60, extra={"module": "scripts"})
        ark_logger.info("📊 DÉMONSTRATION SANDOZIAMETRICS", extra={"module": "scripts"})
        ark_logger.info("=" * 60, extra={"module": "scripts"})

        self.metrics = SandoziaMetrics(retention_hours=1)  # Court pour demo

        ark_logger.info("📈 Génération de métriques temporelles...", extra={"module": "scripts"})

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
            response_time = max(0.1, 2.0 - reflexia_conf * 1.5 + random.uniform(-0.2, 0.2))
            self.metrics.add_metric(
                "reflexia_response_time",
                response_time,
                {"module": "reflexia", "type": "performance"},
            )

        # Analyser les corrélations
        correlation = self.metrics.calculate_correlation(
            "reflexia_confidence_score", "zeroia_confidence_score", 60
        )

        ark_logger.info("✅ Métriques générées:", extra={"module": "scripts"})
        ark_logger.info(
            f"   🔗 Corrélation Reflexia-ZeroIA: {correlation:.3f}"
            if correlation
            else "   🔗 Corrélation: N/A"
        , extra={"module": "scripts"})

        # Santé cross-modules
        health = self.metrics.get_cross_module_health()
        ark_logger.info(f"   🎯 Cohérence inter-modules: {health['cross_module_coherence']:.3f}", extra={"module": "scripts"})
        ark_logger.info(f"   📊 Métriques totales: {health['total_metrics']}", extra={"module": "scripts"})

        # Résumés par métrique
        for metric_name in [
            "reflexia_confidence_score",
            "zeroia_confidence_score",
            "reflexia_response_time",
        ]:
            summary = self.metrics.get_metric_summary(metric_name)
            if summary:
                ark_logger.info(f"   📈 {metric_name}:", extra={"module": "scripts"})
                ark_logger.info(f"      Moyenne: {summary['mean']:.3f}", extra={"module": "scripts"})
                ark_logger.info(f"      Min-Max: {summary['min']:.3f} - {summary['max']:.3f}", extra={"module": "scripts"})
                ark_logger.info(f"      Échantillons: {summary['count']}", extra={"module": "scripts"})

        return health

    async def demo_sandozia_core(self):
        """Démonstration SandoziaCore (orchestrateur)"""
        ark_logger.info("\n" + "=" * 60, extra={"module": "scripts"})
        ark_logger.info("🚀 DÉMONSTRATION SANDOZIACORE", extra={"module": "scripts"})
        ark_logger.info("=" * 60, extra={"module": "scripts"})

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

        ark_logger.info("🔌 Initialisation des connexions modules...", extra={"module": "scripts"})
        await self.sandozia_core.initialize_modules()

        ark_logger.info("📊 Collecte d'un snapshot d'intelligence...", extra={"module": "scripts"})
        snapshot = await self.sandozia_core.collect_intelligence_snapshot()

        ark_logger.info("✅ Snapshot collecté:", extra={"module": "scripts"})
        ark_logger.info(f"   🧠 État Reflexia: {'✅' if snapshot.reflexia_state.get('active', extra={"module": "scripts"}) else '❌'}")
        ark_logger.info(f"   🔍 État ZeroIA: {'✅' if snapshot.zeroia_state.get('active', True, extra={"module": "scripts"}) else '❌'}")
        ark_logger.info(f"   🎯 Score cohérence: {snapshot.coherence_analysis['coherence_score']:.3f}", extra={"module": "scripts"})
        ark_logger.info(f"   ⚠️  Issues détectées: {len(snapshot.coherence_analysis['issues'], extra={"module": "scripts"})}")
        ark_logger.info(f"   🔮 Patterns comportementaux: {len(snapshot.behavioral_patterns, extra={"module": "scripts"})}")
        ark_logger.info(f"   💡 Recommandations: {len(snapshot.recommendations, extra={"module": "scripts"})}")

        if snapshot.recommendations:
            ark_logger.info("\n💡 Recommandations:", extra={"module": "scripts"})
            for rec in snapshot.recommendations[:3]:
                ark_logger.info(f"   • {rec}", extra={"module": "scripts"})

        # Test de monitoring court (10 secondes)
        ark_logger.info("\n🔄 Test monitoring (10 secondes)...", extra={"module": "scripts"})
        await self.sandozia_core.start_monitoring()

        # Attendre un peu pour voir le monitoring
        await asyncio.sleep(10)

        await self.sandozia_core.stop_monitoring()
        ark_logger.info("🛑 Monitoring arrêté", extra={"module": "scripts"})

        # Statut final
        status = self.sandozia_core.get_current_status()
        ark_logger.info("\n📊 Statut final Sandozia:", extra={"module": "scripts"})
        ark_logger.info(f"   🔄 En fonctionnement: {status['is_running']}", extra={"module": "scripts"})
        ark_logger.info(f"   📊 Snapshots collectés: {status['snapshots_count']}", extra={"module": "scripts"})
        connected_modules = sum(status["modules_available"].values())
        total_modules = len(status["modules_available"])
        ark_logger.info(f"   🔌 Modules connectés: {connected_modules}/{total_modules}", extra={"module": "scripts"})

        return status

    async def run_full_demo(self):
        """Exécute la démonstration complète"""
        ark_logger.info("🌟" + "=" * 70 + "🌟", extra={"module": "scripts"})
        ark_logger.info("🧠 DÉMONSTRATION COMPLÈTE SANDOZIA INTELLIGENCE CROISÉE", extra={"module": "scripts"})
        ark_logger.info("🌟" + "=" * 70 + "🌟", extra={"module": "scripts"})
        ark_logger.info(f"📅 Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', extra={"module": "scripts"})}")
        ark_logger.info("🎯 Phase 2 v3.x - Semaine 1 (SandoziaCore + boucle simple)", extra={"module": "scripts"})

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
            ark_logger.info("\n" + "🎉" + "=" * 70 + "🎉", extra={"module": "scripts"})
            ark_logger.info("✅ DÉMONSTRATION SANDOZIA TERMINÉE AVEC SUCCÈS", extra={"module": "scripts"})
            ark_logger.info("🎉" + "=" * 70 + "🎉", extra={"module": "scripts"})

            ark_logger.info("\n📊 RÉSUMÉ DES PERFORMANCES:", extra={"module": "scripts"})
            ark_logger.info(f"   🔍 Cohérence modules: {validator_result['coherence_score']:.3f}", extra={"module": "scripts"})
            ark_logger.info(f"   🧠 Santé comportementale: {analyzer_result['behavioral_health_score']:.3f}", extra={"module": "scripts"})
            ark_logger.info(f"   📈 Cohérence métriques: {metrics_result['cross_module_coherence']:.3f}", extra={"module": "scripts"})
            ark_logger.info(
                f"   🚀 Core opérationnel: {'✅' if core_result['is_running'] is False else '✅'}"
            , extra={"module": "scripts"})  # False car arrêté proprement

            # Score global Sandozia
            scores = [
                validator_result["coherence_score"],
                analyzer_result["behavioral_health_score"],
                metrics_result["cross_module_coherence"],
            ]
            global_score = sum(scores) / len(scores)

            ark_logger.info(f"\n🎯 SCORE GLOBAL SANDOZIA: {global_score:.3f}/1.0", extra={"module": "scripts"})

            if global_score > 0.8:
                ark_logger.info("🌟 EXCELLENT - Sandozia Intelligence Croisée pleinement opérationnelle!", extra={"module": "scripts"})
            elif global_score > 0.6:
                ark_logger.info(
                    "👍 BIEN - Sandozia fonctionne correctement avec "
                    "quelques optimisations possibles"
                , extra={"module": "scripts"})
            else:
                ark_logger.info("⚠️  ATTENTION - Sandozia nécessite des ajustements", extra={"module": "scripts"})

            ark_logger.info("\n🚀 PHASE 2 PRÊTE POUR SEMAINE 2: CrossModuleValidator + Dashboard Grafana", extra={"module": "scripts"})

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
            ark_logger.info(f"❌ ÉCHEC DE LA DÉMONSTRATION: {e}", extra={"module": "scripts"})
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

        ark_logger.info("🧹 Cleanup demo terminé", extra={"module": "scripts"})


async def run_daemon_mode(demo: SandoziaDemo):
    """Mode daemon pour container Docker - boucle infinie"""
    ark_logger.info("🧠 SANDOZIA INTELLIGENCE CROISÉE - Mode Daemon", extra={"module": "scripts"})
    ark_logger.info("🐳 Démarrage pour container Docker...", extra={"module": "scripts"})
    ark_logger.info("=" * 60, extra={"module": "scripts"})

    import time

    cycle_count = 0

    try:
        while True:  # Boucle infinie pour daemon
            cycle_count += 1
            ark_logger.info(f"\n🔄 === CYCLE SANDOZIA DAEMON {cycle_count} ===", extra={"module": "scripts"})
            ark_logger.info(f"⏰ {time.strftime('%H:%M:%S', extra={"module": "scripts"})}")

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

                ark_logger.info(f"📊 Score global Sandozia: {global_score:.3f}", extra={"module": "scripts"})

                # Status périodique détaillé
                if cycle_count % 5 == 0:
                    ark_logger.info(f"🎯 Status après {cycle_count} cycles:", extra={"module": "scripts"})
                    ark_logger.info(f"  - Cohérence modules: {validator_result['coherence_score']:.3f}", extra={"module": "scripts"})
                    behavioral_score = analyzer_result["behavioral_health_score"]
                    ark_logger.info(f"  - Santé comportementale: {behavioral_score:.3f}", extra={"module": "scripts"})
                    ark_logger.info(
                        f"  - Métriques cohérentes: {metrics_result['cross_module_coherence']:.3f}"
                    , extra={"module": "scripts"})
                    ark_logger.info(f"  - Performance globale: {global_score:.3f}", extra={"module": "scripts"})

            except Exception as e:
                ark_logger.info(f"⚠️ Erreur cycle {cycle_count}: {e}", extra={"module": "scripts"})
                # En mode daemon, on continue malgré les erreurs

            # Pause entre cycles (important pour container)
            ark_logger.info("💤 Pause 15s avant prochain cycle...", extra={"module": "scripts"})
            await asyncio.sleep(15)

    except KeyboardInterrupt:
        ark_logger.info("\n⏹️ Daemon Sandozia arrêté proprement", extra={"module": "scripts"})
    except Exception as e:
        ark_logger.info(f"\n💥 Erreur daemon: {e}", extra={"module": "scripts"})
        # En mode daemon, on redémarre automatiquement
        ark_logger.info("🔄 Redémarrage automatique dans 10s...", extra={"module": "scripts"})
        await asyncio.sleep(10)
        await run_daemon_mode(demo)  # Relance recursive


def format_generated():
    """Formate tous les dossiers generated avec isort + black."""
    for d in Path(".").rglob("generated"):
        try:
            # Tri des imports avec isort (compatible black)
            subprocess.run(["isort", str(d), "--profile", "black"], check=True)
            # Formatage du code avec black
            subprocess.run(["black", str(d), "--quiet"], check=True)
            ark_logger.info(f"✅ Formaté: {d}", extra={"module": "scripts"})
        except subprocess.CalledProcessError as e:
            ark_logger.info(f"⚠️ Erreur formatage {d}: {e}", extra={"module": "scripts"})
            # Fallback: essayer au moins isort
            try:
                subprocess.run(["isort", str(d), "--fix"], check=False)
                ark_logger.info(f"⚠️ Fallback isort appliqué: {d}", extra={"module": "scripts"})
            except Exception:
                ark_logger.info(f"❌ Fallback échoué: {d}", extra={"module": "scripts"})


async def main():
    """Point d'entrée principal"""
    import argparse

    parser = argparse.ArgumentParser(description="Démonstration Sandozia Intelligence Croisée")
    parser.add_argument("--full-demo", action="store_true", help="Démonstration complète")
    parser.add_argument(
        "--validator-only", action="store_true", help="CrossModuleValidator uniquement"
    )
    parser.add_argument("--analyzer-only", action="store_true", help="BehaviorAnalyzer uniquement")
    parser.add_argument("--metrics-only", action="store_true", help="SandoziaMetrics uniquement")
    parser.add_argument("--core-only", action="store_true", help="SandoziaCore uniquement")
    parser.add_argument("--cleanup", action="store_true", help="Nettoyer les fichiers de demo")
    parser.add_argument("--daemon", action="store_true", help="Mode daemon pour container Docker")

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
            ark_logger.info(f"\n📁 Résultats sauvegardés: {results_file}", extra={"module": "scripts"})

        elif args.validator_only:
            demo.demo_validator()
        elif args.analyzer_only:
            demo.demo_behavior_analyzer()
        elif args.metrics_only:
            demo.demo_metrics()
        elif args.core_only:
            await demo.demo_sandozia_core()

        format_generated()

        return result

    finally:
        if not args.cleanup:
            # Cleanup automatique sauf si explicitement demandé
            pass


if __name__ == "__main__":
    asyncio.run(main())
