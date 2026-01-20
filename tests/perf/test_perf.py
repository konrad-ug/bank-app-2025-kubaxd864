import time

ITERATIONS = 100

def test_create_and_delete_account(client):
    for i in range(ITERATIONS):
        pesel = f"99000000{i:03d}"
        account = {
            "name": "Jan",
            "surname": "Kowalski",
            "pesel": pesel
        }

        start = time.perf_counter()
        create_resp = client.post("/api/create_account", json=account)
        elapsed = time.perf_counter() - start

        assert create_resp.status_code == 201
        assert elapsed < 0.5

        start = time.perf_counter()
        delete_resp = client.delete(f"/api/accounts/{pesel}")
        elapsed = time.perf_counter() - start

        assert delete_resp.status_code == 200
        assert elapsed < 0.5

def test_100_incoming_transfers_and_balance(client):
    account = {
        "name": "Jan",
        "surname": "Kowalski",
        "pesel": "01445213311"
    }
    pesel = account["pesel"]
    create_resp = client.post(
        "/api/create_account",
        json=account,
    )
    assert create_resp.status_code == 201
    try:
        transfer_amount = 10
        expected_balance = transfer_amount * ITERATIONS
        for _ in range(ITERATIONS):
            start = time.perf_counter()
            transfer_resp = client.post(
                f"/api/account/{pesel}/transfer",
                json={
                    "type": "incoming",
                    "amount": transfer_amount
                },
            )
            elapsed = time.perf_counter() - start
            assert transfer_resp.status_code == 200
            assert elapsed < 0.5
        balance_resp = client.get(
            f"/api/accounts/{pesel}",
        )
        assert balance_resp.status_code == 200
        assert balance_resp.json["balance"] == expected_balance
    finally:
        client.delete(f"/api/accounts/{pesel}")