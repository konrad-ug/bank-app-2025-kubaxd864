from src.company_account import CompanyAccount

class TestCompanyAccount: 
    def test_company_account(self):
        account = CompanyAccount("Firma1", "3423454333")
        assert account.company_name == "Firma1"
        assert account.nip_number == "3423454333"
        assert account.balance == 0

    def test_is_nip_number_to_long(self):
        account = CompanyAccount("Firma1", "34234543337")
        assert account.nip_number == "Niepoprawny NIP!"
    
    def test_is_nip_number_to_short(self):
        account = CompanyAccount("Firma1", "3423454")
        assert account.nip_number == "Niepoprawny NIP!"