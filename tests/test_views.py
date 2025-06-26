import json
import unittest
import warnings
from unittest.mock import patch

import pandas as pd

# Предположим, что ваша функция находится в модуле src.views
from src.views import main_page_handler


class TestMainPageHandler(unittest.TestCase):

    @patch("src.utils.get_greeting")
    @patch("src.utils.load_transactions")
    @patch("src.utils.fetch_currency_rates")
    @patch("src.utils.get_sp500_price")
    @patch("src.reports.expenses_by_category")
    def test_main_page_handler(
        self,
        mock_expenses_by_category,
        mock_get_sp500_price,
        mock_fetch_currency_rates,
        mock_load_transactions,
        mock_get_greeting,
    ):
        # Настраиваем моки
        mock_get_greeting.return_value = "Добрый день"
        mock_load_transactions.return_value = pd.DataFrame(
            {
                "Дата операции": ["2023-07-15", "2023-07-10"],
                "Номер карты": ["1234567890123456", "9876543210987654"],
                "Описание": ["Покупка A", "Покупка B"],
                "Сумма операции": [100, 200],
            }
        )
        mock_fetch_currency_rates.return_value = {"USD": 1.0, "EUR": 0.85}
        mock_get_sp500_price.return_value = 4200.5
        # Мок для отчета по категории
        mock_expenses_by_category.return_value = json.dumps({"category": "Траты по категории"})

        # Вызов функции с тестовыми параметрами
        result_json_str = main_page_handler(
            input_datetime_str="2023-07-15 12:00:00", category="Категория", start_date_str="2023-07-01"
        )

        result = json.loads(result_json_str)

        # Проверки
        self.assertEqual(result["приветствие"], "Добрый день")
        self.assertIn("последние_4_цифры_карт", result)
        self.assertEqual(result["общая_сумма_расходов"], 0.0)
        self.assertEqual(result["кешбэк"], 0)


warnings.filterwarnings("ignore")

if __name__ == "__main__":
    unittest.main()
