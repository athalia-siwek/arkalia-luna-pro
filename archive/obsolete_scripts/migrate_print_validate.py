from typing import Any


def validate_migration(
    audit_data: dict[str, Any], migration_results: dict[str, Any]
) -> dict[str, Any]:
    """Valide la migration et génère un rapport."""
    validation = {
        "total_original": 0,
        "total_migrated": 0,
        "total_excluded": 0,
        "errors": [],
        "warnings": [],
        "success_rate": 0.0,
    }

    # Compter les originaux
    for _file_path, prints in audit_data["audit"]["files"].items():
        validation["total_original"] += len(prints)

    # Compter les migrés
    validation["total_migrated"] = len(migration_results.get("migrated", []))
    validation["total_excluded"] = len(migration_results.get("excluded", []))

    # Calculer le taux de succès
    if validation["total_original"] > 0:
        validation["success_rate"] = (
            validation["total_migrated"] / validation["total_original"]
        ) * 100

    return validation
