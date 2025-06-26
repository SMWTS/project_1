import json
import logging
from datetime import datetime
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def profitable_bonus_categories(year: int, month: int, transactions: List[Dict[str, Any]]) -> str:
    """Анализирует транзакции за указанный месяц и год, подсчитывает сумму кешбэка по категориям.        """
    def is_in_month(transaction):
        date_str = transaction.get('Дата операции')
        date_obj = datetime.strptime(str(date_str), '%Y-%m-%d')
        return date_obj.year == year and date_obj.month == month

    filtered_transactions = list(filter(is_in_month, transactions))
    logging.info(f"Найдено транзакций за {month}/{year}: {len(filtered_transactions)}")

    def reducer(acc, transaction):
        category = transaction.get('Категория', 'Без категории')
        amount = transaction.get('Сумма операции', 0)
        cashback = int(amount // 100)
        acc[category] = acc.get(category, 0) + cashback
        return acc

    cashback_by_category = {}
    for transaction in filtered_transactions:
        cashback_by_category = reducer(cashback_by_category, transaction)

    return json.dumps(cashback_by_category, ensure_ascii=False)
