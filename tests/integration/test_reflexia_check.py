# /Volumes/T7/devstation/cursor/arkalia-luna-pro/tests/integration/
# test_reflexia_check.py

from fastapi.testclient import TestClient

from helloria.core import app

client = TestClient(app)


def test_reflexia_check():
    response = client.get("/reflexia/check")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "metrics" in data
    assert isinstance(data["metrics"], dict)
    assert "cpu" in data["metrics"]
    assert "ram" in data["metrics"]
