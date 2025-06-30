from pathlib import Path
from unittest.mock import mock_open, patch

from modules.zeroia.failsafe import load_snapshot, restore_backup


def test_load_snapshot_error_handling() -> None:
    with patch("toml.load", side_effect=Exception("Test error")):
        with patch("builtins.open", mock_open()):
            result = load_snapshot("invalid_snapshot.toml")
            assert result is None


def test_restore_backup_success(tmp_path) -> None:
    backup_file = tmp_path / "zeroia_state_backup.toml"
    backup_file.write_text('key = "value"')

    state_file = tmp_path / "zeroia_state.toml"

    result = restore_backup(str(backup_file), str(state_file))
    assert result is True


def test_restore_backup_failure() -> None:
    with patch("shutil.copy2", side_effect=Exception("Test error")):
        result = restore_backup("backup.toml", "target.toml")
        assert result is False
