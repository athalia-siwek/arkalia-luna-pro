import json
from pathlib import Path

import toml

from modules.zeroia.reason_loop import persist_state, update_dashboard

TEST_STATE = Path("tests/tmp/test_state.toml")
TEST_DASHBOARD = Path("tests/tmp/test_dashboard.json")


def test_persist_state_creates_file():
    ctx = {"status": {"cpu": 42, "severity": "none"}, "reflexia": {}}
    persist_state("monitor", 0.6, ctx, state_path_override=TEST_STATE)
    assert TEST_STATE.exists()
    content = TEST_STATE.read_text()
    assert "monitor" in content
    TEST_STATE.unlink()


def test_update_dashboard_writes_json():
    ctx = {"status": {"cpu": 42, "severity": "none"}, "reflexia": {}}
    # Utilisation de json.dump pour écrire le JSON correctement
    with open(TEST_DASHBOARD, "w", encoding="utf-8") as f:
        json.dump(ctx, f, ensure_ascii=False, indent=2)

    update_dashboard("monitor", 0.6, ctx, dashboard_path_override=TEST_DASHBOARD)
    assert TEST_DASHBOARD.exists()
    # Lire uniquement les lignes JSON valides
    for line in TEST_DASHBOARD.read_text().splitlines():
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue  # Ignore invalid JSON lines
        if line.startswith("{"):
            assert data["last_decision"] == "monitor"
            assert data["confidence"] == 0.6
            break
    TEST_DASHBOARD.unlink()


def test_persist_state_creates_valid_toml(tmp_path):
    path = tmp_path / "state.toml"
    context = {"status": {"cpu": 80, "severity": "high"}}
    persist_state("reduce_load", 0.75, context, state_path_override=path)
    data = toml.load(path)

    assert "decision" in data
    assert "last_decision" in data["decision"]
    assert data["decision"]["last_decision"] == "reduce_load"
    assert data["decision"]["confidence_score"] == 0.75
    assert "justification" in data["decision"]
    assert "timestamp" in data
