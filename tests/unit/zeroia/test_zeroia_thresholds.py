# 📄 tests/unit/test_zeroia_thresholds.py

from unittest.mock import patch

from modules.zeroia.reason_loop import decide


def test_decide_with_lower_threshold():
    """🔧 Mock should_lower_cpu_threshold pour forcer le mode reduce_load."""
    context = {"status": {"cpu": 75}}
    with patch(
        "modules.zeroia.adaptive_thresholds.should_lower_cpu_threshold",
        return_value=True,
    ):
        decision, confidence = decide(context)
        assert decision == "reduce_load"
        assert confidence == 0.75


@patch("modules.zeroia.reason_loop.should_lower_cpu_threshold", return_value=False)
def test_decide_without_lower_threshold(mock_threshold):
    """🔧 Mock should_lower_cpu_threshold pour ne pas activer le mode reduce_load."""
    context = {"status": {"cpu": 75}}
    decision, confidence = decide(context)
    assert decision == "monitor"
    assert confidence == 0.6
