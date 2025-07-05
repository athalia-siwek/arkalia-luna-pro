import re
import sys
from pathlib import Path

import pytest

# ✅ Forcer ajout de la racine du projet dans sys.path AVANT les autres imports
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from tests.fixtures.__test_helpers import ensure_test_toml, restore_snapshot_if_missing
except ImportError:
    # fallback pour appel direct
    pass


@pytest.fixture(autouse=True, scope="session")
def ensure_state_file() -> None:
    """
    Fixture auto-injectée : crée le fichier TOML global pour tous les tests.
    """
    ensure_test_toml()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.failed and call.excinfo:
        msg = str(call.excinfo.value)
        # Cherche le nom du fichier manquant dans l'erreur
        match = re.search(
            r"No such file or directory: '([^']*intelligence_snapshot_[^']+\\.json)'", msg
        )
        if match:
            missing_file = Path(match.group(1)).name
            restore_snapshot_if_missing(missing_file)
