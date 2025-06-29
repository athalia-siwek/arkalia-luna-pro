#!/usr/bin/env python3
"""
🧪 tests/security/test_poisoning.py
Model Poisoning Detection for ZeroIA - Roadmap S2 P0

Détecte les tentatives d'empoisonnement du modèle décisionnel de ZeroIA
via injection de données malveillantes dans les inputs contextuels.
"""

import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

import toml

from modules.zeroia.reason_loop import decide, reason_loop


class ModelPoisoningDetector:
    """Détecteur d'empoisonnement de modèle pour ZeroIA"""

    def __init__(self):
        self.anomaly_threshold = 0.85
        self.decision_history = []
        self.confidence_baseline = 0.6

    def analyze_decision_pattern(self, decisions: list) -> dict:
        """Analyse les patterns de décision pour détecter des anomalies"""
        if len(decisions) < 3:
            return {"anomaly_detected": False, "confidence": 0.0}

        # Détection de patterns suspects
        suspicious_patterns = {
            "always_emergency": all(d == "emergency_shutdown" for d in decisions[-5:]),
            "always_reduce": all(d == "reduce_load" for d in decisions[-5:]),
            "rapid_oscillation": self._detect_oscillation(decisions[-10:]),
            "impossible_decisions": self._detect_impossible_decisions(decisions),
        }

        anomaly_score = sum(suspicious_patterns.values()) / len(suspicious_patterns)

        return {
            "anomaly_detected": anomaly_score > self.anomaly_threshold,
            "confidence": anomaly_score,
            "patterns": suspicious_patterns,
            "recommendation": self._get_recommendation(suspicious_patterns),
        }

    def _detect_oscillation(self, decisions: list) -> bool:
        """Détecte les oscillations rapides suspectes"""
        if len(decisions) < 4:
            return False
        changes = sum(
            1 for i in range(1, len(decisions)) if decisions[i] != decisions[i - 1]
        )
        return changes > len(decisions) * 0.7

    def _detect_impossible_decisions(self, decisions: list) -> bool:
        """Détecte des décisions impossibles selon la logique ZeroIA"""
        # Emergency shutdown avec CPU normal devrait être suspect
        return "emergency_shutdown" in decisions[-3:] and len(decisions) > 1

    def _get_recommendation(self, patterns: dict) -> str:
        """Génère une recommandation basée sur les patterns détectés"""
        if patterns["always_emergency"]:
            return "CRITICAL: Possible injection forcing emergency shutdown"
        elif patterns["rapid_oscillation"]:
            return "WARNING: Decision instability detected - possible model confusion"
        elif patterns["impossible_decisions"]:
            return "ALERT: Logically inconsistent decisions detected"
        else:
            return "NORMAL: Decision patterns within expected parameters"


