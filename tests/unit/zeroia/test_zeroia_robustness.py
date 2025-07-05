from pathlib import Path

import pytest
import toml

from modules.zeroia.reason_loop import (
    check_for_ia_conflict,
    decide,
    persist_state,
    update_dashboard,
)
from tests.fixtures.__test_helpers import ensure_test_toml, ensure_zeroia_state_file

ensure_test_toml()


def test_decide_with_empty_context() -> None:
    """Test 1: Vérifie que la fonction decide() ne plante pas même si le contexte
    est vide."""
    ensure_zeroia_state_file()
    decision, score = decide({})
    assert decision == "normal"
    assert score == 0.4


def test_dashboard_and_state_write_resilience(tmp_path: Path) -> None:
    """
    Test 2: Vérifie que persist_state() et update_dashboard() écrivent
    bien les fichiers, même si le dossier est recréé à la volée.
    """
    state_path = tmp_path / "zeroia_state.toml"
    dashboard_path = tmp_path / "zeroia_dashboard.json"

    # Test direct des fonctions avec des chemins personnalisés
    persist_state("monitor", 0.6, {}, state_path_override=state_path)
    update_dashboard("monitor", 0.6, {}, dashboard_path_override=dashboard_path)

    assert state_path.exists()
    assert dashboard_path.exists()


def test_contradiction_detection_log_creation(tmp_path: Path) -> None:
    """
    Test 3: Simule une contradiction entre Reflexia et ZeroIA
    et vérifie que le fichier zeroia_contradictions.log est bien créé.
    """
    contradiction_log_path = tmp_path / "zeroia_contradictions.log"

    # Test direct de la fonction check_for_ia_conflict
    check_for_ia_conflict(
        reflexia_decision="decision1",
        zeroia_decision="decision2",
        log_path=contradiction_log_path,
    )

    assert contradiction_log_path.exists()
