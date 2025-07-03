import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from scripts import zeroia_rollback

PROJECT_ROOT = Path(__file__).resolve().parents[3]


# 📁 Setup de répertoires temporaires pour simuler l'état ZeroIA
@pytest.fixture
def temp_env(monkeypatch) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        state_file = tmp_path / "zeroia_state.toml"
        snapshot_file = tmp_path / "zeroia_state_snapshot.toml"
        backup_file = tmp_path / "zeroia_state_backup.toml"
        log_file = tmp_path / "zeroia_rollback.log"
        failure_log = tmp_path / "failure_analysis.md"

        # Initialisation fichiers
        state_file.write_text('timestamp = "TEST"\n[decision]\nlast_decision = "noop"\n')
        snapshot_file.write_text('timestamp = "SNAPSHOT"\n[decision]\nlast_decision = "snapshot"\n')

        # Patch chemins internes du module
        monkeypatch.setattr(zeroia_rollback, "STATE_FILE", state_file)
        monkeypatch.setattr(zeroia_rollback, "SNAPSHOT_FILE", snapshot_file)
        monkeypatch.setattr(zeroia_rollback, "BACKUP_FILE", backup_file)
        monkeypatch.setattr(zeroia_rollback, "LOG_FILE", log_file)
        monkeypatch.setattr(zeroia_rollback, "FAILURE_LOG", failure_log)

        yield {
            "state_file": state_file,
            "snapshot_file": snapshot_file,
            "backup_file": backup_file,
            "log_file": log_file,
            "failure_log": failure_log,
        }


def test_backup_current_state(temp_env) -> None:
    zeroia_rollback.backup_current_state()
    assert temp_env["backup_file"].exists()
    assert "timestamp" in temp_env["backup_file"].read_text()


def test_restore_snapshot_success(temp_env) -> None:
    assert zeroia_rollback.restore_snapshot() is True
    assert temp_env["state_file"].read_text().find("snapshot") != -1


def test_restore_snapshot_failure(monkeypatch, temp_env) -> None:
    monkeypatch.setattr(zeroia_rollback, "SNAPSHOT_FILE", Path("nonexistent.toml"))
    assert zeroia_rollback.restore_snapshot() is False


def test_log_failure(temp_env) -> None:
    zeroia_rollback.log_failure()
    assert temp_env["failure_log"].exists()
    assert "Échec détecté" in temp_env["failure_log"].read_text()


def test_log(temp_env) -> None:
    zeroia_rollback.log("test log line")
    content = temp_env["log_file"].read_text()
    assert "[rollback] test log line" in content


def test_rollback_success(temp_env) -> None:
    temp_env["backup_file"].write_text(
        'timestamp = "BACKUP"\n[decision]\nlast_decision = "rollback"\n'
    )
    zeroia_rollback.rollback_from_backup()
    assert "rollback" in temp_env["state_file"].read_text()


def test_rollback_failure(monkeypatch) -> None:
    monkeypatch.setattr(zeroia_rollback, "BACKUP_FILE", Path("nonexistent.toml"))
    monkeypatch.setattr(zeroia_rollback, "STATE_FILE", Path("state/zeroia_state.toml"))
    zeroia_rollback.rollback_from_backup()


def test_zeroia_rollback_script_runs():
    """Teste que le script zeroia_rollback s'exécute sans erreur"""
    result = subprocess.run(
        ["python", "scripts/zeroia_rollback.py", "--silent"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    # Vérifie que le script s'exécute sans erreur
    assert result.returncode == 0, f"Script a échoué avec code {result.returncode}"

    # Vérifie que la sortie contient les messages attendus ou est vide (mode silent)
    output = result.stdout
    if output:  # Si il y a une sortie
        assert "🗄️" in output or "✅" in output or "❌" in output
    # Si pas de sortie, c'est normal en mode silent
