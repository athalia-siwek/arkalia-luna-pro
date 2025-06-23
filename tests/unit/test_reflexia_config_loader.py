import pytest

from modules.reflexia.utils.config_loader import load_weights


def test_load_valid_weights(tmp_path):
    config_path = tmp_path / "weights.toml"
    config_path.write_text("cpu = 1.0\nram = 1.0\nlatency = 1.0")
    config = load_weights(str(config_path))
    assert config["cpu"] == 1.0


def test_load_missing_file():
    with pytest.raises(FileNotFoundError):
        load_weights("nonexistent.toml")


def test_load_invalid_format(tmp_path):
    config_path = tmp_path / "broken.toml"
    config_path.write_text("💀 invalid_toml = !!!")
    with pytest.raises(Exception):
        load_weights(str(config_path))


def test_config_loader_missing_file():
    with pytest.raises(FileNotFoundError):
        load_weights("/nonexistent/path/config.toml")


def test_config_loader_invalid_format(tmp_path):
    config_path = tmp_path / "invalid.toml"
    config_path.write_text("[bad\n]")
    with pytest.raises(Exception):
        load_weights(str(config_path))
