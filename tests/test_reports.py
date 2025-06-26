import json

import pandas as pd
import pytest
from unittest.mock import patch

from src.reports import expenses_by_category


@pytest.fixture
def sample_df():
    data = {
        'Дата операции': ['2025-05-15', '2025-06-10', '2025-07-01', '2025-05-20'],
        'Категория': ['Развлечения', 'Еда', 'Развлечения', 'Еда'],
        'Сумма операции': [500, 1500, 700, 300]
    }
    df = pd.DataFrame(data)
    return df

def test_expenses_by_category_within_period(sample_df):
    category = 'Развлечения'
    start_date = '2025-05-01'
    result_json = expenses_by_category(sample_df, category, start_date)
    result = json.loads(result_json)

    # Проверка, что результат содержит правильную категорию
    assert result['категория'] == category
    # Проверка, что итоговые траты соответствуют сумме по выбранной категории и периоду
    expected_sum = 500 + 700  # транзакции за май и июнь
    assert abs(result['итоговые_траты'] - expected_sum) < 1e-6
    # Проверка, что дата окончания периода правильная
    assert result['конечная_дата'] == '2025-07-30'  # 3 месяца после 1 марта

def test_expenses_by_category_no_transactions():
    df_empty = pd.DataFrame(columns=['Дата операции', 'Категория', 'Сумма операции'])
    result_json = expenses_by_category(df_empty, 'Любая', '2025-01-01')
    result = json.loads(result_json)
    assert result['итоговые_траты'] == 0