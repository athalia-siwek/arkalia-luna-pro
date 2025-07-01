from typing import Any


def generate_test_plan(audit_data: dict[str, Any]) -> dict[str, Any]:
    """Génère un plan de tests pour la migration."""
    test_plan = {
        "unit_tests": [],
        "integration_tests": [],
        "regression_tests": [],
        "total_test_cases": 0,
    }

    for _file_path, prints in audit_data["audit"]["files"].items():
        for print_info in prints:
            if print_info["criticality"] in ["LOW", "MEDIUM"]:
                test_plan["unit_tests"].append(
                    {"file": _file_path, "line": print_info["line"], "test_type": "unit"}
                )
                test_plan["total_test_cases"] += 1

    return test_plan
