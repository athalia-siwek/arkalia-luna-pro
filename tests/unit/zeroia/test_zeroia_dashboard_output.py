# tests/unit/test_zeroia_dashboard_output.py
import json

from modules.zeroia.reason_loop import update_dashboard


def test_update_dashboard_creates_json(tmp_path) -> None:
    path = tmp_path / "dashboard.json"
    context = {"reflexia": {}, "status": {"cpu": 72, "severity": "medium"}}

    # Utilisation de json.dump pour écrire le JSON correctement
    with open(path, "w", encoding="utf-8") as f:
        json.dump(context, f, ensure_ascii=False, indent=2)

    update_dashboard("monitor", 0.65, context, dashboard_path_override=path)
    # Lire uniquement les lignes JSON valides
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    assert data["last_decision"] == "monitor"
