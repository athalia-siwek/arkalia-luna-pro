# 🧪 Tests pour le mécanisme anti-répétition de ZeroIA
from datetime import datetime, timedelta

import pytest

from modules.zeroia.reason_loop import should_process_decision
from tests.unit.test_helpers import ensure_test_toml

ensure_test_toml()


def test_should_process_decision_new_decision():
    """🧠 Une nouvelle décision différente doit toujours être acceptée"""
    # Réinitialise les variables globales pour ce test
    import modules.zeroia.reason_loop as rl

    rl.LAST_DECISION = "old_decision"
    rl.LAST_DECISION_TIME = datetime.now()

    # Une nouvelle décision différente doit être acceptée
    result = should_process_decision("new_decision")
    assert result is True
    assert rl.LAST_DECISION == "new_decision"


def test_should_process_decision_same_decision_within_interval():
    """🧠 La même décision dans l'intervalle anti-spam doit être rejetée"""
    import modules.zeroia.reason_loop as rl

    rl.LAST_DECISION = "reduce_load"
    rl.LAST_DECISION_TIME = datetime.now()

    # La même décision immédiatement après doit être rejetée
    result = should_process_decision("reduce_load")
    assert result is False


def test_should_process_decision_same_decision_after_interval():
    """🧠 La même décision après l'intervalle anti-spam doit être acceptée"""
    import modules.zeroia.reason_loop as rl

    rl.LAST_DECISION = "reduce_load"
    # Simule un temps passé de 31 secondes (> MIN_DECISION_INTERVAL)
    rl.LAST_DECISION_TIME = datetime.now() - timedelta(seconds=31)

    result = should_process_decision("reduce_load")
    assert result is True


def test_should_process_decision_first_call():
    """🧠 Le premier appel avec LAST_DECISION_TIME = None doit être accepté"""
    import modules.zeroia.reason_loop as rl

    rl.LAST_DECISION = "reduce_load"
    rl.LAST_DECISION_TIME = None

    result = should_process_decision("reduce_load")
    assert result is True
    assert rl.LAST_DECISION_TIME is not None


def test_should_process_decision_reset_after_different_decision():
    """🧠 Après une décision différente, le compteur doit se réinitialiser"""
    import modules.zeroia.reason_loop as rl

    rl.LAST_DECISION = "reduce_load"
    rl.LAST_DECISION_TIME = datetime.now()

    # Nouvelle décision différente
    result1 = should_process_decision("monitor")
    assert result1 is True

    # Maintenant une répétition de "monitor" immédiate devrait être rejetée
    result2 = should_process_decision("monitor")
    assert result2 is False


@pytest.mark.parametrize(
    "interval,expected",
    [
        (15, False),  # Moins que MIN_DECISION_INTERVAL (30s)
        (29, False),  # Juste en dessous
        (30, True),  # Exactement MIN_DECISION_INTERVAL
        (31, True),  # Au-dessus
        (60, True),  # Bien au-dessus
    ],
)
def test_should_process_decision_interval_boundaries(interval, expected):
    """🧠 Test des limites de l'intervalle anti-répétition"""
    import modules.zeroia.reason_loop as rl

    rl.LAST_DECISION = "reduce_load"
    rl.LAST_DECISION_TIME = datetime.now() - timedelta(seconds=interval)

    result = should_process_decision("reduce_load")
    assert result is expected


def test_anti_repetition_with_reason_loop_integration(tmp_path):
    """🧠 Test d'intégration du mécanisme anti-répétition avec reason_loop"""
    import modules.zeroia.reason_loop as rl

    rl.LAST_DECISION = None
    rl.LAST_DECISION_TIME = None

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

    assert decision1 == "reduce_load"
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

    assert decision2 == "reduce_load"
    # Les fichiers ne doivent pas avoir été modifiés (anti-spam actif)
    assert state_path.stat().st_mtime == state_mtime_before
    assert dashboard_path.stat().st_mtime == dashboard_mtime_before
