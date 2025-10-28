from src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip_number, balance = 0):
        self.history = []
        self.company_name = company_name
        self.nip_number = nip_number if self.is_nip_number_valid(nip_number) else "Niepoprawny NIP!"
        self.balance = balance

    def is_nip_number_valid(self, nip_number):
        if nip_number.isdigit() and len(nip_number) == 10:
            return True
        return False
    