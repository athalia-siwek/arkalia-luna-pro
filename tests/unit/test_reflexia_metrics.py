from modules.reflexia.logic.metrics import read_metrics


def test_read_metrics_returns_expected_keys():
    metrics = read_metrics()
    assert all(key in metrics for key in ["cpu", "ram", "latency"])
    assert isinstance(metrics["cpu"], float)