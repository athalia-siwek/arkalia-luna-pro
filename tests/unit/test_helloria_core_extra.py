from modules.helloria.core import app


def test_status_endpoint_exists():
    assert app is not None