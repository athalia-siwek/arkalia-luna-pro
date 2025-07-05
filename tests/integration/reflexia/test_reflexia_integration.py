"""
🧪 Test d'intégration minimal pour ReflexIA (fonction launch_reflexia_check)
"""

import pytest

from modules.reflexia.core import launch_reflexia_check


def test_reflexia_integration_basic():
    result = launch_reflexia_check()
    assert isinstance(result, dict)
    assert "status" in result
    assert "metrics" in result
