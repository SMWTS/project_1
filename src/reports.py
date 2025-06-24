import json
import logging
from datetime import datetime, timedelta

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def expenses_by_category(df: pd.DataFrame, category: str, start_date) -> str:
    # Если start_date — число или список чисел (например, год и месяц)
    if not isinstance(start_date, str):
        # Предположим, что start_date — это кортеж или список вида (год, месяц, день)
        if isinstance(start_date, (list, tuple)):
            start_date = f"{start_date[0]}-{start_date[1]:02d}-{start_date[2]:02d}"
        else:
            start_date = str(start_date)
    # Парсим дату начала периода
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError as e:
        logger.error(f"Ошибка парсинга даты: {e}")
        raise

    # Вычисляем дату окончания периода (через 90 дней)
    end_dt = start_dt + timedelta(days=90)

    # Убедимся, что дата в DataFrame приведена к типу datetime
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")

    # Создаем маски для фильтрации по дате и категории
    mask_date = (df["Дата операции"] >= start_dt) & (df["Дата операции"] <= end_dt)
    mask_category = df["Категория"] == category

    # Применяем фильтр
    filtered_df = df[mask_date & mask_category]

    # Суммируем расходы
    total_expenses = filtered_df["Сумма операции"].sum()

    # Формируем результат
    result = {
        "категория": category,
        "начальная_дата": start_date,
        "конечная_дата": end_dt.strftime("%Y-%m-%d"),
        "итоговые_траты": total_expenses,
    }

    return json.dumps(result, ensure_ascii=False)
