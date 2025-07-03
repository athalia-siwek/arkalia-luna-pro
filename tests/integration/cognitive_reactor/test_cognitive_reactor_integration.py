"""
🧪 Test d'intégration minimal pour CognitiveReactor
"""

import pytest

from modules.cognitive_reactor.core import CognitiveReactor


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cognitive_reactor_integration_basic():
    reactor = CognitiveReactor()
    stimulus = {"type": "integration_test", "severity": "low", "source": "test", "data": {}}
    result = await reactor.process_stimulus(stimulus)
    assert result is not None
    assert "reaction" in result
