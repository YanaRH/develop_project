import os

# Загружаем переменные окружения
db_host = os.getenv('DB_HOST')
api_key = os.getenv('API_KEY')


def main():
    # Здесь вы можете вызывать все функции вашего проекта
    print(f"DB Host: {db_host}")
    print(f"API Key: {api_key}")

    # Проверка на None
    if db_host is None:
        print("Warning: DB_HOST не установлен!")
    if api_key is None:
        print("Warning: API_KEY не установлен!")

    # Пример вызова других функций
    # result = some_function()
    # print(result)


if __name__ == "__main__":
    main()








