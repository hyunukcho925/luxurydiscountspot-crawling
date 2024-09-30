import requests
from bs4 import BeautifulSoup
from datetime import datetime, time
import pytz

class CurrencyConverter:
    def __init__(self):
        self.rates = {
            'EUR': 1400,  # 1 EUR = 1400 KRW (예시 값, 실제 환율로 업데이트 필요)
            'USD': 1300,  # 1 USD = 1300 KRW (예시 값, 실제 환율로 업데이트 필요)
            # 다른 통화들 추가
        }

    def convert_to_krw(self, amount, from_currency):
        if from_currency == 'KRW':
            return amount
        if from_currency in self.rates:
            return round(amount * self.rates[from_currency])
        raise ValueError(f"지원하지 않는 통화: {from_currency}")

currency_converter = CurrencyConverter()