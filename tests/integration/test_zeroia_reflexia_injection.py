from pathlib import Path

import toml

from modules.zeroia.reason_loop import reason_loop
from tests.unit.test_helpers import ensure_test_toml

ensure_test_toml()


def test_reflexia_injection_success(tmp_path: Path):
    """🧪 Injection des données ReflexIA dans le contexte global"""
    # Réinitialise les variables anti-répétition pour ce test
    import modules.zeroia.reason_loop as rl

    rl.LAST_DECISION = None
    rl.LAST_DECISION_TIME = None

    ctx_path = tmp_path / "global_context.toml"
    reflexia_path = tmp_path / "reflexia_state.toml"
    state_path = tmp_path / "zeroia_state.toml"
    dashboard_path = tmp_path / "dashboard.json"

    toml.dump(
        {
            "status": {"cpu": 85, "ram": 50},
            "active": True,
        },
        ctx_path.open("w"),
    )

    toml.dump(
        {
            "reflexia": {"observation": "high cpu"},
            "status": {"cpu": 85, "ram": 50},
            "decision": {"last_decision": "reduce_load"},
        },
        reflexia_path.open("w"),
    )

    decision, score = reason_loop(
        context_path=ctx_path,
        reflexia_path=reflexia_path,
        state_path=state_path,
        dashboard_path=dashboard_path,
    )

    assert decision == "reduce_load"
    assert 0.7 <= score <= 1.0
    assert Path(state_path).exists()
    assert Path(dashboard_path).exists()
