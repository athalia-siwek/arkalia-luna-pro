from unittest.mock import patch

import modules.reflexia.core as reflexia_core
from modules.reflexia.core import launch_reflexia_loop


def test_launch_reflexia_check_mocked():
    """
    🧪 Test simulé : vérifie launch_reflexia_check avec des mocks pour chaque composant.
    """
    mocked_metrics = {"cpu": 0.5}
    mocked_status = "ok"

    with patch("modules.reflexia.core.read_metrics", return_value=mocked_metrics):
        with patch("modules.reflexia.core.monitor_status", return_value=mocked_status):
            with patch("modules.reflexia.core.save_snapshot") as mock_save:
                # Suppression de la variable inutilisée 'result'
                reflexia_core.launch_reflexia_check()
                mock_save.assert_called_once_with(mocked_metrics, mocked_status)


def test_launch_reflexia_loop(monkeypatch):
    """
    🔁 Test isolé : vérifie que la fonction reflexia_loop est bien appelée via
    launch_reflexia_loop.
    """
    called = {}

    def fake_loop():
        called["executed"] = True
        return True

    monkeypatch.setattr("modules.reflexia.logic.main_loop.reflexia_loop", fake_loop)
    launch_reflexia_loop()
    assert called.get("executed") is True


def test_launch_reflexia_check_realistic():
    """
    🧬 Test réel : exécute launch_reflexia_check avec un mock de save_snapshot
    pour vérifier qu'il est bien appelé dans des conditions réalistes.
    """
    state_log = []

    def mock_save_snapshot(metrics, status):
        state_log.append({"metrics": metrics, "status": status})

    with patch("modules.reflexia.core.save_snapshot", new=mock_save_snapshot):
        with patch("modules.reflexia.core.monitor_status", return_value="ok"):
            # Suppression de la variable inutilisée 'result'
            reflexia_core.launch_reflexia_check()

    assert len(state_log) == 1
    assert "metrics" in state_log[0]
    assert "status" in state_log[0]
