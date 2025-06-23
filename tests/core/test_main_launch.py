from app import main


def test_main_launchable():
    assert callable(main.print_status)
