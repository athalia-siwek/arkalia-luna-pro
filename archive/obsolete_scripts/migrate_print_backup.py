from typing import Any


def create_backup_plan(audit_data: dict[str, Any]) -> dict[str, Any]:
    """Crée un plan de backup pour la migration."""
    backup_plan = {
        "files_to_backup": [],
        "total_files": 0,
        "backup_strategy": "patch",
    }

    for _file_path, prints in audit_data["audit"]["files"].items():
        if prints:  # Si le fichier contient des print()
            backup_plan["files_to_backup"].append(_file_path)
            backup_plan["total_files"] += 1

    return backup_plan
