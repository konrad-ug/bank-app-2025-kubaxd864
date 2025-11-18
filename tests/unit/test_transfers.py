from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
import pytest


class TestTransfers:
    @pytest.fixture
    def account(self):
        account = PersonalAccount("John", "Doe", "61352353511")
        return account
    @pytest.mark.parametrize("pesel,promo,amount,expected", [
        ("61352353511", "PROM_2025", 100, 150),
        ("75352353511", "PROM_2025", -100, 50),
        ("75352353511", "PROM_2025", "XD", 50),
    ])
    def test_incoming_transfer_variations(self, pesel, promo, amount, expected):
        account = PersonalAccount("John", "Doe", pesel, promo)
        account.incoming_transfer(amount)
        assert account.balance == expected

    @pytest.mark.parametrize("pesel,promo,amount,expected", [
        ("61352353511", "PROM_2025", 20, 30),
        ("75352353511", "PROM_2025", -100, 50),
        ("75352353511", "PROM_2025", 50, 0),
        ("75352353511", "PROM_2025", "XD", 50),
    ])
    def test_outgoing_transfer_variations(self, pesel, promo, amount, expected):
        account = PersonalAccount("John", "Doe", pesel, promo)
        account.outgoing_transfer(amount)
        assert account.balance == expected

    def test_balance_add_CompanyAcc(self):
        account = CompanyAccount("Firma1", "3423454333")
        account.incoming_transfer(1205)
        assert account.balance == 1205

    def test_balance_send_CompanyAcc(self):
        account = account = CompanyAccount("Firma2", "3411454333")
        account.balance = 200
        account.outgoing_transfer(30)
        assert account.balance == 170

    @pytest.mark.parametrize("pesel,promo,amount,expected", [
        ("75352353511", "PROM_2025", 20, 29),
        ("75352353511", "PROM_2025", 50, -1),
    ])
    def test_fast_transfer_personal_variations(self, pesel, promo, amount, expected):
        account = PersonalAccount("John", "Doe", pesel, promo)
        account.outgoing_transfer(amount, "fast")
        assert account.balance == expected

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

    def test_balance_history_normal_transfer_personal(self, account: PersonalAccount):
        account.incoming_transfer(500)
        account.outgoing_transfer(300)
        assert account.history == [500, -300]
    
    def test_balance_history_normal_transfer_company(self):
        account = CompanyAccount("Firma5", "3416755433")
        account.incoming_transfer(1000)
        account.outgoing_transfer(550)
        assert account.history == [1000, -550]

    def test_balance_history_fast_transfer_personal(self, account: PersonalAccount):
        account.incoming_transfer(200)
        account.outgoing_transfer(50, "fast")
        assert account.history == [200, -50, -1]
    
    def test_balance_history_fast_transfer_company(self):
        account = CompanyAccount("Firma5", "3416755433")
        account.incoming_transfer(550)
        account.outgoing_transfer(250, "fast")
        assert account.history == [550, -250, -5]

    def test_check_history_five_transactions(self, account: PersonalAccount):
        account.incoming_transfer(500)
        account.outgoing_transfer(250, "fast")
        account.incoming_transfer(700)
        account.incoming_transfer(200)
        account.incoming_transfer(1000)
        account.outgoing_transfer(200, "fast")
        account.incoming_transfer(1500)
        account.submit_for_loan(2000)
        assert account.balance == 5448
        assert account.history == [500, -250, -1, 700, 200, 1000, -200, -1, 1500]

    def test_check_history_three_incomming(self, account: PersonalAccount):
        account.incoming_transfer(500)
        account.incoming_transfer(200)
        account.incoming_transfer(700)
        account.submit_for_loan(2000)
        assert account.balance == 3400
        assert account.history == [500, 200, 700]

    def test_check_history_loan_invalid_last_three_invalid(self, account: PersonalAccount):
        account.incoming_transfer(800)
        account.incoming_transfer(700)
        account.outgoing_transfer(200)
        account.submit_for_loan(2000)
        assert account.balance == 1300
        assert account.history == [800, 700, -200]

    def test_check_history_loan_invalid_sum_of_five_less(self, account: PersonalAccount):
        account.incoming_transfer(600)
        account.outgoing_transfer(250)
        account.incoming_transfer(800)
        account.incoming_transfer(700)
        account.outgoing_transfer(300)
        account.submit_for_loan(2000)
        assert account.balance == 1550
        assert account.history == [600, -250, 800, 700, -300]