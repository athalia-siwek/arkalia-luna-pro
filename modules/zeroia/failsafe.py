import shutil
from datetime import datetime
from pathlib import Path

import toml

SNAPSHOT_PATH = Path("state/zeroia_snapshot.toml")
BACKUP_PATH = Path("state/zeroia_snapshot_backup.toml")
FAILURE_LOG = Path("logs/failure_analysis.md")


def load_snapshot(path) -> None:
    try:
        return toml.load(path)
    except Exception as e:
        log_failure(f"Erreur de lecture du snapshot {path.name}: {str(e)}")
        return None


def log_failure(reason) -> None:
    FAILURE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(FAILURE_LOG, "a") as f:
        f.write(f"## 🛑 Échec détecté : {datetime.now().isoformat()}\n")
        f.write(f"**Raison :** {reason}\n\n")


def restore_backup() -> None:
    if BACKUP_PATH.exists():
        shutil.copy(BACKUP_PATH, SNAPSHOT_PATH)
        log_failure("Backup restauré avec succès.")
        return True
    else:
        log_failure("Aucun backup disponible pour restauration.")
        return False


def failsafe_mode() -> None:
    print("🛡️ Activation du mode Failsafe ZeroIA…")
    snapshot = load_snapshot(SNAPSHOT_PATH)

    if snapshot is None or "decision" not in snapshot:
        print("⚠️ Snapshot corrompu ou incomplet. Tentative de restauration…")
        success = restore_backup()
        if success:
            print("✅ Restauration réussie.")
        else:
            print("❌ Aucune restauration possible. " "ZeroIA doit être relancé manuellement.")
    else:
        print("✅ Snapshot valide. Aucun failsafe nécessaire.")


if __name__ == "__main__":
    failsafe_mode()
