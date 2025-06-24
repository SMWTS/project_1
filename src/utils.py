import logging
import os
from datetime import time

import pandas as pd
import requests
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_FINNHUB = os.getenv("API_KEY_FINNHUB")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Путь к файлу с транзакциями
TRANSACTIONS_FILE = "C:\\Users\\Kamilla\\Desktop\\Files\\kursach\\data\\operations.xlsx"


def load_transactions():
    df = pd.read_excel(TRANSACTIONS_FILE)
    required_columns = [
        "Дата операции",
        "Дата платежа",
        "Номер карты",
        "Статус",
        "Сумма операции",
        "Валюта операции",
        "Сумма платежа",
        "Валюта платежа",
        "Кешбэк",
        "Категория",
        "MCC",
        "Описание",
        "Бонусы (включая кешбэк)",
        "Округление на «Инвесткопилку»",
        "Сумма операции с округлением",
    ]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"В файле отсутствует колонка '{col}'")
    return df


def get_greeting(current_time):
    # Определяем границы времени и соответствующие приветствия
    greetings = [
        (time(5, 0), time(11, 59), "Доброе утро"),
        (time(12, 0), time(17, 59), "Добрый день"),
        (time(18, 0), time(22, 59), "Добрый вечер"),
    ]
    for start, end, greeting in greetings:
        if start <= current_time < end:
            return greeting
    return "Доброй ночи"


def fetch_currency_rates():
    url = "https://api.apilayer.com/exchangerates_data/latest?base=RUB"
    headers = {"apikey": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("rates", {})
    else:
        logging.error(f"Ошибка при получении курсов валют: {response.status_code}")
        return {}


def get_sp500_price():
    url = "https://finnhub.io/api/v1/quote"
    params = {"symbol": "^GSPC", "token": API_KEY_FINNHUB}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("c")
    else:
        logging.error(f"Ошибка при получении цены S&P 500: {response.status_code}")
        return None
