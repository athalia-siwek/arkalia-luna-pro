import toml

from modules.zeroia.reason_loop import check_for_ia_conflict


def write_toml(path, content):
    with open(path, "w") as f:
        toml.dump(content, f)


def test_contradiction_detection(tmp_path, monkeypatch):
    """
    Simule une divergence de décision entre ReflexIA et ZeroIA,
    et vérifie la détection + création du log de contradiction.
    """
    reflexia_path = tmp_path / "reflexia_state.toml"
    zeroia_path = tmp_path / "zeroia_state.toml"
    contradiction_log = tmp_path / "zeroia_contradictions.log"

    write_toml(reflexia_path, {"last_decision": "reduce_load"})
    write_toml(zeroia_path, {"last_decision": "normal"})

    monkeypatch.setattr("modules.zeroia.reason_loop.REFLEXIA_STATE", reflexia_path)
    monkeypatch.setattr("modules.zeroia.reason_loop.STATE_PATH", zeroia_path)

    check_for_ia_conflict(
        reflexia_state_path=reflexia_path,
        zeroia_state_path=zeroia_path,
        log_path_override=contradiction_log,
    )

    assert contradiction_log.exists()
    with open(contradiction_log) as f:
        log_content = f.read()
        assert "CONTRADICTION DETECTED" in log_content
        assert "reduce_load" in log_content
        assert "normal" in log_content
