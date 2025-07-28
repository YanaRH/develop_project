from pathlib import Path
import pandas as pd  # Импортируем pandas
from src.utils import fetch_data_from_file
from src.views import filter_by_date

file_path = str(Path(__file__).resolve().parent.parent) + "\\data\\operations.xlsx"
my_list = fetch_data_from_file(file_path)  # Предполагается, что эта функция возвращает DataFrame
empty_list = pd.DataFrame()  # Заменили пустой список на пустой DataFrame


def test_filter_by_date():
    """Тестирование функции фильтра от заданной даты"""
    expected_result = [
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -228.0, 'Валюта платежа': 'RUB',
         'Категория': 'Супермаркеты', 'Описание': 'Колхоз', 'Номер карты': '*4556'},
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -110.0, 'Валюта платежа': 'RUB',
         'Категория': 'Фастфуд', 'Описание': 'Mouse Tail', 'Номер карты': '*4556'},
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -525.0, 'Валюта платежа': 'RUB',
         'Категория': 'Одежда и обувь', 'Описание': 'WILDBERRIES', 'Номер карты': '*4556'}
    ]

    # Преобразуем ожидаемый результат в DataFrame для сравнения
    expected_df = pd.DataFrame(expected_result)

    # Сравниваем результат функции с ожидаемым результатом
    assert filter_by_date("2021.11.01", my_list).equals(expected_df)


def test_filter_by_date_emp_att():
    """Тестирование функции фильтра от заданной даты с пустыми атрибутами"""
    assert filter_by_date("", my_list).empty  # Проверяем, что возвращается пустой DataFrame
    assert not filter_by_date("2021.11.01", my_list).empty  # Проверяем, что результат не пустой
    assert filter_by_date("", empty_list).empty  # Проверяем, что возвращается пустой DataFrame
