# 📄 tests/unit/test_reflexia_core_api.py

from modules.reflexia.core_api import get_reflexia_status


def test_get_reflexia_status_returns_dict():
    result = get_reflexia_status()
    assert isinstance(result, dict)
    assert "status" in result
