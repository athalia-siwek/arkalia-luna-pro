# 📊 Arkalia IA Monitor
# Affiche un état synthétique de la cognition ZeroIA

import json
import subprocess
from pathlib import Path

import requests
import toml

STATE_PATH = Path("modules/zeroia/state/zeroia_state.toml")
DASHBOARD_PATH = Path("state/zeroia_dashboard.json")
LOG_FILE = Path("logs/failure_analysis.md")


def check_docker_status():
    try:
        result = subprocess.run(
            ["docker", "ps"], capture_output=True, text=True, check=True
        )
        if result.stdout:
            print("\n🐳 Docker — Conteneurs en cours d'exécution")
            print(result.stdout)
        else:
            print("\n🐳 Docker — Aucun conteneur en cours d'exécution")
    except subprocess.CalledProcessError as e:
        print(f"💥 Erreur Docker : {e}")


def ping_reflexia():
    try:
        response = requests.get("http://reflexia-endpoint/ping")
        if response.status_code == 200:
            print("\n🔗 Reflexia — Actif")
        else:
            print("\n🔗 Reflexia — Inactif")
    except requests.RequestException as e:
        print(f"💥 Erreur Reflexia : {e}")


def display_recent_errors():
    print("\n📝 Dernières erreurs connues")
    if LOG_FILE.exists():
        with LOG_FILE.open("r", encoding="utf-8") as f:
            lines = f.readlines()
            print(
                "".join(lines[-5:])
            )  # Affiche les 5 dernières lignes du fichier de log
    else:
        print("Aucune erreur connue.")


if __name__ == "__main__":
    print("\n📄 ZeroIA — TOML State")
    try:
        data = toml.load(STATE_PATH)
        print(toml.dumps(data))
    except Exception as e:
        print(f"💥 Erreur lecture TOML : {e}")

    print("\n📊 ZeroIA — Dashboard JSON")
    try:
        data = json.loads(DASHBOARD_PATH.read_text())
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"💥 Erreur lecture JSON : {e}")

    check_docker_status()
    ping_reflexia()
    display_recent_errors()
