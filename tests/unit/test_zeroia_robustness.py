import toml

from modules.zeroia.reason_loop import (
    check_for_ia_conflict,
    decide,
    persist_state,
    update_dashboard,
)
from tests.unit.test_helpers import ensure_test_toml, ensure_zeroia_state_file

ensure_test_toml()


def test_decide_with_empty_context():
    """Test 1: Vérifie que la fonction decide() ne plante pas même si le contexte
    est vide."""
    ensure_zeroia_state_file()
    decision, score = decide({})
    assert decision == "normal"
    assert score == 0.4


def test_dashboard_and_state_write_resilience(tmp_path, monkeypatch):
    """
    Test 2: Vérifie que persist_state() et update_dashboard() écrivent
    bien les fichiers, même si le dossier est recréé à la volée.
    """
    state_path = tmp_path / "zeroia_state.toml"
    dashboard_path = tmp_path / "zeroia_dashboard.json"

    monkeypatch.setattr("modules.zeroia.reason_loop.STATE_PATH", state_path)
    monkeypatch.setattr("modules.zeroia.reason_loop.DASHBOARD_PATH", dashboard_path)

    persist_state("monitor", 0.6, {})
    update_dashboard("monitor", 0.6, {})

    assert state_path.exists()
    assert dashboard_path.exists()


def test_contradiction_detection_log_creation(tmp_path, monkeypatch):
    """
    Test 3: Simule une contradiction entre Reflexia et ZeroIA
    et vérifie que le fichier zeroia_contradictions.log est bien créé.
    """
    reflexia_path = tmp_path / "reflexia_state.toml"
    contradiction_log_path = tmp_path / "zeroia_contradictions.log"
    state_path = tmp_path / "zeroia_state.toml"

    monkeypatch.setattr("modules.zeroia.reason_loop.REFLEXIA_STATE", reflexia_path)
    monkeypatch.setattr("modules.zeroia.reason_loop.STATE_PATH", state_path)

    with open(reflexia_path, "w") as f:
        toml.dump({"last_decision": "reduce_load"}, f)

    toml.dump({"decision": {"last_decision": "shutdown"}}, state_path.open("w"))

    check_for_ia_conflict(log_path_override=contradiction_log_path)

    assert contradiction_log_path.exists()
