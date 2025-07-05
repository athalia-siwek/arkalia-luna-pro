"""
Module failsafe.

Ce module fait partie du système Arkalia Luna Pro.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import toml

SNAPSHOT_PATH = Path("state/zeroia_snapshot.toml")
BACKUP_PATH = Path("state/zeroia_snapshot_backup.toml")
FAILURE_LOG = Path("logs/failure_analysis.md")


def load_snapshot(snapshot_path: str) -> dict[str, Any] | None:
    try:
        with open(snapshot_path) as f:
            data = toml.load(f)
            return data if isinstance(data, dict) else None
    except FileNotFoundError:
        return None
    except Exception:
        return None


def log_failure(error_message: str, log_file: str = "logs/failsafe_errors.log") -> None:
    try:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().isoformat()
        with open(log_path, "a") as f:
            f.write(f"[{timestamp}] {error_message}\n")
    except Exception:
        pass  # Ignore les erreurs d'écriture


def restore_backup(backup_path: str, target_path: str) -> bool:
    try:
        shutil.copy2(backup_path, target_path)
        return True
    except Exception:
        return False


def create_backup(source_path: str, backup_dir: str = "backups") -> str | None:
    try:
        source = Path(source_path)
        if not source.exists():
            return None

        backup_path = (
            Path(backup_dir)
            / f"{source.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{source.suffix}"
        )
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source, backup_path)
        return str(backup_path)
    except Exception:
        return None


def log_success(message: str, log_file: str = "logs/failsafe_success.log") -> None:
    try:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().isoformat()
        with open(log_path, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass  # Ignore les erreurs d'écriture


def rollback_system(snapshot_path: str, target_path: str) -> bool:
    try:
        # Créer un backup avant rollback
        backup_path = create_backup(target_path)
        if not backup_path:
            log_failure(f"Impossible de créer un backup avant rollback de {target_path}")
            return False

        # Restaurer le snapshot
        success = restore_backup(snapshot_path, target_path)
        if success:
            log_success(f"Rollback réussi de {target_path} depuis {snapshot_path}")
        else:
            log_failure(f"Échec du rollback de {target_path} depuis {snapshot_path}")

        return success
    except Exception as e:
        log_failure(f"Erreur lors du rollback: {str(e)}")
        return False


def failsafe_mode() -> None:
    """
    Fonction failsafe_mode.

    Cette fonction fait partie du système Arkalia Luna Pro.
    """
    print("Mode Failsafe Activation du mode Failsafe ZeroIA…")
    snapshot = load_snapshot(str(SNAPSHOT_PATH))

    if snapshot is None or "decision" not in snapshot:
        print("⚠️ Snapshot corrompu ou incomplet. Tentative de restauration…")
        success = restore_backup(str(BACKUP_PATH), str(SNAPSHOT_PATH))
        if success:
            print("✅ Restauration réussie.")
        else:
            print("❌ Aucune restauration possible. ZeroIA doit être relancé manuellement.")
    else:
        print("✅ Snapshot valide. Aucun failsafe nécessaire.")


if __name__ == "__main__":
    failsafe_mode()
