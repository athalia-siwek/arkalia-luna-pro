import sys
from pathlib import Path

import pytest

try:
    from tests.unit.test_helpers import ensure_test_toml
except ImportError:
    # fallback pour appel direct
    from unit.test_helpers import ensure_test_toml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ✅ Forcer ajout de la racine du projet dans sys.path AVANT les autres imports
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True, scope="session")
def ensure_state_file():
    """
    Fixture auto-injectée : crée le fichier TOML global pour tous les tests.
    """
    ensure_test_toml()
