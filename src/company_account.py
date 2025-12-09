from src.account import Account
import requests
import datetime

class CompanyAccount(Account):
    def __init__(self, company_name, nip_number, balance = 0):
        self.history = []
        self.company_name = company_name
        if not self.is_nip_number_valid(nip_number):
            raise ValueError("Nr NIP nie jest poprawny")
        self.nip_number = nip_number
        self.balance = balance

    def is_nip_number_valid(self, nip_number):
        if nip_number.isdigit() and len(nip_number) == 10:
            aktualna_data = datetime.date.today().isoformat() 
            BANK_APP_MF_URL = f"https://wl-api.mf.gov.pl/api/search/nip/{nip_number}?date={aktualna_data}"
            response = requests.get(BANK_APP_MF_URL)
            data = response.json()
            code = data.get("code")
            if code == "WL-115":
                return False

            subject = data.get("result", {}).get("subject")
            if subject is None:
                return False
            
            return subject.get("statusVat") == "Czynny"
        return False
    
    def take_loan(self, amount):
        accepted = False

        if(self.balance * 2 >= amount and -1775 in self.history):
            accepted = True

        if(accepted):
            self.balance += amount
            return True
        
        return False

account = CompanyAccount("MojaFirma", "8461627563", balance=1000)
print("NIP:", account.nip_number)
print("Saldo początkowe:", account.balance)