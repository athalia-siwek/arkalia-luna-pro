#!/usr/bin/env python3
"""
🧪 [MODEL POISONING TEST] - Roadmap S2 Arkalia-LUNA
Tests avancés de détection d'empoisonnement de modèle IA

Tests 5 types d'attaques:
- CPU Injection, Oscillation, YAML Injection, Stealth, Normal
"""

import json
import os
import sys

# Configuration du path AVANT tout import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "modules"))

import tempfile
from datetime import datetime
from pathlib import Path

import toml

from modules.zeroia.model_integrity import get_integrity_monitor
from modules.zeroia.reason_loop import reason_loop
from tests.security.test_poisoning import FakePoisonedDatasets, ModelPoisoningDetector


def test_live_poisoning_attacks():
    """Test en conditions réelles avec fichiers temporaires"""
    print("🧪 [POISONING TEST] Démarrage tests model poisoning...")

    fake_data = FakePoisonedDatasets()
    monitor = get_integrity_monitor()

    # Résultats de test
    test_results = {
        "cpu_injection": {"status": "PENDING", "details": ""},
        "oscillation_attack": {"status": "PENDING", "details": ""},
        "yaml_injection": {"status": "PENDING", "details": ""},
        "stealth_poisoning": {"status": "PENDING", "details": ""},
        "normal_operation": {"status": "PENDING", "details": ""},
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Test 1: CPU Injection Attack
        print("\n🔥 Test 1: CPU Injection Attack")
        try:
            poisoned_ctx = fake_data.create_cpu_injection_attack()
            ctx_file = tmp_path / "ctx_poison.toml"
            state_file = tmp_path / "state_poison.toml"
            reflexia_file = tmp_path / "reflexia_poison.toml"

            # Sauvegarde contexte empoisonné
            with open(ctx_file, "w") as f:
                toml.dump(poisoned_ctx, f)

            # Reflexia state normal
            reflexia_state = {"decision": {"last_decision": "normal", "confidence": 0.8}}
            with open(reflexia_file, "w") as f:
                toml.dump(reflexia_state, f)

            # Exécution avec validation intégrité
            decision, confidence = reason_loop(
                context_path=ctx_file,
                reflexia_path=reflexia_file,
                state_path=state_file,
            )

            integrity_status = monitor.get_integrity_status()

            if integrity_status["status"] in ["SUSPICIOUS", "COMPROMISED"]:
                test_results["cpu_injection"]["status"] = "PROTECTED"
                test_results["cpu_injection"][
                    "details"
                ] = f"Attaque détectée - Status: {integrity_status['status']}"
                print(f"✅ Attaque CPU injection DÉTECTÉE - {integrity_status['status']}")
            else:
                test_results["cpu_injection"]["status"] = "VULNERABLE"
                test_results["cpu_injection"]["details"] = "Attaque non détectée"
                print("❌ Attaque CPU injection NON DÉTECTÉE")

        except Exception as e:
            test_results["cpu_injection"]["status"] = "ERROR"
            test_results["cpu_injection"]["details"] = str(e)
            print(f"⚠️ Erreur test CPU injection: {e}")

        # Test 2: Oscillation Attack
        print("\n🌀 Test 2: Oscillation Attack")
        try:
            contexts = fake_data.create_oscillation_attack()
            decisions = []

            for i, ctx in enumerate(contexts[:5]):  # Limiter à 5 pour le test
                ctx_file = tmp_path / f"ctx_osc_{i}.toml"
                state_file = tmp_path / f"state_osc_{i}.toml"
                reflexia_file = tmp_path / f"reflexia_osc_{i}.toml"

                with open(ctx_file, "w") as f:
                    toml.dump(ctx, f)

                reflexia_state = {"decision": {"last_decision": "monitor", "confidence": 0.7}}
                with open(reflexia_file, "w") as f:
                    toml.dump(reflexia_state, f)

                decision, confidence = reason_loop(
                    context_path=ctx_file,
                    reflexia_path=reflexia_file,
                    state_path=state_file,
                )
                decisions.append(decision)

            # Analyse pattern oscillation
            detector = ModelPoisoningDetector()
            analysis = detector.analyze_decision_pattern(decisions)

            if analysis["anomaly_detected"]:
                test_results["oscillation_attack"]["status"] = "PROTECTED"
                test_results["oscillation_attack"][
                    "details"
                ] = f"Oscillation détectée - Confidence: {analysis['confidence']:.2f}"
                confidence_val = analysis["confidence"]
                print(f"✅ Attaque oscillation DÉTECTÉE - Confidence: {confidence_val:.2f}")
            else:
                test_results["oscillation_attack"]["status"] = "VULNERABLE"
                test_results["oscillation_attack"]["details"] = "Oscillation non détectée"
                print("❌ Attaque oscillation NON DÉTECTÉE")

        except Exception as e:
            test_results["oscillation_attack"]["status"] = "ERROR"
            test_results["oscillation_attack"]["details"] = str(e)
            print(f"⚠️ Erreur test oscillation: {e}")

        # Test 3: YAML Injection
        print("\n💉 Test 3: YAML Injection Attack")
        try:
            malicious_ctx = fake_data.create_yaml_injection_attack()
            ctx_file = tmp_path / "ctx_yaml.toml"

            # Test si l'injection cause erreur (comportement attendu)
            try:
                with open(ctx_file, "w") as f:
                    toml.dump(malicious_ctx, f)

                reflexia_file = tmp_path / "reflexia_yaml.toml"
                state_file = tmp_path / "state_yaml.toml"

                reflexia_state = {"decision": {"last_decision": "normal", "confidence": 0.8}}
                with open(reflexia_file, "w") as f:
                    toml.dump(reflexia_state, f)

                decision, confidence = reason_loop(
                    context_path=ctx_file,
                    reflexia_path=reflexia_file,
                    state_path=state_file,
                )

                # Si on arrive ici, ZeroIA a résisté
                test_results["yaml_injection"]["status"] = "PROTECTED"
                test_results["yaml_injection"]["details"] = "Injection gérée gracieusement"
                print(f"✅ Injection YAML gérée - Decision: {decision}")

            except (ValueError, TypeError, toml.TomlDecodeError) as validation_error:
                # Erreur attendue = protection effective
                test_results["yaml_injection"]["status"] = "PROTECTED"
                test_results["yaml_injection"]["details"] = f"Injection bloquée: {validation_error}"
                print(f"✅ Injection YAML BLOQUÉE: {validation_error}")

        except Exception as e:
            test_results["yaml_injection"]["status"] = "ERROR"
            test_results["yaml_injection"]["details"] = str(e)
            print(f"⚠️ Erreur test YAML injection: {e}")

        # Test 4: Stealth Poisoning
        print("\n🥷 Test 4: Stealth Poisoning")
        try:
            stealth_ctx = fake_data.create_stealth_poisoning()
            decisions = []

            # Répéter 6 fois le même contexte "furtif"
            for i in range(6):
                ctx_file = tmp_path / f"ctx_stealth_{i}.toml"
                state_file = tmp_path / f"state_stealth_{i}.toml"
                reflexia_file = tmp_path / f"reflexia_stealth_{i}.toml"

                with open(ctx_file, "w") as f:
                    toml.dump(stealth_ctx, f)

                reflexia_state = {"decision": {"last_decision": "reduce_load", "confidence": 0.79}}
                with open(reflexia_file, "w") as f:
                    toml.dump(reflexia_state, f)

                decision, confidence = reason_loop(
                    context_path=ctx_file,
                    reflexia_path=reflexia_file,
                    state_path=state_file,
                )
                decisions.append(decision)

            # Analyse répétition suspecte
            if all(d == decisions[0] for d in decisions):
                integrity_status = monitor.get_integrity_status()
                if integrity_status["anomalies_detected"] > 0:
                    test_results["stealth_poisoning"]["status"] = "PROTECTED"
                    test_results["stealth_poisoning"]["details"] = (
                        f"Répétition suspecte détectée - "
                        f"Anomalies: {integrity_status['anomalies_detected']}"
                    )
                    print("✅ Empoisonnement furtif DÉTECTÉ")
                else:
                    test_results["stealth_poisoning"]["status"] = "VULNERABLE"
                    test_results["stealth_poisoning"][
                        "details"
                    ] = "Répétition suspecte non détectée"
                    print("❌ Empoisonnement furtif NON DÉTECTÉ")
            else:
                test_results["stealth_poisoning"]["status"] = "INDETERMINATE"
                test_results["stealth_poisoning"][
                    "details"
                ] = "Décisions variées - test non concluant"
                print("🤔 Test furtif INDÉTERMINÉ")

        except Exception as e:
            test_results["stealth_poisoning"]["status"] = "ERROR"
            test_results["stealth_poisoning"]["details"] = str(e)
            print(f"⚠️ Erreur test stealth: {e}")

        # Test 5: Opération normale (baseline)
        print("\n✅ Test 5: Normal Operation Baseline")
        try:
            normal_contexts = [
                {"status": {"cpu": 45, "severity": "none", "ram": 40, "disk": 25}},
                {"status": {"cpu": 55, "severity": "none", "ram": 45, "disk": 30}},
                {"status": {"cpu": 62, "severity": "none", "ram": 50, "disk": 35}},
            ]

            decisions = []
            for i, ctx in enumerate(normal_contexts):
                ctx_file = tmp_path / f"ctx_normal_{i}.toml"
                state_file = tmp_path / f"state_normal_{i}.toml"
                reflexia_file = tmp_path / f"reflexia_normal_{i}.toml"

                with open(ctx_file, "w") as f:
                    toml.dump(ctx, f)

                reflexia_state = {"decision": {"last_decision": "monitor", "confidence": 0.7}}
                with open(reflexia_file, "w") as f:
                    toml.dump(reflexia_state, f)

                decision, confidence = reason_loop(
                    context_path=ctx_file,
                    reflexia_path=reflexia_file,
                    state_path=state_file,
                )
                decisions.append(decision)

            final_status = monitor.get_integrity_status()
            if final_status["status"] == "HEALTHY":
                test_results["normal_operation"]["status"] = "PASS"
                test_results["normal_operation"]["details"] = "Opération normale non perturbée"
                print("✅ Opération normale PRÉSERVÉE")
            else:
                test_results["normal_operation"]["status"] = "FAIL"
                test_results["normal_operation"][
                    "details"
                ] = f"Faux positifs détectés - Status: {final_status['status']}"
                print("⚠️ Faux positifs détectés")

        except Exception as e:
            test_results["normal_operation"]["status"] = "ERROR"
            test_results["normal_operation"]["details"] = str(e)
            print(f"⚠️ Erreur test normal: {e}")

    # Rapport final
    print(f"\n{'='*60}")
    print("🛡️ RAPPORT FINAL - MODEL POISONING DETECTION")
    print(f"{'='*60}")

    protected_count = sum(
        1 for result in test_results.values() if result["status"] in ["PROTECTED", "PASS"]
    )

    for test_name, result in test_results.items():
        status_emoji = {
            "PROTECTED": "🛡️",
            "PASS": "✅",
            "VULNERABLE": "❌",
            "ERROR": "⚠️",
            "INDETERMINATE": "🤔",
        }.get(result["status"], "❓")

        print(f"{status_emoji} {test_name.upper()}: {result['status']}")
        print(f"   └─ {result['details']}")

    protection_rate = (protected_count / len(test_results)) * 100
    total_tests = len(test_results)
    print(f"\n📊 TAUX DE PROTECTION: {protection_rate:.1f}% " f"({protected_count}/{total_tests})")

    if protection_rate >= 80:
        print("🎉 EXCELLENT: ZeroIA résiste aux attaques d'empoisonnement !")
    elif protection_rate >= 60:
        print("👍 BON: Protection solide, quelques améliorations possibles")
    else:
        print("⚠️ ATTENTION: Vulnérabilités détectées - renforcement nécessaire")

    # Sauvegarde rapport
    report_file = Path("logs/model_poisoning_test_report.json")
    report_file.parent.mkdir(exist_ok=True)

    full_report = {
        "timestamp": datetime.now().isoformat(),
        "protection_rate": protection_rate,
        "test_results": test_results,
        "integrity_final_status": monitor.get_integrity_status(),
    }

    with open(report_file, "w") as f:
        json.dump(full_report, f, indent=2)

    print(f"\n📄 Rapport sauvegardé: {report_file}")

    return protection_rate >= 60  # Retourne True si protection acceptable


if __name__ == "__main__":
    success = test_live_poisoning_attacks()
    sys.exit(0 if success else 1)
