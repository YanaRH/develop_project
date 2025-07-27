import json
import logging
from pathlib import Path

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
    return []  # Возвращаем пустой список как заглушку

def top_five_transaction(transactions):
    return []

# Импортируем заглушку для filter_by_date
def filter_by_date(date, transactions):
    return transactions  # Возвращаем все транзакции как заглушку

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

def main(date: str, df_transactions, stocks: list, currency: list):
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
