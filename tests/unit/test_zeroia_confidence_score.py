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


def test_decide_reduce_load_edge_case():
    ctx = {"status": {"cpu": 85, "severity": "warning"}}
    decision, score = reason_loop.decide(ctx)
    assert decision == "reduce_load"
    assert score == 0.75


def test_decide_halt_edge_case():
    ctx = {"status": {"cpu": 95, "severity": "critical"}}
    decision, score = reason_loop.decide(ctx)
    assert decision == "reduce_load"
    assert score == 0.75


def test_decide_reboot_logic_edge_case():
    ctx = {"status": {"cpu": 50, "severity": "none"}}
    decision, score = reason_loop.decide(ctx)
    assert decision == "normal"
    assert score == 0.4
