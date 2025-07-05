#!/usr/bin/env python3
# 🧠 Monitor ReflexIA State — Arkalia LUNA

from core.ark_logger import ark_logger
import json
from pathlib import Path

import requests

STATE_FILE = Path("modules/reflexia/state/reflexia_state.json")
GRAFANA_API_URL = "http://your-grafana-instance/api/dashboards/db"
GRAFANA_API_KEY = "your_grafana_api_key"  # pragma: allowlist secret


def read_state() -> dict:
    if not STATE_FILE.exists():
        return {"status": "💥", "error": "Fichier reflexia_state.json introuvable."}

    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return {"status": "✅", "data": data}
    except json.JSONDecodeError as e:
        return {"status": "💥", "error": f"Erreur JSON: {e}"}


def display_info(result: dict) -> None:
    if result["status"] != "✅":
        ark_logger.error(f"[ERREUR] {result['error']}", extra={"module": "scripts"})
        return

    data = result["data"]
    ark_logger.info("🔎 État actuel de ReflexIA\n", extra={"module": "scripts"})

    ark_logger.info(f"🧠 Reasoning loop active : {data.get('reasoning_loop_active', False, extra={"module": "scripts"})}")
    ark_logger.info(f"📌 Dernière décision      : {data.get('last_decision', 'N/A', extra={"module": "scripts"})}")
    ark_logger.info(f"🕰️ Timestamp              : {data.get('timestamp', 'N/A', extra={"module": "scripts"})}")
    ark_logger.info(f"📜 Historique décisions   : {data.get('previous', [], extra={"module": "scripts"})}")


def export_to_grafana(data) -> None:
    headers = {
        "Authorization": f"Bearer {GRAFANA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "dashboard": {
            "id": None,
            "title": "ReflexIA Dashboard",
            "panels": [
                {
                    "type": "graph",
                    "title": "Reasoning Loop Active",
                    "targets": [
                        {
                            "refId": "A",
                            "target": data.get("reasoning_loop_active", False),
                        }
                    ],
                },
                {
                    "type": "graph",
                    "title": "Last Decision",
                    "targets": [{"refId": "B", "target": data.get("last_decision", "N/A")}],
                },
            ],
        },
        "overwrite": True,
    }
    response = requests.post(GRAFANA_API_URL, headers=headers, json=payload, timeout=10)
    if response.status_code == 200:
        ark_logger.info("✅ Exportation vers Grafana réussie.", extra={"module": "scripts"})
    else:
        ark_logger.info(f"❌ Erreur lors de l'exportation vers Grafana : {response.content}", extra={"module": "scripts"})


if __name__ == "__main__":
    res = read_state()
    display_info(res)
    if res["status"] == "✅":
        export_to_grafana(res["data"])
