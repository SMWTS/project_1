import json
from datetime import datetime, timedelta

import pandas as pd


def expenses_by_category(df: pd.DataFrame, category: str, start_date: str) -> str:
    """
    Возвращает JSON-отчет о тратах по категории за трехмесячный период, начиная с start_date.
    """
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = start_dt + timedelta(days=90)

    df['Дата операции'] = pd.to_datetime(df['Дата операции'])
    mask_date = (df['Дата операции'] >= start_dt) & (df['Дата операции'] <= end_dt)

    filtered_df = df[mask_date & (df['Категория'] == category)]

    total_expenses = float(filtered_df['Сумма операции'].sum())

    result = {
        "категория": category,
        "начальная_дата": start_date,
        "конечная_дата": end_dt.strftime('%Y-%m-%d'),
        "итоговые_траты": total_expenses
    }

    return json.dumps(result, ensure_ascii=False)