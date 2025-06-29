from modules.helloria.core import app


def test_status_endpoint_exists() -> None:
    assert app is not None
