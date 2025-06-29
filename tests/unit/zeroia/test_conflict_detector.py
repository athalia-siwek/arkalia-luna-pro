import pytest

from modules.zeroia.utils.conflict_detector import detect_conflict


@pytest.mark.unit
def test_conflict_same_key_different_values() -> None:
    dict_a = {"goal": "run"}
    dict_b = {"goal": "sleep"}
    result = detect_conflict(dict_a, dict_b)
    assert result is True, "Conflit attendu mais non détecté."


@pytest.mark.unit
def test_conflict_no_common_keys() -> None:
    dict_a = {"goal": "run"}
    dict_b = {"status": "idle"}
    result = detect_conflict(dict_a, dict_b)
    assert result is False, "Pas de conflit attendu mais un a été détecté."


@pytest.mark.unit
def test_conflict_same_key_same_value() -> None:
    dict_a = {"goal": "run"}
    dict_b = {"goal": "run"}
    result = detect_conflict(dict_a, dict_b)
    assert result is False, "Aucun conflit attendu car les valeurs sont identiques."


@pytest.mark.unit
def test_conflict_multiple_keys_with_one_conflict() -> None:
    dict_a = {"goal": "run", "mode": "auto"}
    dict_b = {"goal": "run", "mode": "manual"}
    result = detect_conflict(dict_a, dict_b)
    assert result is True, "Conflit sur 'mode' attendu mais non détecté."
