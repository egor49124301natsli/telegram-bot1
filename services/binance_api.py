import requests
import os

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BASE_URL = "https://api.binance.com"

def get_binance_price(symbol="BTCUSDT"):
    """
    Получить текущий курс криптовалюты с Binance (например, BTC/USDT).
    symbol — пара, например 'BTCUSDT', 'ETHUSDT', 'TONUSDT'
    """
    endpoint = f"/api/v3/ticker/price?symbol={symbol}"
    url = BASE_URL + endpoint
    response = requests.get(url)
    data = response.json()
    return data.get("price")

def get_binance_24h_stats(symbol="BTCUSDT"):
    """
    Получить 24-часовую статистику по паре.
    """
    endpoint = f"/api/v3/ticker/24hr?symbol={symbol}"
    url = BASE_URL + endpoint
    response = requests.get(url)
    data = response.json()
    return data
