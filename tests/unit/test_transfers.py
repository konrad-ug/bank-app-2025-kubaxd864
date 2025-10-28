from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


class TestTransfers:
    def test_balance_add(self):
        account = PersonalAccount("John", "Doe", "61352353511", "PROM_2025")
        account.incoming_transfer(100)
        assert account.balance == 150

    def test_add_negative_balance(self):
        account = PersonalAccount("John", "Doe", "75352353511", "PROM_2025")
        account.incoming_transfer(-100)
        assert account.balance == 50

    def test_add_string_balance(self):
        account = PersonalAccount("John", "Doe", "75352353511", "PROM_2025")
        account.incoming_transfer("XD")
        assert account.balance == 50

    def test_balance_send(self):
        account = PersonalAccount("John", "Doe", "61352353511", "PROM_2025")
        account.outgoing_transfer(20)
        assert account.balance == 30

    def test_send_negative_balance(self):
        account = PersonalAccount("John", "Doe", "75352353511", "PROM_2025")
        account.outgoing_transfer(-100)
        assert account.balance == 50

    def test_send_perfect_amount(self):
        account = PersonalAccount("John", "Doe", "75352353511", "PROM_2025")
        account.outgoing_transfer(50)
        assert account.balance == 0

    def test_send_string_balance(self):
        account = PersonalAccount("John", "Doe", "75352353511", "PROM_2025")
        account.outgoing_transfer("XD")
        assert account.balance == 50

    def test_balance_add_CompanyAcc(self):
        account = CompanyAccount("Firma1", "3423454333")
        account.incoming_transfer(1205)
        assert account.balance == 1205

    def test_balance_send_CompanyAcc(self):
        account = account = CompanyAccount("Firma2", "3411454333")
        account.balance = 200
        account.outgoing_transfer(30)
        assert account.balance == 170

    def test_fast_transfer_personal(self):
        account = PersonalAccount("John", "Doe", "75352353511", "PROM_2025")
        account.outgoing_transfer(20, "fast")
        assert account.balance == 29

    def test_fast_transfer_company(self):
        account = CompanyAccount("Firma2", "3411454333")
        account.balance = 2000
        account.outgoing_transfer(1599, "fast")
        assert account.balance == 396

    def test_fast_transfer_negative_balance(self):
        account = PersonalAccount("John", "Doe", "75352353511", "PROM_2025")
        account.outgoing_transfer(50, "fast")
        assert account.balance == -1

    def test_fast_transfer_negative_balance_company(self):
        account = CompanyAccount("Firma5", "3416755433")
        account.balance = 500
        account.outgoing_transfer(498, "fast")
        assert account.balance == -3

    def test_balance_history_normal_transfer_personal(self):
        account = PersonalAccount("John", "Doe", "61352353511")
        account.incoming_transfer(500)
        account.outgoing_transfer(300)
        assert account.history == [500, -300]
    
    def test_balance_history_normal_transfer_company(self):
        account = CompanyAccount("Firma5", "3416755433")
        account.incoming_transfer(1000)
        account.outgoing_transfer(550)
        assert account.history == [1000, -550]

    def test_balance_history_fast_transfer_personal(self):
        account = PersonalAccount("John", "Doe", "61352353511")
        account.incoming_transfer(200)
        account.outgoing_transfer(50, "fast")
        assert account.history == [200, -50, -1]
    
    def test_balance_history_fast_transfer_company(self):
        account = CompanyAccount("Firma5", "3416755433")
        account.incoming_transfer(550)
        account.outgoing_transfer(250, "fast")
        assert account.history == [550, -250, -5]