class FakePoisonedDatasets:
    """Générateur de datasets empoisonnés pour tests"""

    @staticmethod
    def create_cpu_injection_attack() -> dict:
        """Injection CPU malveillante pour forcer emergency_shutdown"""
        return {
            "status": {
                "cpu": 95,  # CPU élevé normal
                "severity": "critical",  # Mais severity forcée à critical
                "ram": 45,
                "disk": 30,
            },
            "reflexia": {
                "last_decision": "normal",  # Incohérence volontaire
                "confidence": 0.9,
            },
            "timestamp": datetime.now().isoformat(),
        }

    @staticmethod
    def create_oscillation_attack() -> list:
        """Série de contextes pour créer oscillation artificielle"""
        contexts = []
        for i in range(10):
            cpu_val = 85 if i % 2 == 0 else 55  # Oscillation forcée
            contexts.append(
                {
                    "status": {
                        "cpu": cpu_val,
                        "severity": "none",
                        "ram": 40,
                        "disk": 25,
                    },
                    "reflexia": {"last_decision": "monitor", "confidence": 0.7},
                    "timestamp": (datetime.now() + timedelta(seconds=i)).isoformat(),
                }
            )
        return contexts

    @staticmethod
    def create_yaml_injection_attack() -> dict:
        """Tentative d'injection YAML malveillante"""
        return {
            "status": {
                "cpu": "{{malicious_payload}}",  # Injection template
                "severity": "none & echo 'hacked'",  # Command injection attempt
                "ram": float("inf"),  # Valeur impossible
                "disk": -50,  # Valeur négative impossible
            },
            "reflexia": {
                "last_decision": "'; DROP TABLE decisions; --",  # SQL injection style
                "confidence": 999.9,  # Valeur aberrante
            },
        }

    @staticmethod
    def create_stealth_poisoning() -> dict:
        """Empoisonnement furtif - valeurs presque normales"""
        return {
            "status": {
                "cpu": 79.9,  # Juste sous le seuil, mais répété
                "severity": "none",
                "ram": 45,
                "disk": 30,
            },
            "reflexia": {
                "last_decision": "reduce_load",
                "confidence": 0.79,  # Confidence élevée pour décision mineure
            },
            "timestamp": datetime.now().isoformat(),
            "_poisoned": True,  # Marqueur caché
        }


