"""
🧪 Test d'intégration minimal pour ZeroIA
"""

import pytest

from modules.zeroia.core import ZeroIACore


def test_zeroia_integration_basic():
    zeroia = ZeroIACore()
    status = zeroia.get_status()
    assert status is not None
