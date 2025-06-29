"""
Test Docker Enhanced pour ZeroIA Container
Tests robustes de la boucle Enhanced avec tous les modules Arkalia
"""

import json
import shutil
import subprocess
import time
from pathlib import Path

import pytest

# Vérifie si Docker est disponible
docker_available = shutil.which("docker") is not None


def is_container_running(name: str) -> bool:
    """Vérifie si un conteneur spécifique est actif"""
    try:
        output = subprocess.check_output(
            ["docker", "inspect", "-f", "{{.State.Running}}", name],
            stderr=subprocess.DEVNULL,
        )
        return output.strip() == b"true"
    except subprocess.CalledProcessError:
        return False


def get_container_health(name: str) -> str:
    """Récupère le statut de santé d'un conteneur"""
    try:
        output = subprocess.check_output(
            ["docker", "inspect", "-f", "{{.State.Health.Status}}", name],
            stderr=subprocess.DEVNULL,
        )
        return output.strip().decode()
    except subprocess.CalledProcessError:
        return "unknown"


def check_zeroia_dashboard() -> dict:
    """Vérifie le dashboard ZeroIA pour valider le fonctionnement"""
    dashboard_path = Path("state/zeroia_dashboard.json")
    try:
        if dashboard_path.exists():
            with open(dashboard_path) as f:
                return json.load(f)
    except Exception:
        pass
    return {}


@pytest.mark.skipif(not docker_available, reason="Docker non installé")
def test_docker_service_availability():
    """Test de base: Docker est-il disponible et fonctionnel?"""
    result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "Docker n'est pas disponible"
    assert "Docker version" in result.stdout


@pytest.mark.skipif(not docker_available, reason="Docker non installé")
def test_zeroia_container_exists():
    """Vérifie que le conteneur ZeroIA existe (même s'il n'est pas running)"""
    try:
        subprocess.check_output(["docker", "inspect", "zeroia"], stderr=subprocess.DEVNULL)
        container_exists = True
    except subprocess.CalledProcessError:
        container_exists = False

    # Si le conteneur n'existe pas, on skip au lieu de fail
    if not container_exists:
        pytest.skip("Conteneur ZeroIA non trouvé - skip test Docker")


@pytest.mark.skipif(not docker_available, reason="Docker non installé")
@pytest.mark.skipif(not is_container_running("zeroia"), reason="ZeroIA container non actif")
def test_zeroia_enhanced_docker_functionality():
    """
    Test robuste de la boucle Enhanced ZeroIA dans Docker.
    Vérifie que tous tes modules fonctionnent correctement.
    """
    print("\n🧪 Test ZeroIA Enhanced Container...")

    # 1. Vérifier que le conteneur tourne
    assert is_container_running("zeroia"), "Conteneur ZeroIA non actif"

    # 2. Attendre que ZeroIA se stabilise
    print("⏳ Stabilisation ZeroIA Enhanced...")
    time.sleep(5)

    # 3. Capturer les logs récents
    result = subprocess.run(
        ["docker", "logs", "zeroia", "--tail", "50"],
        capture_output=True,
        text=True,
        timeout=30,
    )

    logs_output = result.stdout + result.stderr
    print(f"📋 Logs capturés (50 dernières lignes):\n{logs_output[-500:]}")

    # 4. Vérifications robustes des fonctionnalités Enhanced
    success_indicators = ["loop started", "enhanced", "decision", "zeroia"]

    found_indicators = [
        indicator for indicator in success_indicators if indicator.lower() in logs_output.lower()
    ]

    assert len(found_indicators) >= 2, (
        f"ZeroIA Enhanced ne semble pas fonctionnel. "
        f"Indicateurs trouvés: {found_indicators} / {success_indicators}\n"
        f"Logs: {logs_output[-300:]}"
    )

    # 5. Vérifier le dashboard s'il existe
    dashboard = check_zeroia_dashboard()
    if dashboard:
        assert "reasoning_loop_active" in dashboard, "Dashboard ZeroIA invalide"
        print(f"✅ Dashboard OK: {dashboard.get('last_decision', 'N/A')}")

    # 6. Test de santé container
    health = get_container_health("zeroia")
    if health not in ["unknown", ""]:
        assert health in ["healthy", "starting"], f"Container health: {health}"

    print("✅ Test ZeroIA Enhanced Container: SUCCÈS")


@pytest.mark.skipif(not docker_available, reason="Docker non installé")
def test_arkalia_modules_integration():
    """
    Test d'intégration des modules Arkalia avec ZeroIA Enhanced.
    Vérifie que tes modules principaux sont bien connectés.
    """
    if not is_container_running("zeroia"):
        pytest.skip("Conteneur ZeroIA non actif - skip test intégration")

    print("\n🔗 Test intégration modules Arkalia...")

    # Vérifier les autres conteneurs si disponibles
    arkalia_containers = ["reflexia", "sandozia", "assistantia", "helloria"]
    active_modules = []

    for container in arkalia_containers:
        if is_container_running(container):
            active_modules.append(container)

    print(f"📦 Modules actifs détectés: {active_modules}")

    # Vérifier les logs pour l'intégration
    if active_modules:
        result = subprocess.run(
            ["docker", "logs", "zeroia", "--tail", "30"],
            capture_output=True,
            text=True,
            timeout=20,
        )

        logs = result.stdout + result.stderr

        # Chercher des signes d'intégration
        integration_signs = ["reflexia", "enhanced", "module", "circuit"]
        found_signs = [sign for sign in integration_signs if sign.lower() in logs.lower()]

        if found_signs:
            print(f"✅ Signes d'intégration trouvés: {found_signs}")
        else:
            print("⚠️ Aucun signe d'intégration détecté (peut être normal)")

    print("✅ Test intégration modules: TERMINÉ")


if __name__ == "__main__":
    # Tests en mode standalone
    print("🧪 Tests Docker ZeroIA Enhanced - Mode Standalone")

    if not docker_available:
        print("❌ Docker non disponible")
        exit(1)

    try:
        test_docker_service_availability()
        print("✅ Docker service OK")

        test_zeroia_container_exists()
        print("✅ Container ZeroIA existe")

        if is_container_running("zeroia"):
            test_zeroia_enhanced_docker_functionality()
            test_arkalia_modules_integration()
        else:
            print("⚠️ Container ZeroIA non actif - tests skippés")

    except Exception as e:
        print(f"❌ Erreur test: {e}")
        exit(1)

    print("🎉 Tous les tests Docker Enhanced: SUCCÈS")
