from modules.reflexia.logic.decision import monitor_status


def test_monitor_status_critical_cpu() -> None:
    assert monitor_status({"cpu": 95, "ram": 50, "latency": 100}) == "🛑 surcharge CPU"


def test_monitor_status_degraded_latency() -> None:
    assert monitor_status({"cpu": 40, "ram": 30, "latency": 350}) == "degraded"


def test_monitor_status_ok() -> None:
    assert monitor_status({"cpu": 20, "ram": 20, "latency": 100}) == "ok"
