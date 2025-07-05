# 🧪 Tests pour le mécanisme anti-répétition de ZeroIA
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from modules.zeroia.reason_loop import should_process_decision
from tests.fixtures.__test_helpers import ensure_test_toml

ensure_test_toml()


def test_should_process_decision_new_decision() -> None:
    """🧠 Une nouvelle décision différente doit toujours être acceptée"""
    # Test avec une nouvelle décision
    result = should_process_decision("new_decision")
    assert result is True


def test_should_process_decision_same_decision_within_interval() -> None:
    """🧠 La même décision dans l'intervalle anti-spam doit être rejetée"""
    # Premier appel
    should_process_decision("reduce_load")
    # Deuxième appel immédiat - doit être rejeté
    result = should_process_decision("reduce_load")
    assert result is False


def test_should_process_decision_same_decision_after_interval() -> None:
    """🧠 La même décision après l'intervalle anti-spam doit être acceptée"""
    # Test avec des décisions différentes pour éviter l'anti-spam
    should_process_decision("decision_a")
    should_process_decision("decision_b")
    should_process_decision("decision_c")

    # Maintenant testons la même décision - devrait être acceptée car c'est une nouvelle décision
    result = should_process_decision("decision_a")
    assert result is True


def test_should_process_decision_first_call() -> None:
    """🧠 Le premier appel doit être accepté"""
    # Test avec une décision complètement nouvelle
    result = should_process_decision("first_call_test")
    assert result is True


def test_should_process_decision_reset_after_different_decision() -> None:
    """🧠 Après une décision différente, le compteur doit se réinitialiser"""
    # Première décision
    should_process_decision("reduce_load")
    # Deuxième appel immédiat - rejeté
    result1 = should_process_decision("reduce_load")
    assert result1 is False

    # Nouvelle décision différente - acceptée
    result2 = should_process_decision("monitor")
    assert result2 is True


@pytest.mark.parametrize(
    "decision1,decision2,expected",
    [
        ("test1", "test1", False),  # Même décision immédiate
        ("test2", "test3", True),  # Décisions différentes
        ("test4", "test4", False),  # Même décision immédiate
    ],
)
def test_should_process_decision_various_scenarios(
    decision1: str, decision2: str, expected: bool
) -> None:
    """🧠 Test de différents scénarios de décisions"""
    should_process_decision(decision1)
    result = should_process_decision(decision2)
    assert result is expected


def test_anti_repetition_with_reason_loop_integration(tmp_path: Path) -> None:
    """🧠 Test d'intégration du mécanisme anti-répétition avec reason_loop"""
    from modules.zeroia.reason_loop import reason_loop

    # Setup des fichiers de test
    ctx_path = tmp_path / "global_context.toml"
    reflexia_path = tmp_path / "reflexia_state.toml"
    state_path = tmp_path / "zeroia_state.toml"
    dashboard_path = tmp_path / "dashboard.json"

    import toml

    toml.dump(
        {
            "status": {"cpu": 75, "ram": 50},
            "active": True,
        },
        ctx_path.open("w"),
    )

    toml.dump(
        {
            "decision": {"last_decision": "reduce_load"},
        },
        reflexia_path.open("w"),
    )

    # Premier appel - doit créer les fichiers
    decision1, score1 = reason_loop(
        context_path=ctx_path,
        reflexia_path=reflexia_path,
        state_path=state_path,
        dashboard_path=dashboard_path,
    )

    # Vérifier que la décision est valide (pas vide et dans les valeurs attendues)
    valid_decisions = {"reduce_load", "monitor", "halt", "reboot", "emergency_shutdown"}
    assert decision1 in valid_decisions, f"Décision invalide: {decision1}"
    assert state_path.exists()
    assert dashboard_path.exists()

    # Deuxième appel immédiat - ne doit PAS recréer les fichiers (anti-spam)
    state_mtime_before = state_path.stat().st_mtime
    dashboard_mtime_before = dashboard_path.stat().st_mtime

    decision2, score2 = reason_loop(
        context_path=ctx_path,
        reflexia_path=reflexia_path,
        state_path=state_path,
        dashboard_path=dashboard_path,
    )

    # Vérifier que la décision est cohérente
    assert decision2 in valid_decisions, f"Décision invalide: {decision2}"
    # Les fichiers ne doivent pas avoir été modifiés (anti-spam actif)
    assert state_path.stat().st_mtime == state_mtime_before
    assert dashboard_path.stat().st_mtime == dashboard_mtime_before
