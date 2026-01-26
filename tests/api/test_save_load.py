import pytest
from app.api import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_save_and_load_accounts(client):
    pesel = "99010112345"
    client.delete(f"/api/accounts/{pesel}")
    resp = client.post("/api/create_account", json={"name": "Test", "surname": "User", "pesel": pesel})
    assert resp.status_code == 201

    resp = client.post("/api/accounts/save")
    assert resp.status_code == 201

    resp = client.delete(f"/api/accounts/{pesel}")
    assert resp.status_code == 200

    resp = client.get(f"/api/accounts/{pesel}")
    assert resp.status_code == 404

    resp = client.post("/api/accounts/load")
    assert resp.status_code == 200

    resp = client.get(f"/api/accounts/{pesel}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["pesel"] == pesel
