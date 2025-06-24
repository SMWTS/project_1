import unittest
from unittest.mock import patch

import pandas as pd


class TestReportsErrorHandling(unittest.TestCase):

    @patch("src.reports.json.dumps")
    def test_expenses_by_category_exception(self, mock_json_dumps):
        mock_json_dumps.side_effect = Exception("Ошибка сериализации")
        df = pd.DataFrame({"Дата операции": ["2025-06-01"], "Категория": ["Категория1"], "Сумма операции": [1000]})
        from src.reports import expenses_by_category

        with self.assertRaises(Exception):
            expenses_by_category(df, "Категория1", "2025-06-01")
        mock_json_dumps.assert_called()
