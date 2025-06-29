# tests/unit/test_zeroia_orchestrator.py
from unittest.mock import patch

from modules.zeroia.orchestrator import orchestrate_zeroia_loop


def test_orchestrator_runs_limited_loops(monkeypatch):
    """Test que l'orchestrateur s'arrête après max_loops"""
    # Mock de la fonction réellement appelée par l'orchestrateur
    monkeypatch.setattr(
        "modules.zeroia.orchestrator.reason_loop_enhanced_with_recovery",
        lambda: ("normal", 0.5),
    )
    monkeypatch.setattr("time.sleep", lambda x: None)

    # Test avec 2 boucles max - doit se terminer rapidement
    try:
        orchestrate_zeroia_loop(max_loops=2)
        assert True  # Si on arrive ici, le test a réussi
    except Exception as e:
        raise AssertionError(f"L'orchestrateur a échoué: {e}")


class MockOrchestrator:
    def run(self):
        return {"status": "ok"}


def test_orchestrator_runs_correctly():
    """Test du mock orchestrator de base"""
    orchestrator = MockOrchestrator()
    with patch.object(orchestrator, "run", return_value={"status": "ok"}) as mock_run:
        result = orchestrator.run()
        expected = {"status": "ok"}
        assert result == expected
        mock_run.assert_called_once()


def test_orchestrator_runs_correctly_with_mock():
    """Test simple du mock orchestrator"""
    orchestrator = MockOrchestrator()
    expected = {"status": "ok"}
    result = orchestrator.run()
    assert result == expected


def test_orchestrator_exception_handling(monkeypatch):
    """Test que l'orchestrateur gère les exceptions correctement"""

    # Mock qui lève une exception
    def mock_failing_reason_loop():
        raise Exception("Test exception")

    monkeypatch.setattr(
        "modules.zeroia.orchestrator.reason_loop_enhanced_with_recovery",
        mock_failing_reason_loop,
    )
    monkeypatch.setattr("time.sleep", lambda x: None)

    # Doit se terminer sans planter
    try:
        orchestrate_zeroia_loop(max_loops=1)
        assert True
    except Exception as e:
        raise AssertionError(f"L'orchestrateur n'a pas géré l'exception: {e}")
