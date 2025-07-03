from app import main


def test_main_launchable() -> None:
    assert callable(main.print_status)
