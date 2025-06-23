# tests/integration/test_reflexia_adaptative.py
from modules.reflexia.core import launch_reflexia_check


def test_launch_reflexia_check_runs():
    result = launch_reflexia_check()
    assert isinstance(result, dict)
    assert "status" in result