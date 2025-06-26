from pathlib import Path
from unittest.mock import mock_open, patch

from modules.zeroia.failsafe import load_snapshot, restore_backup


def test_load_snapshot_error_handling():
    with patch("toml.load", side_effect=Exception("Test error")):
        with patch("builtins.open", mock_open()):
            result = load_snapshot(Path("invalid_snapshot.toml"))
            assert result is None


def test_restore_backup_success(tmp_path):
    backup_file = tmp_path / "zeroia_state_backup.toml"
    backup_file.write_text('key = "value"')

    state_file = tmp_path / "zeroia_state.toml"

    # Patch les chemins utilisés par restore_backup
    import modules.zeroia.failsafe as failsafe

    failsafe.BACKUP_PATH = backup_file
    failsafe.SNAPSHOT_PATH = state_file

    assert restore_backup() is True


def test_restore_backup_failure():
    with patch("pathlib.Path.exists", return_value=False):
        with patch("builtins.open", mock_open()):
            result = restore_backup()
            assert result is False
