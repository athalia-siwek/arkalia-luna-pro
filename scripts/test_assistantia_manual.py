#!/usr/bin/env python3
"""
🧪 Test AssistantIA - Script de validation v2.8.0
Teste le bon fonctionnement d'AssistantIA avec Ollama
"""

import asyncio
import json
import time
from pathlib import Path
from typing import Any

import requests


class AssistantIATester:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []

    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Enregistre un résultat de test"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": time.time(),
        }
        self.test_results.append(result)

        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {details}")

    def test_health_endpoint(self) -> bool:
        """Teste l'endpoint de santé"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, f"Status: {data.get('status')}")
                return True
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Erreur: {str(e)}")
            return False

    def test_models_endpoint(self) -> bool:
        """Teste l'endpoint des modèles disponibles"""
        try:
            response = requests.get(f"{self.base_url}/models", timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                model_names = [m.get("name", "") for m in models]
                self.log_test("Models Endpoint", True, f"Modèles: {', '.join(model_names)}")
                return True
            else:
                self.log_test("Models Endpoint", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Models Endpoint", False, f"Erreur: {str(e)}")
            return False

    def test_chat_endpoint(self, message: str = "Bonjour, comment allez-vous ?") -> bool:
        """Teste l'endpoint de chat"""
        try:
            payload = {
                "message": message,
                "model": "mistral:latest",
                "temperature": 0.7,
                "include_context": True,
            }

            response = requests.post(f"{self.base_url}/api/v1/chat", json=payload, timeout=30)

            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")
                processing_time = data.get("processing_time", 0)
                context_quality = data.get("context_quality", 0)

                self.log_test(
                    "Chat Endpoint",
                    True,
                    f"Réponse: {response_text[:50]}... | Temps: {processing_time:.2f}s | Qualité contexte: {context_quality}",
                )
                return True
            else:
                self.log_test("Chat Endpoint", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Chat Endpoint", False, f"Erreur: {str(e)}")
            return False

    def test_ollama_connection(self) -> bool:
        """Teste la connexion à Ollama"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                model_names = [m.get("name", "") for m in models]
                self.log_test(
                    "Ollama Connection", True, f"Modèles disponibles: {', '.join(model_names)}"
                )
                return True
            else:
                self.log_test("Ollama Connection", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Ollama Connection", False, f"Erreur: {str(e)}")
            return False

    def test_arkalia_context(self) -> bool:
        """Teste la récupération du contexte Arkalia"""
        try:
            # Vérifier les fichiers d'état
            state_files = [
                "state/zeroia_dashboard.json",
                "state/reflexia_state.toml",
                "state/sandozia",
                "state/cognitive_reactor_state.toml",
            ]

            available_contexts = []
            for file_path in state_files:
                if Path(file_path).exists():
                    available_contexts.append(Path(file_path).name)

            if available_contexts:
                self.log_test(
                    "Arkalia Context", True, f"Contexte disponible: {', '.join(available_contexts)}"
                )
                return True
            else:
                self.log_test("Arkalia Context", False, "Aucun contexte disponible")
                return False
        except Exception as e:
            self.log_test("Arkalia Context", False, f"Erreur: {str(e)}")
            return False

    def test_metrics_endpoint(self) -> bool:
        """Teste l'endpoint des métriques Prometheus"""
        try:
            response = requests.get(f"{self.base_url}/metrics", timeout=10)
            if response.status_code == 200:
                content = response.text
                if "assistantia_prompts_total" in content:
                    self.log_test("Metrics Endpoint", True, "Métriques Prometheus disponibles")
                    return True
                else:
                    self.log_test("Metrics Endpoint", False, "Métriques Prometheus manquantes")
                    return False
            else:
                self.log_test("Metrics Endpoint", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Metrics Endpoint", False, f"Erreur: {str(e)}")
            return False

    def run_all_tests(self) -> dict[str, Any]:
        """Exécute tous les tests"""
        print("🧪 Démarrage des tests AssistantIA...")
        print("=" * 50)

        tests = [
            ("Ollama Connection", self.test_ollama_connection),
            ("Health Endpoint", self.test_health_endpoint),
            ("Models Endpoint", self.test_models_endpoint),
            ("Arkalia Context", self.test_arkalia_context),
            ("Chat Endpoint", self.test_chat_endpoint),
            ("Metrics Endpoint", self.test_metrics_endpoint),
        ]

        passed = 0
        total = len(tests)

        for _test_name, test_func in tests:
            if test_func():
                passed += 1

        print("=" * 50)
        print(f"📊 Résultats: {passed}/{total} tests réussis")

        # Test de chat avancé
        print("\n🤖 Test de conversation avancée...")
        advanced_tests = [
            "Explique-moi le rôle de ZeroIA dans Arkalia-LUNA",
            "Quelle est la différence entre Reflexia et Sandozia ?",
            "Comment fonctionne le système de monitoring ?",
        ]

        for question in advanced_tests:
            print(f"\n❓ Question: {question}")
            self.test_chat_endpoint(question)
            time.sleep(2)  # Pause entre les questions

        return {
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": total - passed,
            "success_rate": (passed / total) * 100 if total > 0 else 0,
            "test_results": self.test_results,
        }

    def save_results(self, filename: str = "logs/assistantia_test_results.json"):
        """Sauvegarde les résultats des tests"""
        try:
            Path(filename).parent.mkdir(exist_ok=True)
            with open(filename, "w") as f:
                json.dump(self.test_results, f, indent=2)
            print(f"💾 Résultats sauvegardés dans {filename}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")


def main():
    """Fonction principale"""
    tester = AssistantIATester()
    results = tester.run_all_tests()
    tester.save_results()

    print("\n🎯 Résumé final:")
    print(f"   Tests réussis: {results['passed_tests']}/{results['total_tests']}")
    print(f"   Taux de succès: {results['success_rate']:.1f}%")

    if results["success_rate"] >= 80:
        print("🎉 AssistantIA fonctionne correctement !")
        return 0
    else:
        print("⚠️  AssistantIA nécessite des corrections.")
        return 1


if __name__ == "__main__":
    exit(main())
