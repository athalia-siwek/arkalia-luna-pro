from pathlib import Path

import toml

from modules.zeroia.reason_loop import check_for_ia_conflict

REFLEXIA_STATE = Path("tests/tmp/reflexia_state.toml")
ZEROIA_STATE = Path("tests/tmp/zeroia_state.toml")
CONFLICT_LOG = Path("tests/tmp/zeroia_contradictions.log")


def test_check_for_ia_conflict_detected(monkeypatch):
    toml.dump({"last_decision": "monitor"}, REFLEXIA_STATE.open("w"))
    toml.dump({"last_decision": "reduce_load"}, ZEROIA_STATE.open("w"))

    monkeypatch.setattr("modules.zeroia.reason_loop.REFLEXIA_STATE", REFLEXIA_STATE)
    monkeypatch.setattr("modules.zeroia.reason_loop.STATE_PATH", ZEROIA_STATE)
    monkeypatch.setattr("modules.zeroia.reason_loop.CONTRADICTION_LOG", CONFLICT_LOG)

    check_for_ia_conflict()

    assert CONFLICT_LOG.exists()
    log_content = CONFLICT_LOG.read_text()
    assert "CONTRADICTION DETECTED" in log_content

    REFLEXIA_STATE.unlink()
    ZEROIA_STATE.unlink()
    CONFLICT_LOG.unlink()


def test_conflict_log_written(tmp_path):
    reflexia_path = tmp_path / "reflexia.toml"
    zeroia_path = tmp_path / "zeroia.toml"
    log_path = tmp_path / "contradiction.log"

    toml.dump({"last_decision": "monitor"}, reflexia_path.open("w"))
    toml.dump({"last_decision": "shutdown"}, zeroia_path.open("w"))

    check_for_ia_conflict(log_path_override=log_path)

    log_content = log_path.read_text()
    assert "CONTRADICTION DETECTED" in log_content
