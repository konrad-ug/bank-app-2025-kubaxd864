import datetime
from lib.smtp import SMTPClient

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
    
    def send_history_via_email(self, email_address):
        from src.personal_account import PersonalAccount
        from src.company_account import CompanyAccount
        aktualna_data = datetime.date.today().isoformat()
        historia = ", ".join(str(x) for x in self.history)
        title = f"Account Transfer History {aktualna_data}"
        if isinstance(self, PersonalAccount):
            body = f"Personal account history: {historia.__str__()}"
        elif isinstance(self, CompanyAccount):
            body = f"Company account history: {historia.__str__()}"
        else:
            return False
        return SMTPClient.send(title, body, email_address)

