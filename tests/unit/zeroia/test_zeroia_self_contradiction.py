from pathlib import Path

import toml

from modules.zeroia.reason_loop import reason_loop
from tests.common.test_helpers import ensure_test_toml

ensure_test_toml()


def test_self_contradiction_detected(tmp_path: Path):
    """🧠 Simule une contradiction : ReflexIA ≠ ZeroIA"""
    # Réinitialise les variables anti-répétition pour ce test
    import modules.zeroia.reason_loop as rl

    rl.LAST_DECISION = None
    rl.LAST_DECISION_TIME = None

    ctx_path = tmp_path / "global_context.toml"
    reflexia_path = tmp_path / "reflexia_state.toml"
    state_path = tmp_path / "zeroia_state.toml"
    dashboard_path = tmp_path / "dashboard.json"
    log_path = tmp_path / "conflict.log"

    toml.dump(
        {
            "status": {"cpu": 95, "ram": 60},
            "active": True,
        },
        ctx_path.open("w"),
    )

    toml.dump(
        {
            "reflexia": {"observation": "critical load"},
            "status": {"cpu": 95, "ram": 60},
            "decision": {"last_decision": "monitor"},
        },
        reflexia_path.open("w"),
    )

    decision, _ = reason_loop(
        context_path=ctx_path,
        reflexia_path=reflexia_path,
        state_path=state_path,
        dashboard_path=dashboard_path,
        contradiction_log_path=log_path,
    )

    assert decision == "reduce_load"
    assert log_path.exists()
    assert "CONTRADICTION" in log_path.read_text().upper()
