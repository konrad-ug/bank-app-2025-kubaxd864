from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code = None, balance = 0):
        self.history = []
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 50 if self.is_older_than_60(pesel) and self.is_promo_code_valid(promo_code) else balance
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"

    def is_pesel_valid(self, pesel):
        if len(pesel) == 11 and pesel.isdigit():
            return True
        return False
    
    def is_promo_code_valid(self, promo_code):
        if promo_code is None:
            return False
        if promo_code.startswith("PROM_") and len(promo_code) == 9:
            return True
        return 
    
    def is_older_than_60(self, pesel):
        if pesel.isdigit() and int(pesel[:2]) > 60:
            return True
        elif pesel.isdigit() and int(pesel[2:4]) > 21 and int(pesel[2:4]) < 32:
            return True
        return False