"""
🧪 Test d'intégration minimal pour AssistantIA (fonction process_input)
"""

import pytest

from modules.assistantia.utils.processing import process_input


@pytest.mark.integration
def test_assistantia_integration_basic():
    result = process_input("integration_test")
    assert result.startswith("Tu as dit :")
