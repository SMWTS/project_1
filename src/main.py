import json
from datetime import datetime

import pandas as pd

from src.utils import load_transactions, get_greeting, fetch_currency_rates, get_sp500_price, load_user_settings
from src.services import profitable_bonus_categories
from src.reports import expenses_by_category

def main():
    # Входные параметры
    input_datetime_str = '2023-03-24 14:00:00'
    category = 'Развлечения'
    start_date = '2023-02-01'

    # Загружаем транзакции
    df = load_transactions()

    # Обработка данных для страницы «Главная»
    dt = datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M:%S')
    greeting = get_greeting(dt.time())

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    date_from = dt.replace(day=1)
    date_to = dt
    filtered_df = df[(df['Дата операции'] >= date_from) & (df['Дата операции'] <= date_to)]

    # Формируем список карт
    last_digits = [str(card)[-4:] for card in filtered_df['Номер карты']]
    total_expenses = filtered_df['Сумма операции'].sum()
    cashback = float(total_expenses) / 100  # кешбэк
    top_transactions_df = filtered_df.sort_values(by='Сумма операции', ascending=False).head(5)
    top_transactions = top_transactions_df[['Дата операции', 'Сумма операции', 'Категория', 'Описание']].to_dict(orient='records')

    # Получение валют и акций из файла настроек
    settings = load_user_settings()
    currency_rates = settings.get('currency_rates', [])
    stock_prices = settings.get('stock_prices', [])

    # Вызов функции анализа кешбэка по категориям
    bonus_json = profitable_bonus_categories(dt.year, dt.month, filtered_df.to_dict(orient='records'))

    # Вызов отчета по категории
    report_json = expenses_by_category(df, category, start_date)

    # Формируем итоговый ответ
    result = {
        "greeting": greeting,
        "cards": [
            {
                "last_digits": last_digits,
                "total_spent": float(total_expenses),
                "cashback": cashback
            }
        ],
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
        "bonus_by_category": json.loads(bonus_json),
        "category_expenses": json.loads(report_json)
    }

    print(json.dumps(result, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()