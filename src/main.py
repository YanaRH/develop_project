import json
import logging
from pathlib import Path
import pandas as pd  # Импортируем pandas для работы с DataFrame


# Заглушки для функций
def currency_rates(currency):
    return {}


def for_each_card(transactions):
    return []


def get_price_stock(stocks):
    return {}


def greetings():
    return "Добро пожаловать!"


def read_excel(file_path):
    return pd.read_excel(file_path, engine='openpyxl')  # Чтение Excel файла в DataFrame


def top_five_transaction(transactions):
    return []


# Функция для фильтрации транзакций по дате
def filter_by_date(date: str, transactions: pd.DataFrame) -> pd.DataFrame:
    """Фильтрация транзакций по заданной дате."""
    if transactions.empty:
        return transactions  # Если DataFrame пустой, возвращаем его

    # Преобразуем строку даты в формат datetime
    date = pd.to_datetime(date, errors='coerce')

    if pd.isna(date):
        raise ValueError("Некорректный формат даты")

    # Фильтруем транзакции по дате
    filtered_transactions = transactions[transactions['date'] == date]
    return filtered_transactions


# Настройка логирования
logger = logging.getLogger("utils.log")
file_handler = logging.FileHandler("main.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

# Путь к файлу
file_path = str(Path(__file__).resolve().parent.parent / "data" / "operations.xlsx")
data_frame = read_excel(file_path)


def main(date: str, df_transactions: pd.DataFrame, stocks: list, currency: list):
    """Функция создающая JSON ответ для страницы главная"""
    logger.info("Начало работы главной функции (main)")
    final_list = filter_by_date(date, df_transactions)
    greeting = greetings()
    cards = for_each_card(final_list)
    top_trans = top_five_transaction(final_list)
    stocks_prices = get_price_stock(stocks)
    currency_r = currency_rates(currency)
    logger.info("Создание JSON ответа")
    result = [{
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_trans,
        "currency_rates": currency_r,
        "stock_prices": stocks_prices,
    }]
    date_json = json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )
    logger.info("Завершение работы главной функции (main)")
    return date_json
