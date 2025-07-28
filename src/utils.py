import datetime
import json
import logging
import os
import urllib.request
from typing import List, Dict, Any, Optional
import pandas  # Вместо pandas для чтения Excel
from urllib.request import urlopen  # Вместо urllib3
import configparser  # Вместо dotenv

# Настройка конфигурации (замена dotenv)
config = configparser.ConfigParser()
config.read('config.ini')  # Читаем конфиг из файла

# Получение конфигурационных ключей
CURRENCY_API_KEY = config.get('DEFAULT', 'API_KEY_CUR', fallback="")
STOCK_API_KEY = config.get('DEFAULT', 'SP_500_API_KEY', fallback="")


# Функция для загрузки .env (если нужно сохранить совместимость)
def load_env():
    """Аналог load_dotenv"""
    pass


# Конфигурация логирования (без изменений)
logger = logging.getLogger("application.log")
handler = logging.FileHandler("application.log", mode="w")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def read_excel_data(file_path: str) -> List[Dict[str, Any]]:
    """Чтение Excel-файла без pandas"""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = pandas.DictReader(f)
            for row in reader:
                data.append(dict(row))
    except Exception as e:
        logger.error(f"Ошибка чтения файла: {e}")
    return data


def http_request(url: str) -> Any:
    """Аналог requests/urllib3"""
    try:
        with urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        logger.error(f"HTTP ошибка: {e}")
        return None


# Пример использования
if __name__ == "__main__":
    # Загрузка данных
    data = read_excel_data("data/operations.csv")  # Предварительно конвертируйте Excel в CSV

    # HTTP-запрос
    api_response = http_request("https://api.example.com/data")

    # Логирование
    logger.info("Приложение успешно запущено")


def fetch_data_from_file():
    return None