import json

import pytest
import pandas as pd
from src.reports import expenses_by_category

# Создадим фикстуру с тестовыми данными
@pytest.fixture
def sample_df():
    data = {
        'Дата операции': [
            '2025-03-15', '2025-04-10', '2025-05-20', '2025-06-05', '2025-07-01'
        ],
        'Категория': [
            'Развлечения', 'Развлечения', 'Покупки', 'Развлечения', 'Путешествия'
        ],
        'Сумма операции': [
            500, 1500, 2000, 700, 3000
        ]
    }
    df = pd.DataFrame(data)
    return df

def test_expenses_by_category_correct_sum(sample_df):
    # Вызов функции с датой начала периода
    start_date = '2025-03-01'
    category = 'Развлечения'
    # Вызов функции
    result_json = expenses_by_category(sample_df, category, start_date)
    result = json.loads(result_json)
    assert result['категория'] == category
    assert result['начальная_дата'] == start_date
    assert result['конечная_дата'] == '2025-05-30'