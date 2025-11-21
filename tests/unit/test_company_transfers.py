from src.company_account import CompanyAccount
import pytest

class TestCompanyTransfers:
    @pytest.fixture
    def account(self):
        account = CompanyAccount("Firma1", "3423454333")
        return account

    def test_balance_add_CompanyAcc(self, account: CompanyAccount):
        account.incoming_transfer(1205)
        assert account.balance == 1205

    def test_balance_send_CompanyAcc(self, account: CompanyAccount):
        account.balance = 200
        account.outgoing_transfer(30)
        assert account.balance == 170

    def test_fast_transfer_company(self, account: CompanyAccount):
        account.balance = 2000
        account.outgoing_transfer(1599, "fast")
        assert account.balance == 396

    def test_fast_transfer_negative_balance_company(self, account: CompanyAccount):
        account.balance = 500
        account.outgoing_transfer(498, "fast")
        assert account.balance == -3

    def test_balance_history_normal_transfer_company(self, account: CompanyAccount):
        account.incoming_transfer(1000)
        account.outgoing_transfer(550)
        assert account.history == [1000, -550]

    def test_balance_history_fast_transfer_company(self, account: CompanyAccount):
        account.incoming_transfer(550)
        account.outgoing_transfer(250, "fast")
        assert account.history == [550, -250, -5]

    def test_check_loan_succesful(self, account: CompanyAccount):
        account.balance = 5000
        account.history = [5000, 200, -100, -1775]
        account.take_loan(2000)
        assert account.balance == 7000

    def test_one_double_amount_only(self, account: CompanyAccount):
        account.balance = 5000
        account.history = [5000, 200, -100, -1000, 2000]
        account.take_loan(2000)
        assert account.balance == 5000

    def test_only_one_transfer_to_zus(self, account: CompanyAccount):
        account.balance = 5000
        account.history = [5000, 200, -100, -1775]
        account.take_loan(11000)
        assert account.balance == 5000

    def test_fast_fee_applied_even_if_amount_exceeds_balance(company_account_class):
        acc = CompanyAccount("FirmaX", "1234567890")
        acc.balance = 3
        acc.outgoing_transfer(10, "fast")
        assert acc.balance == -2   
        assert acc.history == [-5]   