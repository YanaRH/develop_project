import json
import logging
import csv as pd  # Импортируем pandas

from src.decorators import decorator_search

logger = logging.getLogger("services.log")
file_handler = logging.FileHandler("services.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


@decorator_search
def simple_search(my_list: pd.DataFrame, string_search: str) -> str:
    """Функция поиска по переданной строке"""
    result = []
    logger.info("Начало работы функции (simple_search)")

    if string_search == '':
        return json.dumps(result, indent=4, ensure_ascii=False)

    # Фильтрация данных
    for index, row in my_list.iterrows():
        if (
                row["Описание"] == "nan" or isinstance(row["Описание"], float) or
                row["Категория"] == "nan" or isinstance(row["Категория"], float)
        ):
            continue
        elif string_search in row["Описание"] or string_search in row["Категория"]:
            result.append(row.to_dict())  # Преобразуем строку DataFrame в словарь

    logger.info("Конец работы функции (simple_search)")
    data_json = json.dumps(result, indent=4, ensure_ascii=False)

    return data_json
