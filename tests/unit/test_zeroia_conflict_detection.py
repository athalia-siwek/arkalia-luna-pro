# 📄 tests/unit/test_zeroia_conflict_detection.py

from pathlib import Path

import toml

from modules.zeroia.reason_loop import check_for_ia_conflict
from tests.unit.test_helpers import ensure_test_toml, ensure_zeroia_state_file

REFLEXIA_STATE = Path("tests/tmp/reflexia_state.toml")
ZEROIA_STATE = Path("tests/tmp/zeroia_state.toml")
CONFLICT_LOG = Path("tests/tmp/zeroia_contradictions.log")

# 🧪 Setup initial obligatoire pour certains tests
ensure_test_toml()


def test_check_for_ia_conflict_detected(monkeypatch):
    """
    💥 Détection d'une contradiction explicite entre ReflexIA et ZeroIA
    (mocked paths)
    """
    ensure_zeroia_state_file()
    REFLEXIA_STATE.parent.mkdir(parents=True, exist_ok=True)

    toml.dump({"decision": {"last_decision": "monitor"}}, REFLEXIA_STATE.open("w"))
    toml.dump({"decision": {"last_decision": "shutdown"}}, ZEROIA_STATE.open("w"))

    monkeypatch.setattr("modules.zeroia.reason_loop.REFLEXIA_STATE", REFLEXIA_STATE)
    monkeypatch.setattr("modules.zeroia.reason_loop.STATE_PATH", ZEROIA_STATE)
    monkeypatch.setattr("modules.zeroia.reason_loop.CONTRADICTION_LOG", CONFLICT_LOG)

    check_for_ia_conflict(log_path_override=CONFLICT_LOG)

    assert CONFLICT_LOG.exists(), "Log file was not created"
    log_content = CONFLICT_LOG.read_text()
    assert "CONTRADICTION DETECTED" in log_content.upper()

    # 🧼 Nettoyage
    for path in [REFLEXIA_STATE, ZEROIA_STATE, CONFLICT_LOG]:
        path.unlink(missing_ok=True)


def test_conflict_log_written(tmp_path: Path):
    """✅ Vérifie que le fichier de log est bien écrit en cas de divergence"""
    reflexia_path = tmp_path / "reflexia_state.toml"
    zeroia_path = tmp_path / "zeroia_state.toml"
    log_path = tmp_path / "contradiction.log"

    toml.dump({"decision": {"last_decision": "monitor"}}, reflexia_path.open("w"))
    toml.dump({"decision": {"last_decision": "shutdown"}}, zeroia_path.open("w"))

    check_for_ia_conflict(
        reflexia_path_override=reflexia_path,
        zeroia_state_path=zeroia_path,
        log_path_override=log_path,
    )

    assert log_path.exists(), "Log file was not created"
    log_content = log_path.read_text()
    assert "CONTRADICTION DETECTED" in log_content.upper()


def test_contradiction_detection(tmp_path: Path):
    """🎯 Cas générique de détection d'une contradiction 'observe' ≠ 'shutdown'"""
    reflexia_path = tmp_path / "reflexia.toml"
    zeroia_path = tmp_path / "zeroia.toml"
    log_path = tmp_path / "conflict.log"

    toml.dump({"decision": {"last_decision": "observe"}}, reflexia_path.open("w"))
    toml.dump({"decision": {"last_decision": "shutdown"}}, zeroia_path.open("w"))

    check_for_ia_conflict(
        reflexia_path_override=reflexia_path,
        zeroia_state_path=zeroia_path,
        log_path_override=log_path,
    )

    assert log_path.exists(), "Log file was not created"
    log_content = log_path.read_text()
    assert "CONTRADICTION DETECTED" in log_content.upper()
