from typing import Any


def extract_excluded_prints(audit_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Extrait les print() exclus (json.dumps, etc.)."""
    excluded_prints = []

    for _file_path, prints in audit_data["audit"]["files"].items():
        for print_info in prints:
            if print_info["criticality"] == "EXCLUDE":
                excluded_prints.append(print_info)

    return excluded_prints
