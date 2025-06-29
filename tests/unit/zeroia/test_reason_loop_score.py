import pytest

from modules.zeroia.reason_loop import compute_confidence_score


@pytest.mark.unit
def test_confidence_score_high_success_low_error():
    result = compute_confidence_score(success_rate=0.9, error_rate=0.05)
    assert 0.8 <= result <= 1.0, f"Score trop bas : {result}"


@pytest.mark.unit
def test_confidence_score_mixed_success_and_error():
    result = compute_confidence_score(success_rate=0.5, error_rate=0.5)
    assert 0.0 <= result <= 0.5, f"Score hors limites : {result}"


@pytest.mark.unit
def test_confidence_score_zero_success_low_error():
    result = compute_confidence_score(success_rate=0.0, error_rate=0.1)
    assert 0.0 <= result < 0.1, f"Score inattendu : {result}"


@pytest.mark.unit
def test_confidence_score_zero_success_high_error():
    result = compute_confidence_score(success_rate=0.0, error_rate=1.0)
    assert result == 0.0, f"Score devrait être 0, reçu : {result}"


@pytest.mark.unit
def test_confidence_score_perfect():
    result = compute_confidence_score(success_rate=1.0, error_rate=0.0)
    assert result == 1.0, f"Score parfait attendu, reçu : {result}"
