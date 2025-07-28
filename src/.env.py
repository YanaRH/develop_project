import os
import json
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

# 1. Создаем шаблон .env файла при его отсутствии
ENV_TEMPLATE = """# Database connection settings
DB_HOST=your_database_host
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password

# API keys
EXCHANGE_RATE_API_KEY=your_exchange_api_key
STOCK_API_KEY=your_stock_api_key

# Application settings
DEBUG=True
LOG_LEVEL=INFO
"""


def create_env_file():
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write(ENV_TEMPLATE)
        print(f"Created .env template at {env_path}")


# 2. Основной модуль приложения
class FinanceAnalyzer:
    def __init__(self):
        self.logger = self._setup_logger()
        self.data_path = Path(__file__).parent.parent / 'data'
        self.transactions = None

    def _setup_logger(self):
        logger = logging.getLogger("finance_analyzer")
        logger.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler('finance_analysis.log', mode='w')
        file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(console_handler)

        return logger

    def load_transactions(self):
        """Load transactions from Excel file"""
        excel_file = self.data_path / 'operations.xlsx'
        try:
            self.transactions = pd.read_excel(excel_file, engine='openpyxl')
            self.logger.info(f"Loaded {len(self.transactions)} transactions")
            return True
        except Exception as e:
            self.logger.error(f"Error loading transactions: {str(e)}")
            return False

    def filter_by_date(self, date_str):
        """Filter transactions by date"""
        if self.transactions is None:
            self.logger.warning("No transactions loaded")
            return None

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            filtered = self.transactions[
                pd.to_datetime(self.transactions['date']).dt.date == target_date
                ]
            self.logger.info(f"Found {len(filtered)} transactions for {date_str}")
            return filtered
        except Exception as e:
            self.logger.error(f"Error filtering by date: {str(e)}")
            return None

    def analyze_cards(self, transactions):
        """Analyze card transactions"""
        if transactions is None or transactions.empty:
            return []

        # Group by card and calculate sums
        cards_analysis = (transactions
                          .groupby('card_number')
                          .agg({'amount': ['sum', 'count']})
                          .reset_index())

        cards_analysis.columns = ['card_number', 'total_amount', 'transaction_count']
        return cards_analysis.to_dict('records')

    def get_top_transactions(self, transactions, n=5):
        """Get top n transactions by amount"""
        if transactions is None or transactions.empty:
            return []

        return (transactions
                .sort_values('amount', ascending=False)
                .head(n)
                .to_dict('records'))

    def get_all_analysis(self, date_str):
        """Run all analysis functionalities"""
        self.logger.info("Starting complete analysis")

        if not self.load_transactions():
            return None

        filtered = self.filter_by_date(date_str)
        if filtered is None:
            return None

        return {
            "cards_analysis": self.analyze_cards(filtered),
            "top_transactions": self.get_top_transactions(filtered),
            "date": date_str,
            "total_transactions": len(filtered)
        }


# 3. Модуль для запуска всех функциональностей
def run_full_analysis():
    """Main function to run all application functionalities"""
    create_env_file()  # Ensure .env exists

    analyzer = FinanceAnalyzer()
    date_str = input("Enter date for analysis (YYYY-MM-DD): ")

    result = analyzer.get_all_analysis(date_str)

    if result:
        print("\nAnalysis Results:")
        print(f"Date: {result['date']}")
        print(f"Total transactions: {result['total_transactions']}")

        print("\nCards Analysis:")
        for card in result['cards_analysis']:
            print(f"Card: {card['card_number']} - "
                  f"Total: {card['total_amount']} - "
                  f"Transactions: {card['transaction_count']}")

        print("\nTop Transactions:")
        for i, trans in enumerate(result['top_transactions'], 1):
            print(f"{i}. Amount: {trans['amount']} - "
                  f"Description: {trans['description']}")
    else:
        print("Analysis failed. Check logs for details.")


if __name__ == "__main__":
    run_full_analysis()









