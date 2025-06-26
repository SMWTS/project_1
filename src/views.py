import json
from datetime import datetime

import pandas as pd

from src.reports import expenses_by_category
from src.utils import fetch_currency_rates, get_greeting, get_sp500_price, load_transactions


def main_page_handler(input_datetime_str, category, start_date_str):
    """
    Обработка запроса для страницы «Главная».
    - input_datetime_str: строка с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'
    - category: категория для отчета «Траты по категории»
    - start_date_str: дата начала периода в формате 'YYYY-MM-DD'

    Возвращает JSON-ответ.
    """
    # Парсим входную дату
    dt = datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(dt.time())

    # Загружаем транзакции
    df = load_transactions()

    # Фильтрация по дате операции
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    date_from = dt.replace(day=1)
    date_to = dt
    filtered_df = df[(df["Дата операции"] >= date_from) & (df["Дата операции"] <= date_to)]

    # Формируем список последних 4 цифр карт
    last_digits = [str(card)[-4:] for card in filtered_df["Номер карты"]]

    # Общая сумма расходов
    total_expenses = filtered_df["Сумма операции"].sum()

    # Кешбэк
    cashback = int(total_expenses // 100)

    # Топ-5 транзакций
    top_transactions = filtered_df.sort_values(by="Сумма операции", ascending=False).head(5)
    top_list = top_transactions[["Номер карты", "Описание", "Сумма операции"]].to_dict(orient="records")

    # Курсы валют
    currency_rates = fetch_currency_rates()

    # Стоимость S&P 500
    sp500_price = get_sp500_price()

    # Вызов отчета «Траты по категории»
    report_json_str = expenses_by_category(df, category, start_date_str)
    report_json = json.loads(report_json_str)

    # Итоговый JSON
    result = {
        "приветствие": greeting,
        "последние_4_цифры_карт": last_digits,
        "общая_сумма_расходов": total_expenses,
        "кешбэк": cashback,
        "топ_5_транзакций": top_list,
        "отчет_по_категории": report_json,
        "курсы_валют": currency_rates,
        "стоимость_SP500": sp500_price,
    }

    return json.dumps(result, ensure_ascii=False)
