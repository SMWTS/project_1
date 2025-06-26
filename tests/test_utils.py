from datetime import datetime
from unittest.mock import Mock, patch

from src.utils import fetch_currency_rates, get_greeting, get_sp500_price, load_transactions


def test_load_transactions():
    df = load_transactions()
    assert not df.empty
    assert "Дата операции" in df.columns


def test_get_greeting():
    morning = get_greeting(datetime.strptime("2025-06-24 06:00:00", "%Y-%m-%d %H:%M:%S").time())
    afternoon = get_greeting(datetime.strptime("2025-06-24 13:00:00", "%Y-%m-%d %H:%M:%S").time())
    evening = get_greeting(datetime.strptime("2025-06-24 18:00:00", "%Y-%m-%d %H:%M:%S").time())
    night = get_greeting(datetime.strptime("2025-06-24 23:00:00", "%Y-%m-%d %H:%M:%S").time())
    assert morning == "Доброе утро"
    assert afternoon == "Добрый день"
    assert evening == "Добрый вечер"
    assert night == "Доброй ночи"

def test_get_sp500_price():
    price = get_sp500_price()
    assert isinstance(price, float) or price is None