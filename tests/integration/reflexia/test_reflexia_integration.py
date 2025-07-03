"""
🧪 Test d'intégration minimal pour ReflexIA
"""
import pytest

from modules.reflexia.core import ReflexIA


def test_reflexia_integration_basic():
    reflex = ReflexIA()
    result = reflex.check_status()
    assert result is not None
