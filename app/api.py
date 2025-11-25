from src.account_registery import AccountRegistery
from src.personal_account import PersonalAccount
from flask import Flask, request, jsonify

app = Flask(__name__)
registry = AccountRegistery()

@app.route("/api/create_account", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.return_accounts_list()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=["GET"])
def count_all_accounts():
    print("Counting all accounts in registery")
    count = registry.return_register_length()
    return jsonify({"length": count}), 200


@app.route("/api/accounts/<pesel>", methods=["GET"])
def find_by_pesel(pesel):
    account = registry.find_by_id_number(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404

    account_data = {
        "name": account.first_name,
        "surname": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance
    }
    return jsonify(account_data), 200


@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json() or {}
    name = data.get("name")
    surname = data.get("surname")

    update = registry.update_account_by_id(pesel, name, surname)
    if not update:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    delete = registry.delete_account_by_id(pesel)
    if not delete:
        return jsonify({"message": "Account not found"}), 404
    
    return jsonify({"message": "Account deleted"}), 200