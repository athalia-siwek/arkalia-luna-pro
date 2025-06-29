# 📄 tests/unit/test_zeroia_reason_loop_emergency.py

from modules.zeroia.reason_loop import decide


def test_decide_emergency_shutdown() -> None:
    ctx = {"status": {"cpu": 20, "severity": "critical"}}
    decision, score = decide(ctx)
    assert decision == "emergency_shutdown"
    assert score == 1.0
