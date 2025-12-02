import pytest
from app.api import app, registry


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        client.post("/api/create_account", json={"name": "Anna", "surname": "Nowak", "pesel": "22222222222"})
        yield client


def test_get_account_by_id(client):
    r = client.get("/api/accounts/22222222222")
    assert r.status_code == 200


def test_get_account_by_id_not_exist(client):
    r = client.get("/api/accounts/22222222211")
    assert r.status_code == 404


def test_patch_updates_name(client):
    r = client.patch("/api/accounts/22222222222", json={"name": "Anka"})
    assert r.status_code == 200
    acc = registry.find_by_id_number("22222222222")
    assert acc.first_name == "Anka"


def test_delete_account(client):
    r = client.delete("/api/accounts/22222222222")
    assert r.status_code == 200


def test_delete_account_not_exist(client):
    r = client.delete("/api/accounts/22222222211")
    assert r.status_code == 404

def test_pesel_already_used(client):
    r = client.post("/api/create_account", json={"name": "Anna", "surname": "Nowak", "pesel": "22222222222"})
    assert r.status_code == 409

def test_transfer_account_not_found(client):
    r = client.post("/api/account/22222222211/transfer", json={"amount": 500, "type": "incoming"})
    assert r.status_code == 404

def test_transfer_incorrect_type(client):
    r = client.post("/api/account/22222222222/transfer", json={"amount": 500, "type": "incomingg"})
    assert r.status_code == 405

def test_transfer_incorrect_amount_type(client):
    r = client.post("/api/account/22222222222/transfer", json={"amount": "500", "type": "incoming"})
    assert r.status_code == 400

def test_transfer_incoming(client):
    r = client.post("/api/account/22222222222/transfer", json={"amount": 500, "type": "incoming"})
    assert r.status_code == 200

def test_transfer_ourgoing(client):
    r = client.post("/api/account/22222222222/transfer", json={"amount": 500, "type": "outgoing"})
    assert r.status_code == 200

def test_transfer_fast(client):
    r = client.post("/api/account/22222222222/transfer", json={"amount": 500, "type": "fast"})
    assert r.status_code == 200
