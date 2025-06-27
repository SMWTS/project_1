import functools
import json
import logging
from datetime import datetime, timedelta

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_report_to_file(filename=None):
    """
    Декоратор для сохранения результата функции-отчета в файл.
    Если filename не указан, используется имя по умолчанию.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Определяем имя файла
            file_name = filename
            if file_name is None:
                # Имя по умолчанию — имя функции с расширением .json
                file_name = f"{func.__name__}_report.json"
            # Запись в файл
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(result)
            return result

        return wrapper

    return decorator


@save_report_to_file()  # Использование без параметра — имя по умолчанию
def expenses_by_category(df: pd.DataFrame, category: str, start_date: str) -> str:
    """
    Возвращает JSON-отчет о тратах по категории за трехмесячный период, начиная с start_date.
    """
    # Расчет конца периода (3 месяца)
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = start_dt + timedelta(days=90)

    # Фильтрация по дате
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])
    mask_date = (df["Дата операции"] >= start_dt) & (df["Дата операции"] <= end_dt)

    # Фильтрация по категории
    mask_category = df["Категория"] == category

    # Итоговые траты
    filtered_df = df[mask_date & mask_category]

    total_expenses = filtered_df["Сумма операции"].sum()

    # Формируем ответ
    result = {
        "категория": category,
        "начальная_дата": start_date,
        "конечная_дата": end_dt.strftime("%Y-%m-%d"),
        "итоговые_траты": float(total_expenses),
    }

    # Возвращаем JSON
    return json.dumps(result, ensure_ascii=False)
