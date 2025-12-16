import datetime
import pytest
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from lib import smtp
from pytest_mock import MockerFixture

class TestEmail:
    date = datetime.date.today().isoformat()
    email = "test@example.com"

    def test_send_history_personal_success(self, mocker: MockerFixture):
        acc = PersonalAccount("Jan", "Kowalski", "61352353511")
        acc.history = [100, -50]

        send_mock = mocker.patch("lib.smtp.SMTPClient.send", return_value=True)
        result = acc.send_history_via_email(self.email)
        assert result is True
        expected_title = f"Account Transfer History {self.date}"
        expected_body = "Personal account history: 100, -50"

        send_mock.assert_called_once_with(expected_title, expected_body, self.email)


    def test_send_history_personal_failure(self, mocker: MockerFixture):
        acc = PersonalAccount("Jan", "Kowalski", "61352353511")
        acc.history = [1, 2]

        # make send raise
        send_mock = mocker.patch("lib.smtp.SMTPClient.send", return_value=False)
        result = acc.send_history_via_email(self.email)
        assert result is False


    def test_send_history_company_success(self, mocker: MockerFixture):
        mocker.patch.object(CompanyAccount, "is_nip_number_valid", return_value=True)
        acc = CompanyAccount("Firma", "1234567890")
        acc.history = [500, -200]

        send_mock = mocker.patch("lib.smtp.SMTPClient.send", return_value=True)
        result = acc.send_history_via_email(self.email)

        assert result is True
        expected_title = f"Account Transfer History {self.date}"
        expected_body = "Company account history: 500, -200"
        send_mock.assert_called_once_with(expected_title, expected_body, self.email)


    def test_send_history_company_failure(self, mocker: MockerFixture):
        mocker.patch.object(CompanyAccount, "is_nip_number_valid", return_value=True)
        acc = CompanyAccount("Firma", "1234567890")
        acc.history = [10]

        mocker.patch("lib.smtp.SMTPClient.send", return_value=False)

        result = acc.send_history_via_email(self.email)
        assert result is False
