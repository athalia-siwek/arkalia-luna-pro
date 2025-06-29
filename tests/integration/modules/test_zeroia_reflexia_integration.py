from modules.zeroia import reason_loop


def test_decide_emergency_from_reflexia():
    ctx = {
        "status": {"cpu": 51.1, "severity": "critical"},
        "reflexia": {"last_snapshot": "🛑 surcharge CPU"},
    }
    assert reason_loop.decide(ctx)[0] == "emergency_shutdown"
