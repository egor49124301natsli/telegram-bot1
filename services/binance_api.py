import requests

def get_binance_price(symbol: str) -> float:
    symbol = symbol.upper()  # всегда используем верхний регистр
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"✅ Ответ Binance для {symbol}: {response.text}")
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"❌ Ошибка Binance при {symbol}: {e}")
        return 0.0
