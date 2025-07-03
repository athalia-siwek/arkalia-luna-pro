from typing import Any


def migrate_high_prints(audit_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Extrait les print() critiques pour migration Phase 3 (très future)."""
    high_prints = []

    for _file_path, prints in audit_data["audit"]["files"].items():
        for print_info in prints:
            if print_info["criticality"] == "HIGH":
                high_prints.append(print_info)

    return high_prints
