"""
🧪 Test d'intégration minimal pour AssistantIA
"""
import pytest

from modules.assistantia.core import AssistantIA


@pytest.mark.integration
def test_assistantia_integration_basic():
    assistant = AssistantIA()
    response = assistant.process_input({"input": "integration_test"})
    assert response is not None
