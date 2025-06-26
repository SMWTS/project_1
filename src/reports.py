import json
import logging
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def expenses_by_category(df: pd.DataFrame, category: str, start_date: str) -> str:
    """
    Возвращает JSON-отчет о тратах по категории за трехмесячный период, начиная с start_date.
    """
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    # Расчет конца периода (3 месяца)
    end_dt = start_dt + timedelta(days=90)

    # Фильтрация по дате
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])
    mask_date = (df['Дата операции'] >= start_dt) & (df['Дата операции'] <= end_dt)

    # Фильтрация по категории
    mask_category = df['Категория'] == category

    # Итоговые траты
    filtered_df = df[mask_date & mask_category]

    total_expenses = filtered_df['Сумма операции'].sum()

    # Преобразование типов для сериализации
    def convert_types(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        raise TypeError(f"Тип {type(obj)} не сериализуемый")

    # Формируем ответ
    result = {
        "категория": category,
        "начальная_дата": start_date,
        "конечная_дата": end_dt.strftime('%Y-%m-%d'),
        "итоговые_траты": total_expenses
    }

    # Возвращаем JSON
    return json.dumps(result, default=convert_types, ensure_ascii=False)