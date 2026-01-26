import pytest
from unittest.mock import MagicMock, patch
from src.mongo import MongoAccountsRepository
from src.personal_account import PersonalAccount

class TestMongoAccountsRepository:
    
    @patch('src.mongo.MongoClient')
    def test_save_all(self, mock_client_cls):
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_collection = MagicMock()
        
        mock_client_cls.return_value = mock_client
        mock_client.bank_app = mock_db
        mock_db.accounts = mock_collection
        
        repo = MongoAccountsRepository()
        
        account = PersonalAccount("Jan", "Kowalski", "12345678901", balance=100)
        account.history = [10, -10]
        accounts = [account]
        
        repo.save_all(accounts)
        
        mock_collection.delete_many.assert_called_once_with({})
        mock_collection.insert_many.assert_called_once()
        args, _ = mock_collection.insert_many.call_args
        inserted_data = args[0]
        assert len(inserted_data) == 1
        assert inserted_data[0]["first_name"] == "Jan"
        assert inserted_data[0]["balance"] == 100
        assert inserted_data[0]["history"] == [10, -10]

    @patch('src.mongo.MongoClient')
    def test_load_all(self, mock_client_cls):
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_collection = MagicMock()
        
        mock_client_cls.return_value = mock_client
        mock_client.bank_app = mock_db
        mock_db.accounts = mock_collection
        
        mock_collection.find.return_value = [
            {"first_name": "Jan", "last_name": "Kowalski", "pesel": "12345678901", "balance": 200.0, "history": [50]}
        ]
        
        repo = MongoAccountsRepository()
        accounts = repo.load_all()
        
        assert len(accounts) == 1
        assert accounts[0].first_name == "Jan"
        assert accounts[0].balance == 200.0
        assert accounts[0].history == [50]
