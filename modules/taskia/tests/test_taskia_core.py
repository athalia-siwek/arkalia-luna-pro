from modules.taskia.core import taskia_main


def test_taskia_main_basic():
    context = {"reflexia": "ok", "zeroia": "alert"}
    summary = taskia_main(context)
    assert "reflexia" in summary
    assert "zeroia" in summary
