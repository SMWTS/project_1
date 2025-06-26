import json

import pytest
from src.services import profitable_bonus_categories

def test_profitable_bonus_categories():
    transactions = [
        {'Дата операции': '2025-06-01', 'Категория': 'Еда', 'Сумма операции': 500},
        {'Дата операции': '2025-06-15', 'Категория': 'Еда', 'Сумма операции': 1500},
        {'Дата операции': '2025-05-20', 'Категория': 'Развлечения', 'Сумма операции': 2000},
    ]
    result_json = profitable_bonus_categories(2025, 6, transactions)
    result = json.loads(result_json)
    assert result['Еда'] == 20  # 500//100 + 1500//100 = 5 + 15 = 20
    assert 'Развлечения' not in result

def test_empty_transactions():
    result_json = profitable_bonus_categories(2025, 1, [])
    result = json.loads(result_json)
    assert result == {}