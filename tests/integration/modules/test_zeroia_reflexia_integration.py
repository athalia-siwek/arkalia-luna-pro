from modules.zeroia.reason_loop import decide


def test_decide_emergency_from_reflexia() -> None:
    ctx = {
        "status": {"cpu": 51.1, "severity": "critical"},
        "reflexia": {"last_snapshot": "🛑 surcharge CPU"},
    }
    assert decide(ctx)[0] == "emergency_shutdown"
