import sys
from pathlib import Path

import pytest

# ✅ Forcer ajout de la racine du projet dans sys.path AVANT les autres imports
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from tests.fixtures.test_helpers import ensure_test_toml
except ImportError:
    # fallback pour appel direct
    pass


@pytest.fixture(autouse=True, scope="session")
def ensure_state_file() -> None:
    """
    Fixture auto-injectée : crée le fichier TOML global pour tous les tests.
    """
    ensure_test_toml()
