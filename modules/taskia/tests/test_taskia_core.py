from modules.taskia.core import taskia_main


def test_taskia_main_basic() -> None:
    context = {"reflexia": "ok", "zeroia": "alert"}
    summary = taskia_main(context)
    if "reflexia" not in summary:
        raise AssertionError('"reflexia" not found in summary')
    if "zeroia" not in summary:
        raise AssertionError('"zeroia" not found in summary')
