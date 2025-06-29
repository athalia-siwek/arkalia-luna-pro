from modules.zeroia.reason_loop import decide


def test_decide_with_high_cpu_and_threshold() -> None:
    ctx = {"status": {"cpu": 75, "severity": "none"}}
    decision, score = decide(ctx)
    assert decision == "reduce_load"
    assert score == 0.75
