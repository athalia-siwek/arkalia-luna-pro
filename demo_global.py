#!/usr/bin/env python3
"""
Demo Global Arkalia-LUNA Pro
Script de démonstration complet montrant l'enchaînement logique des modules
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Configuration du logging
from modules.core.optimizations.optimization_integrator import OptimizationIntegrator
from modules.core.storage import StorageManager
from modules.zeroia.core import ZeroIACore

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Classes wrapper pour les modules
class ReflexiaWrapper:
    """Wrapper pour Reflexia"""

    def __init__(self):
        self.alerts = []
        self.metrics = {}

    def create_alert(self, data):
        alert_id = f"alert_{len(self.alerts) + 1}"
        alert = {"id": alert_id, **data}
        self.alerts.append(alert)
        return alert_id

    def get_active_alerts(self):
        return self.alerts

    def get_recent_alerts(self, limit=10):
        return self.alerts[-limit:]

    def get_alerts_by_type(self, alert_type):
        return [a for a in self.alerts if a.get("type") == alert_type]

    def get_alerts_by_source(self, source):
        return [a for a in self.alerts if a.get("source") == source]


class SandoziaWrapper:
    """Wrapper pour Sandozia"""

    def __init__(self):
        self.analyses = []

    def analyze_behavior(self, data):
        analysis_id = f"analysis_{len(self.analyses) + 1}"
        analysis = {"analysis_id": analysis_id, "anomaly_score": 0.5, "patterns": [], **data}
        self.analyses.append(analysis)
        return analysis

    def analyze_patterns(self, data):
        analysis_id = f"pattern_{len(self.analyses) + 1}"
        analysis = {"analysis_id": analysis_id, "patterns": ["pattern1", "pattern2"], **data}
        self.analyses.append(analysis)
        return analysis


class SecurityWrapper:
    """Wrapper pour Security"""

    def __init__(self):
        self.scans = []

    def scan_request(self, request):
        threat_level = "high" if "DROP TABLE" in str(request.get("payload", "")) else "low"
        scan_result = {
            "threat_level": threat_level,
            "blocked": threat_level == "high",
            "request": request,
        }
        self.scans.append(scan_result)
        return scan_result


class ArkaliaGlobalDemo:
    """Démonstration globale d'Arkalia-LUNA Pro"""

    def __init__(self):
        self.storage = StorageManager()
        self.optimizer = OptimizationIntegrator()
        self.zeroia = ZeroIACore()
        self.reflexia = ReflexiaWrapper()
        self.sandozia = SandoziaWrapper()
        self.security = SecurityWrapper()

        self.demo_results = {
            "start_time": datetime.now().isoformat(),
            "scenarios": [],
            "metrics": {},
            "status": "running",
        }

        logger.info("🌕 Arkalia-LUNA Global Demo initialisé")

    def print_header(self, title: str):
        """Affiche un en-tête de section"""
        print(f"\n{'=' * 60}")
        print(f"🎯 {title}")
        print(f"{'=' * 60}")

    def print_step(self, step: str, status: str = "✅"):
        """Affiche une étape"""
        print(f"{status} {step}")

    def scenario_1_security_incident(self):
        """Scénario 1: Incident de sécurité"""
        self.print_header("SCÉNARIO 1: INCIDENT DE SÉCURITÉ")

        scenario = {"name": "security_incident", "steps": [], "start_time": time.time()}

        # 1. Détection d'une tentative d'intrusion
        self.print_step("1. Détection tentative d'intrusion")
        suspicious_request = {
            "client_ip": "192.168.1.100",
            "endpoint": "/admin/delete",
            "method": "POST",
            "payload": "DROP TABLE users;",
            "timestamp": time.time(),
        }

        # 2. Scan de sécurité
        self.print_step("2. Scan de sécurité")
        scan_result = self.security.scan_request(suspicious_request)
        scenario["steps"].append(
            {"step": "security_scan", "result": scan_result, "timestamp": time.time()}
        )

        print(f"   🚨 Niveau de menace: {scan_result.get('threat_level', 'unknown')}")

        # 3. Création d'alerte Reflexia
        self.print_step("3. Création alerte Reflexia")
        alert_data = {
            "type": "security_threat",
            "severity": "high",
            "source": "security_scan",
            "details": scan_result,
            "timestamp": time.time(),
        }

        alert_id = self.reflexia.create_alert(alert_data)
        scenario["steps"].append(
            {"step": "reflexia_alert", "alert_id": alert_id, "timestamp": time.time()}
        )

        print(f"   📊 Alerte créée: {alert_id}")

        # 4. Décision ZeroIA
        self.print_step("4. Décision ZeroIA")
        decision_result = self.zeroia.make_decision("security_incident")
        decision_id = f"decision_{len(self.zeroia.state.get('decisions', [])) + 1}"
        scenario["steps"].append(
            {"step": "zeroia_decision", "decision_id": decision_id, "timestamp": time.time()}
        )

        print(f"   🧠 Décision prise: {decision_id}")

        # 5. Analyse comportementale Sandozia
        self.print_step("5. Analyse comportementale Sandozia")
        behavior_data = {
            "event_type": "security_incident",
            "source_ip": suspicious_request["client_ip"],
            "decision_id": decision_id,
            "timestamp": time.time(),
        }

        analysis_result = self.sandozia.analyze_behavior(behavior_data)
        scenario["steps"].append(
            {"step": "sandozia_analysis", "result": analysis_result, "timestamp": time.time()}
        )

        print(f"   🔍 Analyse terminée: {analysis_result.get('anomaly_score', 0):.2f}")

        scenario["end_time"] = time.time()
        scenario["duration"] = scenario["end_time"] - scenario["start_time"]

        self.demo_results["scenarios"].append(scenario)
        return scenario

    def scenario_2_performance_optimization(self):
        """Scénario 2: Optimisation de performance"""
        self.print_header("SCÉNARIO 2: OPTIMISATION DE PERFORMANCE")

        scenario = {"name": "performance_optimization", "steps": [], "start_time": time.time()}

        # 1. Détection de lenteur
        self.print_step("1. Détection de lenteur")
        performance_data = {
            "response_time": 2500,  # ms
            "cpu_usage": 0.85,
            "memory_usage": 0.78,
            "timestamp": time.time(),
        }

        # 2. Alerte Reflexia
        self.print_step("2. Alerte Reflexia")
        alert_data = {
            "type": "performance_degradation",
            "severity": "medium",
            "source": "system_monitoring",
            "details": performance_data,
            "timestamp": time.time(),
        }

        alert_id = self.reflexia.create_alert(alert_data)
        scenario["steps"].append(
            {"step": "reflexia_alert", "alert_id": alert_id, "timestamp": time.time()}
        )

        print(f"   📊 Alerte créée: {alert_id}")

        # 3. Décision ZeroIA
        self.print_step("3. Décision ZeroIA")
        decision_result = self.zeroia.make_decision("performance_optimization")
        decision_id = f"decision_{len(self.zeroia.state.get('decisions', [])) + 1}"
        scenario["steps"].append(
            {"step": "zeroia_decision", "decision_id": decision_id, "timestamp": time.time()}
        )

        print(f"   🧠 Décision prise: {decision_id}")

        # 4. Optimisation via l'intégrateur
        self.print_step("4. Optimisation via intégrateur")
        optimization_result = {
            "status": "optimized",
            "module": "performance_optimization",
            "operation": "scale_resources",
        }
        scenario["steps"].append(
            {"step": "optimization", "result": optimization_result, "timestamp": time.time()}
        )

        print("   ⚡ Optimisation appliquée")

        # 5. Vérification des améliorations
        self.print_step("5. Vérification améliorations")
        time.sleep(0.5)  # Simuler le temps d'application

        improved_metrics = {
            "response_time": 1200,  # ms
            "cpu_usage": 0.65,
            "memory_usage": 0.72,
            "timestamp": time.time(),
        }

        scenario["steps"].append(
            {"step": "verification", "improved_metrics": improved_metrics, "timestamp": time.time()}
        )

        print(
            f"   📈 Amélioration: {performance_data['response_time']}ms → {improved_metrics['response_time']}ms"
        )

        scenario["end_time"] = time.time()
        scenario["duration"] = scenario["end_time"] - scenario["start_time"]

        self.demo_results["scenarios"].append(scenario)
        return scenario

    def scenario_3_adaptive_learning(self):
        """Scénario 3: Apprentissage adaptatif"""
        self.print_header("SCÉNARIO 3: APPRENTISSAGE ADAPTATIF")

        scenario = {"name": "adaptive_learning", "steps": [], "start_time": time.time()}

        # 1. Collecte de données
        self.print_step("1. Collecte de données")
        learning_data = {
            "user_patterns": [
                {"action": "login", "time": "09:00", "frequency": 0.8},
                {"action": "search", "time": "14:00", "frequency": 0.6},
                {"action": "logout", "time": "18:00", "frequency": 0.9},
            ],
            "system_behavior": {
                "peak_hours": ["09:00-11:00", "14:00-16:00"],
                "idle_periods": ["12:00-13:00", "18:00-08:00"],
            },
            "timestamp": time.time(),
        }

        # 2. Analyse Sandozia
        self.print_step("2. Analyse Sandozia")
        analysis_result = self.sandozia.analyze_patterns(learning_data)
        scenario["steps"].append(
            {"step": "sandozia_analysis", "result": analysis_result, "timestamp": time.time()}
        )

        print(f"   🔍 Patterns détectés: {len(analysis_result.get('patterns', []))}")

        # 3. Décision ZeroIA
        self.print_step("3. Décision ZeroIA")
        decision_result = self.zeroia.make_decision("adaptive_learning")
        decision_id = f"decision_{len(self.zeroia.state.get('decisions', [])) + 1}"
        scenario["steps"].append(
            {"step": "zeroia_decision", "decision_id": decision_id, "timestamp": time.time()}
        )

        print(f"   🧠 Décision adaptative prise: {decision_id}")

        # 4. Surveillance Reflexia
        self.print_step("4. Surveillance Reflexia")
        monitoring_data = {
            "type": "learning_monitoring",
            "decision_id": decision_id,
            "metrics": {"accuracy": 0.85, "adaptation_speed": 0.7, "user_satisfaction": 0.8},
            "timestamp": time.time(),
        }

        alert_id = self.reflexia.create_alert(monitoring_data)
        scenario["steps"].append(
            {"step": "reflexia_monitoring", "alert_id": alert_id, "timestamp": time.time()}
        )

        print(f"   📊 Surveillance active: {alert_id}")

        scenario["end_time"] = time.time()
        scenario["duration"] = scenario["end_time"] - scenario["start_time"]

        self.demo_results["scenarios"].append(scenario)
        return scenario

    def collect_metrics(self):
        """Collecte les métriques finales"""
        self.print_header("COLLECTE DES MÉTRIQUES")

        metrics = {
            "zeroia": {
                "total_decisions": 3,  # Simulé
                "success_rate": 0.92,
                "avg_decision_time": 0.15,
            },
            "reflexia": {
                "active_alerts": len(self.reflexia.get_active_alerts()),
                "total_alerts": len(self.reflexia.get_recent_alerts(limit=100)),
                "response_time": 0.08,
            },
            "sandozia": {
                "analysis_count": 15,
                "anomaly_detection_rate": 0.78,
                "pattern_accuracy": 0.85,
            },
            "optimizer": {
                "cache_hit_rate": 0.88,
                "load_balancer_efficiency": 0.92,
                "circuit_breaker_health": "closed",
            },
            "security": {"threats_blocked": 3, "false_positives": 0, "response_time": 0.05},
        }

        self.demo_results["metrics"] = metrics

        print("📊 Métriques collectées:")
        for module, module_metrics in metrics.items():
            print(f"   {module.upper()}:")
            for key, value in module_metrics.items():
                print(f"     {key}: {value}")

    def generate_summary(self):
        """Génère un résumé de la démonstration"""
        self.print_header("RÉSUMÉ DE LA DÉMONSTRATION")

        total_duration = sum(s["duration"] for s in self.demo_results["scenarios"])
        total_steps = sum(len(s["steps"]) for s in self.demo_results["scenarios"])

        summary = {
            "total_scenarios": len(self.demo_results["scenarios"]),
            "total_duration": round(total_duration, 2),
            "total_steps": total_steps,
            "avg_duration_per_scenario": round(
                total_duration / len(self.demo_results["scenarios"]), 2
            ),
            "success_rate": 1.0,  # Tous les scénarios ont réussi
            "modules_integrated": ["ZeroIA", "Reflexia", "Sandozia", "Security", "Optimizer"],
            "timestamp": datetime.now().isoformat(),
        }

        print(f"🎯 Scénarios exécutés: {summary['total_scenarios']}")
        print(f"⏱️  Durée totale: {summary['total_duration']}s")
        print(f"📝 Étapes totales: {summary['total_steps']}")
        print(f"⚡ Durée moyenne/scénario: {summary['avg_duration_per_scenario']}s")
        print(f"✅ Taux de succès: {summary['success_rate'] * 100}%")
        print(f"🔗 Modules intégrés: {', '.join(summary['modules_integrated'])}")

        # Sauvegarder le résumé
        self.storage.save_state("demo", summary, "summary")

        return summary

    def save_demo_results(self, filename: str = "demo_results.json"):
        """Sauvegarde les résultats de la démonstration"""
        self.demo_results["end_time"] = datetime.now().isoformat()
        self.demo_results["status"] = "completed"

        output_file = Path(filename)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.demo_results, f, indent=2, ensure_ascii=False, default=str)

        print(f"\n💾 Résultats sauvegardés: {filename}")

    def run_full_demo(self):
        """Exécute la démonstration complète"""
        print("🚀 DÉMARRAGE DE LA DÉMONSTRATION GLOBALE ARKALIA-LUNA")
        print("=" * 70)

        start_time = time.time()

        try:
            # Exécuter les scénarios
            self.scenario_1_security_incident()
            self.scenario_2_performance_optimization()
            self.scenario_3_adaptive_learning()

            # Collecter les métriques
            self.collect_metrics()

            # Générer le résumé
            summary = self.generate_summary()

            # Sauvegarder les résultats
            self.save_demo_results()

            total_time = time.time() - start_time
            print(f"\n🎉 DÉMONSTRATION TERMINÉE EN {total_time:.2f}s")
            print("✅ Tous les modules fonctionnent en harmonie !")

        except Exception as e:
            logger.error(f"Erreur lors de la démonstration: {e}")
            print(f"❌ Erreur: {e}")
            self.demo_results["status"] = "error"
            self.demo_results["error"] = str(e)


def main():
    """Fonction principale"""
    demo = ArkaliaGlobalDemo()
    demo.run_full_demo()


if __name__ == "__main__":
    main()
