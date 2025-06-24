from modules.zeroia import reason_loop


def test_confidence_scores():
    ctx = {"status": {"cpu": 91}}
    decision, score = reason_loop.decide(ctx)
    assert decision == "reduce_load"
    assert score == 0.75

    ctx = {"status": {"cpu": 45}}
    decision, score = reason_loop.decide(ctx)
    assert decision == "normal"
    assert score == 0.4
