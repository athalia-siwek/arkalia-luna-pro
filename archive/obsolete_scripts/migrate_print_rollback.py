from typing import Any


def analyze_rollback_needs(audit_data: dict[str, Any]) -> dict[str, Any]:
    """Analyse les besoins de rollback."""
    rollback_analysis = {
        "critical_files": [],
        "safe_files": [],
        "rollback_strategy": "selective",
    }

    for _file_path, prints in audit_data["audit"]["files"].items():
        has_critical = any(p["criticality"] == "HIGH" for p in prints)
        if has_critical:
            rollback_analysis["critical_files"].append(_file_path)
        else:
            rollback_analysis["safe_files"].append(_file_path)

    return rollback_analysis
