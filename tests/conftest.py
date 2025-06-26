import sys
from pathlib import Path

import pytest

from tests.unit.test_helpers import ensure_test_toml  # ✅ toujours en premier

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(autouse=True, scope="session")
def ensure_state_file():
    """
    Fixture auto-injectée : crée le fichier TOML global pour tous les tests.
    """
    ensure_test_toml()
