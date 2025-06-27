import json
from datetime import datetime

import pandas as pd

from src.reports import expenses_by_category
from src.utils import fetch_currency_rates, get_greeting, get_sp500_price, load_transactions


def main():
    input_datetime_str = "2025-06-24 14:30:00"
    category = "Развлечения"
    start_date = "2025-03-01"

    df = load_transactions()

    dt = datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(dt.time())

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    date_from = dt.replace(day=1)
    date_to = dt
    filtered_df = df[(df["Дата операции"] >= date_from) & (df["Дата операции"] <= date_to)]

    # Обработка ключа last_digits: берем одно значение - номер карты первой транзакции
    last_digits_value = None
    if len(filtered_df) > 0:
        last_digits_value = str(filtered_df.iloc[0]["Номер карты"])[-4:]

    # Группировка по картам для ключа 'cards'
    cards_info = []
    grouped = filtered_df.groupby("Номер карты")
    for card_num, group in grouped:
        total_spent = group["Сумма операции"].sum()
        cashback_sum = group["Кешбэк"].sum()
        cards_info.append(
            {"номер_карты": str(card_num), "общая_сумма_расходов": float(total_spent), "кешбек": float(cashback_sum)}
        )

    # Вызов отчета по категории с декоратором
    report_json = expenses_by_category(df, category, start_date)

    # Итоговая структура
    result = {
        "приветствие": greeting,
        "последние_4_цифры_карт": last_digits_value,
        "общая_сумма_расходов": float(filtered_df["Сумма операции"].sum()),
        "кешбэк": float(filtered_df["Кешбэк"].sum()),
        "топ_5_транзакций": filtered_df.sort_values(by="Сумма операции", ascending=False)
        .head(5)[["Номер карты", "Описание", "Сумма операции"]]
        .to_dict(orient="records"),
        "отчет_по_категории": json.loads(report_json),
        "курсы_валют": fetch_currency_rates(),
        "стоимость_SP500": get_sp500_price(),
        "cards": cards_info,
    }

    print(json.dumps(result, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