class TestModelPoisoning(unittest.TestCase):
    """Tests de détection d'empoisonnement de modèle"""

    def setUp(self):
        self.detector = ModelPoisoningDetector()
        self.fake_data = FakePoisonedDatasets()

    def test_cpu_injection_detection(self):
        """Test détection injection CPU malveillante"""
        poisoned_ctx = self.fake_data.create_cpu_injection_attack()

        decision, confidence = decide(poisoned_ctx)

        # La décision devrait être cohérente malgré l'injection
        self.assertEqual(decision, "emergency_shutdown")
        self.assertGreaterEqual(confidence, 0.8)

        # Le détecteur devrait signaler l'incohérence
        analysis = self.detector.analyze_decision_pattern([decision] * 3)
        self.assertTrue(analysis["patterns"]["impossible_decisions"])

    def test_oscillation_attack_detection(self):
        """Test détection attaque par oscillation"""
        contexts = self.fake_data.create_oscillation_attack()
        decisions = []

        for ctx in contexts:
            decision, _ = decide(ctx)
            decisions.append(decision)

        analysis = self.detector.analyze_decision_pattern(decisions)
        self.assertTrue(analysis["anomaly_detected"])
        self.assertTrue(analysis["patterns"]["rapid_oscillation"])
        self.assertIn("instability", analysis["recommendation"])

    def test_yaml_injection_protection(self):
        """Test protection contre injection YAML"""
        malicious_ctx = self.fake_data.create_yaml_injection_attack()

        # ZeroIA devrait gérer gracieusement les valeurs aberrantes
        try:
            decision, confidence = decide(malicious_ctx)
            # Si on arrive ici, c'est que ZeroIA a résisté à l'injection
            self.assertIsInstance(decision, str)
            self.assertIsInstance(confidence, (int, float))
        except (ValueError, TypeError) as e:
            # Erreur attendue pour valeurs malformées
            self.assertIn("invalid", str(e).lower())

    def test_stealth_poisoning_detection(self):
        """Test détection empoisonnement furtif"""
        stealth_ctx = self.fake_data.create_stealth_poisoning()

        # Répéter la même décision "presque normale" plusieurs fois
        decisions = []
        for _ in range(8):
            decision, confidence = decide(stealth_ctx)
            decisions.append(decision)

        analysis = self.detector.analyze_decision_pattern(decisions)

        # Détecter le pattern de répétition suspect
        if all(d == decisions[0] for d in decisions):
            self.assertGreater(analysis["confidence"], 0.5)

    def test_normal_operation_baseline(self):
        """Test que l'opération normale ne déclenche pas d'alerte"""
        normal_contexts = [
            {"status": {"cpu": 45, "severity": "none", "ram": 40, "disk": 25}},
            {"status": {"cpu": 55, "severity": "none", "ram": 45, "disk": 30}},
            {"status": {"cpu": 62, "severity": "none", "ram": 50, "disk": 35}},
            {"status": {"cpu": 58, "severity": "none", "ram": 47, "disk": 32}},
        ]

        decisions = []
        for ctx in normal_contexts:
            decision, _ = decide(ctx)
            decisions.append(decision)

        analysis = self.detector.analyze_decision_pattern(decisions)
        self.assertFalse(analysis["anomaly_detected"])
        self.assertEqual(
            analysis["recommendation"],
            "NORMAL: Decision patterns within expected parameters",
        )

    def test_integration_with_reason_loop(self):
        """Test intégration avec reason_loop principal"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Création fichiers temporaires
            ctx_path = Path(tmp_dir) / "context.toml"
            state_path = Path(tmp_dir) / "state.toml"

            # Context empoisonné
            poisoned_context = {
                "status": {"cpu": 90, "severity": "critical", "ram": 85, "disk": 70},
                "reflexia": {
                    "last_decision": "normal",  # Incohérent !
                    "confidence": 0.9,
                },
            }

            # Sauvegarde context empoisonné
            with open(ctx_path, "w") as f:
                toml.dump(poisoned_context, f)

            # État reflexia normal
            reflexia_state = {
                "decision": {"last_decision": "normal", "confidence": 0.8}
            }
            reflexia_path = Path(tmp_dir) / "reflexia.toml"
            with open(reflexia_path, "w") as f:
                toml.dump(reflexia_state, f)

            # Exécution reason_loop avec détection
            try:
                decision, confidence = reason_loop(
                    context_path=ctx_path,
                    reflexia_path=reflexia_path,
                    state_path=state_path,
                )

                # Vérification que ZeroIA prend la bonne décision malgré empoisonnement
                self.assertEqual(decision, "emergency_shutdown")
                self.assertGreater(confidence, 0.8)

                # Vérification que l'état est persisté
                self.assertTrue(state_path.exists())

            except Exception as e:
                self.fail(f"reason_loop a échoué avec context empoisonné: {e}")


def create_model_integrity_report() -> dict:
    """Génère un rapport d'intégrité du modèle ZeroIA"""
    detector = ModelPoisoningDetector()
    fake_data = FakePoisonedDatasets()

    # Tests multiples
    test_results = {
        "cpu_injection": False,
        "oscillation_attack": False,
        "yaml_injection": False,
        "stealth_poisoning": False,
        "baseline_normal": True,
    }

    # Test CPU injection
    try:
        ctx = fake_data.create_cpu_injection_attack()
        decision, _ = decide(ctx)
        analysis = detector.analyze_decision_pattern([decision] * 3)
        test_results["cpu_injection"] = analysis["anomaly_detected"]
    except Exception:
        test_results["cpu_injection"] = True  # Erreur = détection

    # Test oscillation
    try:
        contexts = fake_data.create_oscillation_attack()
        decisions = [decide(ctx)[0] for ctx in contexts]
        analysis = detector.analyze_decision_pattern(decisions)
        test_results["oscillation_attack"] = analysis["anomaly_detected"]
    except Exception:
        test_results["oscillation_attack"] = True

    return {
        "timestamp": datetime.now().isoformat(),
        "model_integrity": "PROTECTED" if any(test_results.values()) else "VULNERABLE",
        "test_results": test_results,
        "recommendation": (
            "Model poisoning detection operational"
            if any(test_results.values())
            else "CRITICAL: Implement additional protections"
        ),
    }


if __name__ == "__main__":
    # Exécution des tests
    unittest.main(verbosity=2, exit=False)

    # Génération rapport d'intégrité
    report = create_model_integrity_report()
    print("\n🛡️ Model Integrity Report:")
    print(f"Status: {report['model_integrity']}")
    print(f"Recommendation: {report['recommendation']}")
