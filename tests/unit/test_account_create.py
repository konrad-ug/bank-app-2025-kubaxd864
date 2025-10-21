from src.personal_account import PersonalAccount


class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "51352353511")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0

    def test_is_pesel_to_long(self):
        account = PersonalAccount("John", "Doe", "236342343221")
        assert account.pesel == "Invalid"
    
    def test_is_pesel_to_short(self):
        account = PersonalAccount("John", "Doe", "23634")
        assert account.pesel == "Invalid"
    
    def test_is_pesel_digit(self):
        account = PersonalAccount("John", "Doe", "wdwda")
        assert account.pesel == "Invalid"
    
    def test_is_pesel_valid(self):
        account = PersonalAccount("John", "Doe", "51352353511")
        assert account.pesel == "51352353511"

    def test_is_promo_code_valid(self):
        account = PersonalAccount("John", "Doe", "61352353511", "PROM_2025")
        assert account.balance == 50
    
    def test_is_promo_code_to_long(self):
        account = PersonalAccount("John", "Doe", "61352353511", "PROM_202522")
        assert account.balance == 0

    def test_is_promo_code_to_short(self):
        account = PersonalAccount("John", "Doe", "81352353511", "PROM_")
        assert account.balance == 0
    
    def test_no_promo_code(self):
        account = PersonalAccount("John", "Doe", "71352353511")
        assert account.balance == 0

    def test_is_too_old(self):
        account = PersonalAccount("John", "Doe", "41102353511", "PROM_2025")
        assert account.balance == 0

    def test_is_too_old_after_2000(self):
        account = PersonalAccount("John", "Doe", "01302353511", "PROM_2025")
        assert account.balance == 50

    def test_is_too_old_before_2000(self):
        account = PersonalAccount("John", "Doe", "91102353511", "PROM_2025")
        assert account.balance == 50