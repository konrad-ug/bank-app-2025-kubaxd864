from src.account import Account


class TestTransfers:
    def test_balance_add(self):
        account = Account("John", "Doe", "61352353511", "PROM_2025")
        account.incoming_balance(100)
        assert account.balance == 150

    def test_add_negative_balance(self):
        account = Account("John", "Doe", "75352353511", "PROM_2025")
        account.incoming_balance(-100)
        assert account.balance == 50

    def test_add_string_balance(self):
        account = Account("John", "Doe", "75352353511", "PROM_2025")
        account.incoming_balance("XD")
        assert account.balance == 50

    def test_balance_send(self):
        account = Account("John", "Doe", "61352353511", "PROM_2025")
        account.outgoing_balance(20)
        assert account.balance == 30

    def test_send_negative_balance(self):
        account = Account("John", "Doe", "75352353511", "PROM_2025")
        account.outgoing_balance(-100)
        assert account.balance == 50

    def test_send_string_balance(self):
        account = Account("John", "Doe", "75352353511", "PROM_2025")
        account.outgoing_balance("XD")
        assert account.balance == 50
