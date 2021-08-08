# pylint: disable=C0114, C0116
# docs will need to be updated for this module later
from fastapi.testclient import TestClient
from .api import app

client = TestClient(app)


def test_read_main():
    response = client.get("/api/cova-demo")
    assert response.status_code == 200
