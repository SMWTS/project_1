import json

import pytest

from src.services import profitable_bonus_categories


# Фикстура с тестовыми транзакциями
@pytest.fixture
def sample_transactions():
    return [
        {"Дата операции": "2025-06-15 10:30:00", "Категория": "Питание", "Сумма операции": 2500},
        {"Дата операции": "2025-06-20 14:00:00", "Категория": "Развлечения", "Сумма операции": 1500},
        {"Дата операции": "2025-05-25 09:00:00", "Категория": "Путешествия", "Сумма операции": 5000},
        {"Дата операции": "2025-06-10 12:00:00", "Категория": "Питание", "Сумма операции": 300},
    ]


def test_profitability_for_june(sample_transactions):
    # Анализ за июнь 2025
    result_json = profitable_bonus_categories(2025, 6, sample_transactions)
    result = json.loads(result_json)

    # Проверка, что транзакции за июнь учтены
    assert "Питание" in result
    assert "Развлечения" in result
    # Транзакции за май не должны учитываться
    assert "Путешествия" not in result
    # Проверка суммы кешбэка
    # 1500 кешбэк = 15
    assert result["Развлечения"] == 15


def test_no_transactions_for_month():
    transactions = [{"Дата операции": "2025-05-15 10:00:00", "Категория": "Питание", "Сумма операции": 1000}]
    # Анализ за июнь 2025, транзакций нет
    result_json = profitable_bonus_categories(2025, 6, transactions)
    result = json.loads(result_json)
    assert result == {}


def test_empty_transactions():
    # Пустой список транзакций
    result_json = profitable_bonus_categories(2025, 6, [])
    result = json.loads(result_json)
    assert result == {}


def test_transaction_date_format():
    transactions = [{"Дата операции": "2025-06-15 10:30:00", "Категория": "Питание", "Сумма операции": 2500}]
    # Проверка, что функция правильно парсит дату
    result_json = profitable_bonus_categories(2025, 6, transactions)
    result = json.loads(result_json)
    assert "Питание" in result


def test_logging_output(caplog, sample_transactions):
    # Проверка, что логируется сообщение о количестве транзакций
    with caplog.at_level("INFO"):
        profitable_bonus_categories(2025, 6, sample_transactions)
    assert "Найдено транзакций за 6/2025" in caplog.text
