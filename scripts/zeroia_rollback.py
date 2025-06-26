#!/usr/bin/env python3
# 🔄 ZeroIA Rollback — Arkalia LUNA v2.6.x

import shutil
from datetime import datetime
from pathlib import Path

STATE_FILE = Path("modules/zeroia/state/zeroia_state.toml")
SNAPSHOT_FILE = Path("modules/zeroia/state/zeroia_state_snapshot.toml")
BACKUP_FILE = Path("modules/zeroia/state/zeroia_state_backup.toml")
LOG_FILE = Path("logs/zeroia_rollback.log")


def backup_current_state():
    if STATE_FILE.exists():
        shutil.copy(STATE_FILE, BACKUP_FILE)
        print(f"🗄️  Backup du fichier actuel effectué : {BACKUP_FILE}")


def restore_snapshot():
    if not SNAPSHOT_FILE.exists():
        print("❌ Aucun fichier snapshot à restaurer.")
        return False

    shutil.copy(SNAPSHOT_FILE, STATE_FILE)
    print("✅ Snapshot restauré dans zeroia_state.toml")
    return True


def log_failure():
    log_file = Path("logs/failure_analysis.md")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as f:
        f.write("\n")
        f.write(f"## 🛑 Échec détecté : {datetime.now().isoformat()}\n")
        f.write("**Raison :** Restauration du snapshot ZeroIA exécutée manuellement.\n")


def log(msg: str):
    with LOG_FILE.open("a") as f:
        f.write(f"[rollback] {msg}\n")


def rollback():
    if not BACKUP_FILE.exists():
        log("❌ Aucune sauvegarde trouvée.")
        print("❌ Rollback impossible : pas de backup.")
        return

    try:
        shutil.copy2(BACKUP_FILE, STATE_FILE)
        log("✅ Rollback effectué depuis backup.")
        print("✅ Rollback effectué depuis backup.")
    except Exception as e:
        log(f"❌ Erreur rollback : {e}")
        print(f"❌ Rollback échoué : {e}")


if __name__ == "__main__":
    backup_current_state()
    if restore_snapshot():
        log_failure()
    rollback()
