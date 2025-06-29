def should_adjust_thresholds(log):
    return all(entry["output"] == log[0]["output"] for entry in log)


def test_zeroia_consistency_check():
    log = [{"output": "monitor"}, {"output": "monitor"}, {"output": "monitor"}]
    assert should_adjust_thresholds(log) is True
