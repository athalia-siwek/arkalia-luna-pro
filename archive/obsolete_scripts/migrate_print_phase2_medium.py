from typing import Any


def migrate_medium_prints(audit_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Extrait les print() de criticité moyenne pour migration Phase 2."""
    medium_prints = []

    for _file_path, prints in audit_data["audit"]["files"].items():
        for print_info in prints:
            if print_info["criticality"] == "MEDIUM":
                medium_prints.append(print_info)

    return medium_prints
