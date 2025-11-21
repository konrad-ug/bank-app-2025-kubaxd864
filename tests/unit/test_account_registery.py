from src.personal_account import PersonalAccount
from src.account_registery import AccountRegistery
import pytest


@pytest.fixture
def account():
    return PersonalAccount("John", "Doe", "61352353511")


@pytest.fixture
def register():
    return AccountRegistery()


class TestAccountRegistery:
    def test_add_account(self, register, account):
        assert register.return_register_length() == 0
        register.add_account(account)
        assert account in register.return_accounts_list()

    def test_register_length(self, register, account):
        register.add_account(account)
        assert register.return_register_length() == 1

    def test_return_accounts_list(self, register, account):
        register.add_account(account)
        assert register.return_accounts_list() == [account]

    def test_find_by_id_number(self, register, account):
        register.add_account(account)
        account2 = PersonalAccount("James", "May", "75022353511")
        register.add_account(account2)
        assert register.find_by_id_number("75022353511") == account2

    def test_find_by_id_number_no_acc(self, register, account):
        register.add_account(account)
        account2 = PersonalAccount("James", "May", "75022353511")
        register.add_account(account2)
        assert register.find_by_id_number("75022351511") == None
