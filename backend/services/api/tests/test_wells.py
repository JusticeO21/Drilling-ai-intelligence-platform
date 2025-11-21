from fastapi.testclient import TestClient
from ..app.main import app

client = TestClient(app)


def test_get_wells():
    response = client.get("/api/v1/wells/")
    assert response.status_code == 200
    data = response.json()
    assert "wells" in data
    assert len(data["wells"]) == 3
    assert data["wells"][0]["name"] == "Well A"
    assert data["wells"][0]["depth"] == 1500.5
