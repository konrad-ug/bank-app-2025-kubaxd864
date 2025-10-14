from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "51352353511")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0

    def test_is_pesel_to_long(self):
        account = Account("John", "Doe", "236342343221")
        assert account.pesel == "Invalid"
    
    def test_is_pesel_to_short(self):
        account = Account("John", "Doe", "23634")
        assert account.pesel == "Invalid"
    
    def test_is_pesel_digit(self):
        account = Account("John", "Doe", "wdwda")
        assert account.pesel == "Invalid"
    
    def test_is_pesel_valid(self):
        account = Account("John", "Doe", "51352353511")
        assert account.pesel == "51352353511"

    def test_is_promo_code_valid(self):
        account = Account("John", "Doe", "61352353511", "PROM_2025")
        assert account.balance == 50
    
    def test_is_promo_code_to_long(self):
        account = Account("John", "Doe", "61352353511", "PROM_202522")
        assert account.balance == 0

    def test_is_promo_code_to_short(self):
        account = Account("John", "Doe", "81352353511", "PROM_")
        assert account.balance == 0
    
    def test_no_promo_code(self):
        account = Account("John", "Doe", "71352353511")
        assert account.balance == 0

    def test_is_too_old(self):
        account = Account("John", "Doe", "51352353511", "PROM_2025")
        assert account.balance == 0