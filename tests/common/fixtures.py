# 📄 tests/common/fixtures.py
# Fixtures partagées pour tous les tests

from pathlib import Path

import pytest

from .helpers import ensure_test_toml, ensure_zeroia_state_file


@pytest.fixture(scope="session")
def test_data_dir():
    """Répertoire temporaire pour les données de test."""
    return Path("tests/data")


@pytest.fixture(scope="session")
def mock_config():
    """Configuration de test standard."""
    return {"test_mode": True, "debug": True, "timeout": 5}


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup automatique de l'environnement de test."""
    ensure_test_toml()
    ensure_zeroia_state_file()


@pytest.fixture
def clean_state_files():
    """Nettoie les fichiers d'état après les tests."""
    yield
    # Cleanup après les tests
    state_files = [
        "modules/zeroia/state/zeroia_state.toml",
        "state/reflexia_state.toml",
    ]
    for file_path in state_files:
        if Path(file_path).exists():
            Path(file_path).write_text("")
