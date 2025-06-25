import json

import pandas as pd
from src.reports import expenses_by_category


def test_expenses_by_category_no_data():
    df = pd.DataFrame({
        'Дата операции': [],
        'Категория': [],
        'Сумма операции': []
    })
    result_json = expenses_by_category(df, 'Еда', '2025-01-01')
    result = json.loads(result_json)
    assert result['итоговые_траты'] == 0