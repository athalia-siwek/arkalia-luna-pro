import pytest

from modules.reflexia.utils.config_loader import load_weights


def test_invalid_weights_config(tmp_path):
    broken_config = tmp_path / "broken.toml"
    broken_config.write_text("💀 invalid_toml = !!?!")

    with pytest.raises(Exception):
        load_weights()
