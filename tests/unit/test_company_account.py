from src.company_account import CompanyAccount
import pytest
from pytest_mock import MockerFixture

class TestCompanyAccount: 
    def test_company_account(self, mocker: MockerFixture):
        mocker.patch.object(CompanyAccount, "is_nip_number_valid", return_value=True)
        account = CompanyAccount("Firma1", "8461627563")
        assert account.company_name == "Firma1"
        assert account.nip_number == "8461627563"
        assert account.balance == 0

    def test_company_account_without_request(self, mocker: MockerFixture):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}
        mocker.patch("src.company_account.requests.get", return_value=mock_response)
        account = CompanyAccount("Firma1", "8461627563")
        assert account.company_name == "Firma1"
        assert account.nip_number == "8461627563"
        assert account.balance == 0

    def test_is_nip_number_to_long(self):
        with pytest.raises(ValueError):
            CompanyAccount("Firma1", "846162756334")
    
    def test_is_nip_number_to_short(self):
        with pytest.raises(ValueError):
            CompanyAccount("Firma1", "3423454")