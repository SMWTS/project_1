import json

from src.services import profitable_bonus_categories


def test_profitable_bonus_categories():
    transactions = [
        {"Дата операции": "2025-06-01", "Категория": "Еда", "Сумма операции": 500},
        {"Дата операции": "2025-06-15", "Категория": "Транспорт", "Сумма операции": 300},
        {"Дата операции": "2025-06-20", "Категория": "Еда", "Сумма операции": 700},
        {"Дата операции": "2025-05-10", "Категория": "Развлечения", "Сумма операции": 1000},
    ]
    result_json = profitable_bonus_categories(2025, 6, transactions)
    result = json.loads(result_json)
    assert result["Еда"] == 12  # 1200/100=12
    assert result["Транспорт"] == 3
    assert "Развлечения" not in result  # не в июне
