from src.personal_account import PersonalAccount
import pytest


class TestPrivateTransfers:
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

    @pytest.mark.parametrize("pesel,promo,amount,expected", [
        ("75352353511", "PROM_2025", 20, 29),
        ("75352353511", "PROM_2025", 50, -1),
    ])
    def test_fast_transfer_personal_variations(self, pesel, promo, amount, expected):
        account = PersonalAccount("John", "Doe", pesel, promo)
        account.outgoing_transfer(amount, "fast")
        assert account.balance == expected

    def test_fast_transfer_negative_balance(self):
        account = PersonalAccount("John", "Doe", "75352353511", "PROM_2025")
        account.outgoing_transfer(50, "fast")
        assert account.balance == -1

    def test_balance_history_normal_transfer_personal(self, account: PersonalAccount):
        account.incoming_transfer(500)
        account.outgoing_transfer(300)
        assert account.history == [500, -300]

    def test_balance_history_fast_transfer_personal(self, account: PersonalAccount):
        account.incoming_transfer(200)
        account.outgoing_transfer(50, "fast")
        assert account.history == [200, -50, -1]

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

    def test_personal_fast_fee_applied_even_if_amount_exceeds_balance(self):
        acc = PersonalAccount("Jan", "Kowalski", "61352353511")
        acc.balance = 2
        acc.outgoing_transfer(100, "fast")
        assert acc.balance == 1  
        assert acc.history == [-1] 