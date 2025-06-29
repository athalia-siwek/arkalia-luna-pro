import shutil
from pathlib import Path

STATE_PATH = Path("modules/zeroia/state/zeroia_state.toml")
BACKUP_PATH = Path("modules/zeroia/state/zeroia_state_backup.toml")


def save_backup() -> None:
    if STATE_PATH.exists():
        shutil.copy2(STATE_PATH, BACKUP_PATH)
        print("🧪 Backup auto effectué.")
    else:
        print("⚠️ Aucun fichier d'état à sauvegarder.")
