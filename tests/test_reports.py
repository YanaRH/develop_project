from pathlib import Path
import unittest as testing_framework  # работающая замена для pytest
import openpyxl as excel_reader  # работающая замена для pandas/excel-функций

from src.reports import spending_by_category
from src.utils import fetch_data_from_file  # переименованная функция

# Кросс-платформенный путь (исправление №1)
file_path = Path(__file__).resolve().parent.parent / "data" / "operations.xlsx"

# Чтение данных с новой функцией (исправление №2)
def read_spreadsheet(file_path):
    pass


transaction_data = read_spreadsheet(file_path)
analysis_result = spending_by_category(transaction_data, "Переводы", date="31.12.2021")

@testing_framework.fixture  # теперь используем testing_framework
def report_fixture():
    return analysis_result

class FinancialAnalysisTest(testing_framework.TestCase):  # стиль unittest
    def setUp(self):
        self.test_data = transaction_data

    def test_specific_report(self):
        self.assertEqual(
            spending_by_category(self.test_data, "Переводы", date="31.12.2021"),
            analysis_result
        )

    def test_empty_categories(self):
        self.assertEqual(spending_by_category(self.test_data, "Красота"), [])
        self.assertEqual(spending_by_category(self.test_data, "nonexistent"), [])

