import json
import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

from src.reports import expenses_by_category
from src.utils import fetch_currency_rates, get_greeting, get_sp500_price, load_transactions

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_FINNHUB = os.getenv("API_KEY_FINNHUB")


def main():
    input_datetime_str = "2025-06-24 14:30:00"
    category = "Развлечения"
    start_date = "2025-03-01"

    df = load_transactions()

    dt = datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(dt.time())

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    date_from = dt.replace(day=1)
    date_to = dt
    filtered_df = df[(df["Дата операции"] >= date_from) & (df["Дата операции"] <= date_to)]

    last_digits = [str(card)[-4:] for card in filtered_df["Номер карты"]]
    total_expenses = filtered_df["Сумма операции"].sum()
    cashback = int(total_expenses // 100)
    top_transactions = filtered_df.sort_values(by="Сумма операции", ascending=False).head(5)
    top_list = top_transactions[["Номер карты", "Описание", "Сумма операции"]].to_dict(orient="records")
    currency_rates = fetch_currency_rates()
    sp500_price = get_sp500_price()

    report_json = expenses_by_category(df, category, start_date)

    result = {
        "приветствие": greeting,
        "последние_4_цифры_карт": last_digits,
        "общая_сумма_расходов": total_expenses,
        "кешбэк": cashback,
        "топ_5_транзакций": top_list,
        "отчет_по_категории": json.loads(report_json),
        "курсы_валют": currency_rates,
        "стоимость_SP500": sp500_price,
    }

    print(json.dumps(result, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
