# modules/reflexia/tests/test_reflexia.py

from modules.reflexia.core import monitor_status


def test_monitor_status():
    assert monitor_status({"cpu": 95}) == "🛑 surcharge CPU"
    assert monitor_status({"memory": 85}) == "⚠️ haute mémoire"
    assert monitor_status({"cpu": 30, "memory": 40}) == "✅ stable"
