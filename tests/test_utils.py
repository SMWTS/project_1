from datetime import datetime

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


def test_fetch_currency_rates():
    rates = fetch_currency_rates()
    assert isinstance(rates, dict)
    assert "USD" in rates or "EUR" in rates


def test_get_sp500_price():
    price = get_sp500_price()
    assert isinstance(price, float) or price is None


# @patch('utils.requests.get')
# def test_fetch_currency_rates(mock_get):
#     mock_response = MagicMock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {'rates': {'USD': 0.013, 'EUR': 0.012}}
#     mock_get.return_value = mock_response
#     rates = fetch_currency_rates()
#     assert 'USD' in rates
#
# @patch('utils.requests.get')
# def test_get_sp500_price(mock_get):
#     mock_response = MagicMock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {'c': 4200}
#     mock_get.return_value = mock_response
#     price = get_sp500_price()
#     assert price == 4200
