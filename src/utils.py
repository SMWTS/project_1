import os
import logging
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_FINNHUB = os.getenv("API_KEY_FINNHUB")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Относительный путь к файлу с транзакциями
BASE_DIR = r"C:\Users\Kamilla\Desktop\Files\Project 1. Application for analysis of banking operations\data"
TRANSACTIONS_FILE = os.path.join(BASE_DIR, "operations.xlsx")

def load_transactions() -> pd.DataFrame:
    """
    Загружает транзакции из файла Excel.
    Возвращает DataFrame с данными.
    """
    df = pd.read_excel(TRANSACTIONS_FILE)
    # Проверка наличия обязательных колонок
    required_columns = [
        'Дата операции', 'Дата платежа', 'Номер карты', 'Статус',
        'Сумма операции', 'Валюта операции', 'Сумма платежа', 'Валюта платежа',
        'Кешбэк', 'Категория', 'MCC', 'Описание', 'Бонусы (включая кешбэк)',
        'Округление на «Инвесткопилку»', 'Сумма операции с округлением'
    ]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"В файле отсутствует колонка '{col}'")
    return df

def get_greeting(current_time: datetime.time) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.
    """
    if datetime.strptime('05:00', '%H:%M').time() <= current_time < datetime.strptime('12:00', '%H:%M').time():
        return "Доброе утро"
    elif datetime.strptime('12:00', '%H:%M').time() <= current_time < datetime.strptime('17:00', '%H:%M').time():
        return "Добрый день"
    elif datetime.strptime('17:00', '%H:%M').time() <= current_time < datetime.strptime('22:00', '%H:%M').time():
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def fetch_currency_rates() -> dict:
    """
    Получает текущие курсы валют с API.
    Возвращает словарь с курсами.
    """
    url = 'https://api.apilayer.com/exchangerates_data/latest?base=RUB'
    headers = {'apikey': API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('rates', {})
    else:
        logging.error(f"Ошибка при получении курсов валют: {response.status_code}")
        return {}

def get_sp500_price() -> Any | None:
    """
    Получает текущую цену индекса S&P 500 через API Finnhub.
    Возвращает цену как float.
    """
    api_key = API_KEY_FINNHUB
    url = 'https://finnhub.io/api/v1/quote'
    params = {'symbol': '^GSPC', 'token': api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('c')  # текущая цена закрытия
    else:
        logging.error(f"Ошибка при получении цены S&P 500: {response.status_code}")
        return None
