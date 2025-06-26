import unittest
from unittest.mock import patch


class TestMainErrorHandling(unittest.TestCase):

    @patch("src.main.load_transactions")
    def test_main_load_transactions_exception(self, mock_load_transactions):
        # Имитация исключения при загрузке транзакций
        mock_load_transactions.side_effect = Exception("Ошибка чтения файла")
        from src.main import main

        with self.assertRaises(Exception):
            main()
