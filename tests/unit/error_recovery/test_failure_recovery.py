import shutil
import subprocess
import sys
from pathlib import Path

SNAPSHOT = Path("state/zeroia_snapshot.toml")
BACKUP = Path("state/zeroia_snapshot_backup.toml")
FAILURE_LOG = Path("logs/failure_analysis.md")


def setup_module(module) -> None:
    # Sauvegarde des versions originales
    if SNAPSHOT.exists():
        shutil.copy(SNAPSHOT, SNAPSHOT.with_suffix(".toml.original"))
    if BACKUP.exists():
        shutil.copy(BACKUP, BACKUP.with_suffix(".toml.original"))


def teardown_module(module) -> None:
    # Restaure les fichiers d'origine
    original_snapshot = SNAPSHOT.with_suffix(".toml.original")
    original_backup = BACKUP.with_suffix(".toml.original")
    if original_snapshot.exists():
        shutil.copy(original_snapshot, SNAPSHOT)
        original_snapshot.unlink()
    if original_backup.exists():
        shutil.copy(original_backup, BACKUP)
        original_backup.unlink()


def test_failsafe_recovers_from_corrupt_snapshot() -> None:
    # Écrit un snapshot corrompu
    with open(SNAPSHOT, "w") as f:
        f.write("::corruption::")

    # Lance le script failsafe
    result = subprocess.run(
        [sys.executable, "modules/zeroia/failsafe.py"],
        capture_output=True,
        text=True,
        check=True,
        shell=False,
    )

    assert "⚠️ Snapshot corrompu ou incomplet" in result.stdout
    assert FAILURE_LOG.exists()

    with open(FAILURE_LOG) as f:
        content = f.read()
        assert "Backup restaur\u00e9" in content or "Aucun backup disponible" in content
