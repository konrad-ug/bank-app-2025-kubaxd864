class Account:
    def __init__(self):
        self.history = []

    def incoming_transfer(self, kwota):
        if str(kwota).isdigit() and kwota >= 0:
            self.balance += kwota
            self.history.append(kwota)
        return self.balance

    def outgoing_transfer(self, kwota, transfer_type = "standard"):
        from src.personal_account import PersonalAccount
        from src.company_account import CompanyAccount
        if str(kwota).isdigit() and kwota >= 0 and self.balance >= kwota:
            self.balance -= kwota
            self.history.append(-kwota)
        if transfer_type == "fast" and isinstance(self, CompanyAccount): 
            self.balance -= 5
            self.history.append(-5)
        elif transfer_type == "fast" and isinstance(self, PersonalAccount):
            self.balance -= 1
            self.history.append(-1)
        return self.balance
