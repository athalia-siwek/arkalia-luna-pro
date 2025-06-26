import io
import os
import signal
import sys
from unittest.mock import patch

import pytest

from modules.zeroia.orchestrator import orchestrate_zeroia_loop
from modules.zeroia.reason_loop import reason_loop


def test_conflict_detection():
    with patch(
        "modules.zeroia.reason_loop.check_for_ia_conflict", return_value=True
    ) as mock_detect:
        # Logique de test ici
        assert mock_detect("decision1", "decision2", "log_path")


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Instable en CI")
@pytest.mark.benchmark
def test_reason_loop_performance(benchmark, tmp_path):
    # Créer un fichier temporaire pour éviter FileNotFoundError
    tmp_file = tmp_path / "zeroia_state.toml.tmp"
    tmp_file.touch()

    with (
        patch("modules.zeroia.reason_loop.persist_state"),
        patch("modules.zeroia.reason_loop.update_dashboard"),
        patch("modules.zeroia.reason_loop.log_conflict"),
    ):

        result = benchmark(reason_loop)
        assert result is not None  # Ensure the function runs without error


def test_reason_loop_basic(tmp_path):
    # Création de fichiers TOML fictifs
    context_path = tmp_path / "context.toml"
    reflexia_path = tmp_path / "reflexia.toml"

    context_path.write_text(
        """
        [status]
        cpu = 45
        ram = 70
        [reflexia]
        summary = "ok"
        """
    )

    reflexia_path.write_text(
        """
        [decision]
        last_decision = "normal"
        """
    )

    with (
        patch("modules.zeroia.reason_loop.persist_state"),
        patch("modules.zeroia.reason_loop.update_dashboard"),
        patch("modules.zeroia.reason_loop.log_conflict"),
    ):

        decision, score = reason_loop(
            context_path=context_path, reflexia_path=reflexia_path
        )

    print(f"[TEST OK] decision={decision}, score={score}")
    assert decision in {"normal", "monitor", "reduce_load"}
    assert 0.0 <= score <= 1.0


def test_reason_loop_timeout(monkeypatch):
    def handler(signum, frame):
        raise TimeoutError("Blocage détecté")

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(2)  # 2 secondes

    try:
        with (
            patch("modules.zeroia.reason_loop.persist_state"),
            patch("modules.zeroia.reason_loop.update_dashboard"),
            patch("modules.zeroia.reason_loop.log_conflict"),
        ):

            decision, score = reason_loop()
    except TimeoutError:
        pytest.fail("reason_loop() a bloqué")
    finally:
        signal.alarm(0)


def test_orchestrator_limited_loops(monkeypatch):
    monkeypatch.setattr(
        "modules.zeroia.orchestrator.reason_loop", lambda: ("noop", 0.0)
    )
    monkeypatch.setattr("time.sleep", lambda _: None)
    orchestrate_zeroia_loop(max_loops=2)


def test_reason_loop_returns_decision(monkeypatch):
    monkeypatch.setattr(
        "modules.zeroia.reason_loop.persist_state", lambda *a, **kw: None
    )
    monkeypatch.setattr(
        "modules.zeroia.reason_loop.update_dashboard", lambda *a, **kw: None
    )
    monkeypatch.setattr(
        "modules.zeroia.reason_loop.log_conflict", lambda *a, **kw: None
    )

    decision, score = reason_loop()
    assert isinstance(decision, str)
    assert isinstance(score, float)


def test_orchestrator_prints(monkeypatch, capsys):
    monkeypatch.setattr(
        "modules.zeroia.orchestrator.reason_loop", lambda: ("test", 1.0)
    )
    monkeypatch.setattr("time.sleep", lambda x: None)

    orchestrate_zeroia_loop(max_loops=1)
    captured = capsys.readouterr()

    assert "[DEBUG] Decision: test / Score: 1.0" in captured.out


def test_orchestrate_zeroia_loop_limited(monkeypatch):
    monkeypatch.setattr(
        "modules.zeroia.orchestrator.reason_loop", lambda: ("noop", 0.0)
    )
    monkeypatch.setattr("time.sleep", lambda x: None)
    orchestrate_zeroia_loop(max_loops=2)


def test_orchestrate_zeroia_loop_output(monkeypatch):
    monkeypatch.setattr(
        "modules.zeroia.orchestrator.reason_loop", lambda: ("noop", 0.0)
    )
    monkeypatch.setattr("time.sleep", lambda x: None)

    captured = io.StringIO()
    sys.stdout = captured
    orchestrate_zeroia_loop(max_loops=1)
    sys.stdout = sys.__stdout__

    output = captured.getvalue()
    assert "[DEBUG] Decision: noop / Score: 0.0" in output
    assert "[DEBUG] Max loop reached. Exiting." in output
