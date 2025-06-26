import json
import logging
from datetime import datetime
from typing import Dict, Any

import pandas as pd
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Относительный путь к файлу данных
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'operations.xlsx')
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), '..', 'user_settings.json')

def load_transactions() -> pd.DataFrame:
    """Загружает транзакции из файла Excel."""
    df = pd.read_excel(DATA_PATH)
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

def load_user_settings() -> Dict[str, Any]:
    """Загружает настройки из файла user_settings.json."""
    with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_greeting(current_time: datetime.time) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    if datetime.strptime('05:00', '%H:%M').time() <= current_time < datetime.strptime('12:00', '%H:%M').time():
        return "Доброе утро"
    elif datetime.strptime('12:00', '%H:%M').time() <= current_time < datetime.strptime('17:00', '%H:%M').time():
        return "Добрый день"
    elif datetime.strptime('17:00', '%H:%M').time() <= current_time < datetime.strptime('22:00', '%H:%M').time():
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def fetch_currency_rates() -> list:
    """
    Получает курсы валют из файла настроек.
    """
    settings = load_user_settings()
    return settings.get('currency_rates', [])

def get_sp500_price() -> float:
    """
    Получает цену S&P 500 из файла настроек.
    """
    settings = load_user_settings()
    return settings.get('sp500_price', 0.0)
