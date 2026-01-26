from pymongo import MongoClient
from src.personal_account import PersonalAccount

class MongoAccountsRepository():
    def __init__(self):
        self.client = MongoClient('mongodb://admin:password@localhost:27017/')
        self.db = self.client.bank_app
        self.collection = self.db.accounts

    def save_all(self, accounts):
        self.collection.delete_many({})
        data_to_insert = []
        for account in accounts:
            data_to_insert.append({
                "first_name": account.first_name,
                "last_name": account.last_name,
                "pesel": account.pesel,
                "balance": account.balance,
                "history": account.history
            })
        if data_to_insert:
            self.collection.insert_many(data_to_insert)

    def load_all(self):
        accounts_data = self.collection.find()
        accounts = []
        for data in accounts_data:
            acc = PersonalAccount(data["first_name"], data["last_name"], data["pesel"], balance=data["balance"])
            acc.history = data.get("history", [])
            accounts.append(acc)
        return accounts