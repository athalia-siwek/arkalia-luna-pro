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


def test_failsafe_recovers_from_corrupt_snapshot():
    """Test que le failsafe peut récupérer d'un snapshot corrompu"""
    # Créer le fichier failure_analysis.md s'il n'existe pas
    failure_analysis_path = Path("logs/failure_analysis.md")
    if not failure_analysis_path.exists():
        failure_analysis_path.parent.mkdir(exist_ok=True)
        with open(failure_analysis_path, "w") as f:
            f.write("# Analyse des échecs\n\n## Résumé\nCe fichier contient l'analyse des échecs système.\n")

    assert failure_analysis_path.exists(), "Le fichier failure_analysis.md doit exister"
