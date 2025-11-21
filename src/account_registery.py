from src.personal_account import PersonalAccount

class AccountRegistery:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: PersonalAccount):
        self.accounts.append(account)

    def return_accounts_list(self):
        return self.accounts
    
    def return_register_length(self):
        return len(self.accounts)
    
    def find_by_id_number(self, id_number):
        for acc in self.accounts:
            if acc.pesel == id_number:
                return acc
        return None