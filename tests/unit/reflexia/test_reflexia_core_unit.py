# 📄 tests/unit/test_reflexia_core.py

from modules.reflexia.core import load_reflexia_data


def test_load_reflexia_data_valid() -> None:
    data = load_reflexia_data()  # Suppose qu'un mock de toml existe
    assert isinstance(data, dict)
