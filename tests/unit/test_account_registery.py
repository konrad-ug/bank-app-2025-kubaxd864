from src.personal_account import PersonalAccount
from src.account_registery import AccountRegistery
from src.account_registery import AccountRegistery
from src.account import Account
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

    def test_update_surname(self, register, account):
        register.add_account(account)
        assert register.update_account_by_id(account.pesel, surname="NewSurname") is True
        assert account.last_name == "NewSurname"

def test_send_history_else_branch_returns_false():
    acc = Account()
    acc.history = [1, 2, 3]
    assert acc.send_history_via_email("a@b.c") is False


def test_account_registery_update_and_delete_behaviour():
    reg = AccountRegistery()
    acc = PersonalAccount("X","Y","61352353511")
    reg.add_account(acc)
    assert reg.update_account_by_id(acc.pesel, name="New") is True
    assert acc.first_name == "New"
    assert reg.update_account_by_id("00000000000", name="No") is False
    assert reg.delete_account_by_id(acc.pesel) is True
    assert reg.delete_account_by_id(acc.pesel) is False
