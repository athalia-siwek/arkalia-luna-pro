from modules.zeroia import adaptive_thresholds


def test_should_lower_cpu_threshold():
    # Simule 9 décisions "monitor"
    adaptive_thresholds.LOG_PATH.write_text(
        """
[[decisions]]
output = "monitor"
[[decisions]]
output = "monitor"
[[decisions]]
output = "monitor"
[[decisions]]
output = "monitor"
[[decisions]]
output = "monitor"
[[decisions]]
output = "monitor"
[[decisions]]
output = "monitor"
[[decisions]]
output = "monitor"
[[decisions]]
output = "monitor"
[[decisions]]
output = "normal"
"""
    )
    assert adaptive_thresholds.should_lower_cpu_threshold() is True
