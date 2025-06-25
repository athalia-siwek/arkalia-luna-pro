# tests/unit/test_zeroia_dashboard_output.py
import json

from modules.zeroia.reason_loop import update_dashboard


def test_update_dashboard_creates_json(tmp_path):
    path = tmp_path / "dashboard.json"
    context = {"reflexia": {}, "status": {"cpu": 72, "severity": "medium"}}

    update_dashboard("monitor", 0.65, context, dashboard_path_override=path)
    data = json.loads(path.read_text())

    assert data["last_decision"] == "monitor"
    assert data["confidence"] == 0.65
    assert data["reasoning_loop_active"] is True
    assert "last_updated" in data
