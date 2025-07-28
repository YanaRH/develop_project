import json
from pathlib import Path
import pandas as pd  # Импортируем pandas

from src.services import simple_search
from src.utils import fetch_data_from_file  # Замена read_excel на fetch_data_from_file

# Используем Path для создания пути к файлу
file_path = Path(__file__).resolve().parent.parent / "data" / "operations.xlsx"
my_list = fetch_data_from_file(file_path)  # Заменили read_excel на fetch_data_from_file
empty_list = pd.DataFrame()  # Заменили пустой список на пустой DataFrame

def test_services_works():
    """Тестирование функции простой поиск в обычных условиях"""
    expected_result = [
        {
            "Дата платежа": "31.12.2021",
            "Статус": "OK",
            "Сумма платежа": -564.0,
            "Валюта платежа": "RUB",
            "Категория": "Различные товары",
            "Описание": "Ozon.ru",
            "Номер карты": "*5091"
        },
        {
            "Дата платежа": "20.12.2021",
            "Статус": "OK",
            "Сумма платежа": 421.0,
            "Валюта платежа": "RUB",
            "Категория": "Различные товары",
            "Описание": "Ozon.ru",
            "Номер карты": "*7197"
        },
        {
            "Дата платежа": "14.12.2021",
            "Статус": "OK",
            "Сумма платежа": -421.0,
            "Валюта платежа": "RUB",
            "Категория": "Различные товары",
            "Описание": "Ozon.ru",
            "Номер карты": "*7197"
        },
        {
            "Дата платежа": "21.10.2021",
            "Статус": "OK",
            "Сумма платежа": -119.0,
            "Валюта платежа": "RUB",
            "Категория": "Различные товары",
            "Описание": "Ozon.ru",
            "Номер карты": "*7197"
        },
        {
            "Дата платежа": "04.10.2020",
            "Статус": "OK",
            "Сумма платежа": -750.0,
            "Валюта платежа": "RUB",
            "Категория": "Различные товары",
            "Описание": "Ozon.ru",
            "Номер карты": "*7197"
        }
    ]

    # Преобразуем ожидаемый результат в DataFrame для сравнения
    expected_df = pd.DataFrame(expected_result)

    # Сравниваем результат функции с ожидаемым результатом
    assert simple_search(my_list, "Ozon.ru") == expected_df.to_dict(orient='records')

def test_services_empty_attribute():
    """Тестирование функции простой поиск, с пустыми атрибутами """
    assert simple_search(empty_list, "Ozon.ru") == []
    assert simple_search(my_list, "") == []
