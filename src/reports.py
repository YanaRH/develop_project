import datetime
import json
import logging
from typing import Any, Callable, Optional, Dict
import csv as pd  # Импортируем pandas

from src.decorators import decorator_spending_by_category

logger = logging.getLogger("report.log")
file_handler = logging.FileHandler("report.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def log_spending_by_category(filename: Any) -> Callable:
    """Логирует результат функции в указанный файл"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            with open(filename, "w") as f:
                json.dump(result, f, indent=4)
            return result

        return wrapper


@decorator_spending_by_category
def spending_by_category(
        transactions: pd.DataFrame,  # Изменено на DataFrame
        category: str,
        date: Optional[str] = None
) -> pd.DataFrame:  # Изменено на DataFrame
    """Функция возвращающая траты за последние 3 месяца по заданной категории"""
    logger.info("Начало работы")

    if date is None:
        logger.info("Обработка условия на отсутствие даты")
        date_start = datetime.datetime.now() - datetime.timedelta(days=90)

        # Фильтрация по категории
        filtered_transactions = transactions[transactions["Категория"] == category]

        # Фильтрация по дате
        filtered_transactions["Дата платежа"] = pd.to_datetime(filtered_transactions["Дата платежа"], format="%d.%m.%Y",
                                                               errors='coerce')
        final_list = filtered_transactions[
            (filtered_transactions["Дата платежа"] >= date_start) &
            (filtered_transactions["Дата платежа"] <= date_start + datetime.timedelta(days=90))
            ]

        return final_list[["Сумма платежа", "Дата платежа", "Категория"]].to_dict(
            orient='records')  # Возвращаем список словарей
    else:
        logger.info("Обработка условия с указанной датой")
        try:
            day, month, year = map(int, date.split("."))
            date_obj = datetime.datetime(year, month, day)
            date_start = date_obj - datetime.timedelta(days=90)
        except ValueError as e:
            logger.error(f"Неверный формат даты: {e}")
            return []

        filtered_transactions = transactions[transactions["Категория"] == category]

        filtered_transactions["Дата платежа"] = pd.to_datetime(filtered_transactions["Дата платежа"], format="%d.%m.%Y",
                                                               errors='coerce')
        final_list = filtered_transactions[
            (filtered_transactions["Дата платежа"] >= date_start) &
            (filtered_transactions["Дата платежа"] <= date_start + datetime.timedelta(days=90))
            ]

        logger.info("Завершение работы функции")
        return final_list[["Сумма платежа", "Дата платежа", "Категория"]].to_dict(
            orient='records')  # Возвращаем список словарей
