import pandas as pd
from utils import load_transactions, get_greeting, fetch_currency_rates, get_sp500_price
from reports import expenses_by_category
import json
from datetime import datetime

def main():
    """Функция, которая запускает всю программу"""
    input_datetime_str = '2025-06-24 14:30:00'
    category = 'Развлечения'
    start_date = '2025-03-01'

    df = load_transactions()

    dt = datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M:%S')
    greeting = get_greeting(dt.time())

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
    date_from = dt.replace(day=1)
    date_to = dt
    filtered_df = df[(df['Дата операции'] >= date_from) & (df['Дата операции'] <= date_to)]

    last_digits = [str(card)[-4:] for card in filtered_df['Номер карты']]
    total_expenses = filtered_df['Сумма операции'].sum()
    cashback = int(total_expenses // 100)
    top_transactions = filtered_df.sort_values(by='Сумма операции', ascending=False).head(5)
    top_list = top_transactions[['Номер карты', 'Описание', 'Сумма операции']].to_dict(orient='records')
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
        "стоимость_SP500": sp500_price
    }

    print(json.dumps(result, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
