from pathlib import Path

from modules.zeroia.reason_loop import check_for_ia_conflict
from tests.fixtures.test_helpers import ensure_test_toml

# Setup TOML minimal au cas où certains tests accèdent aux chemins globaux
ensure_test_toml()


def test_check_for_ia_conflict_detected(tmp_path: Path) -> None:
    log_path = tmp_path / "zeroia_contradictions.log"
    reflexia_decision = "monitor"
    zeroia_decision = "shutdown"

    result = check_for_ia_conflict(
        reflexia_decision=reflexia_decision,
        zeroia_decision=zeroia_decision,
        log_path=log_path,
    )

    assert result is True
    assert log_path.exists(), "Log file was not created"
    content = log_path.read_text()
    assert "CONTRADICTION" in content.upper()


def test_conflict_log_written(tmp_path: Path):
    """✅ Vérifie que le fichier de log est bien écrit en cas de divergence"""
    log_path = tmp_path / "contradiction.log"

    check_for_ia_conflict(
        reflexia_decision="monitor",
        zeroia_decision="shutdown",
        log_path=log_path,
    )

    assert log_path.exists(), "Log file was not created"
    log_content = log_path.read_text()
    assert "CONTRADICTION" in log_content.upper()


def test_contradiction_detection(tmp_path: Path):
    """🎯 Cas générique de détection d'une contradiction 'observe' ≠ 'shutdown'"""
    log_path = tmp_path / "conflict.log"

    check_for_ia_conflict(
        reflexia_decision="observe",
        zeroia_decision="shutdown",
        log_path=log_path,
    )

    assert log_path.exists(), "Log file was not created"
    log_content = log_path.read_text()
    assert "CONTRADICTION" in log_content.upper()
