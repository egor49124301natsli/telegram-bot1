import requests

# --- Маппинг символов для CoinGecko и CoinCap ---
COINGECKO_MAP = {
    "BTCUSDT": ("bitcoin", "tether"),
    "ETHUSDT": ("ethereum", "tether"),
    "TONUSDT": ("toncoin", "tether"),
    "XRPUSDT": ("ripple", "tether"),
}

COINCAP_MAP = {
    "BTCUSDT": "bitcoin",
    "ETHUSDT": "ethereum",
    "TONUSDT": "toncoin",
    "XRPUSDT": "ripple",
}

# --- Источник 1: Binance ---
def get_price_binance(symbol: str) -> float:
    symbol = symbol.upper()
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"❌ Binance API error for {symbol}: {e}")
        return 0.0

# --- Источник 2: CoinGecko ---
def get_price_coingecko(symbol: str) -> float:
    symbol = symbol.upper()
    pair = COINGECKO_MAP.get(symbol)
    if not pair:
        return 0.0
    coin_id, vs_currency = pair
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={vs_currency}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data[coin_id][vs_currency])
    except Exception as e:
        print(f"❌ CoinGecko error for {symbol}: {e}")
        return 0.0

# --- Источник 3: CoinCap ---
def get_price_coincap(symbol: str) -> float:
    symbol = symbol.upper()
    asset = COINCAP_MAP.get(symbol)
    if not asset:
        return 0.0
    url = f"https://api.coincap.io/v2/assets/{asset}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data["data"]["priceUsd"])
    except Exception as e:
        print(f"❌ CoinCap error for {symbol}: {e}")
        return 0.0

# --- Главная функция ---
def get_crypto_price(symbol: str) -> float:
    for source in (get_price_binance, get_price_coingecko, get_price_coincap):
        price = source(symbol)
        if price > 0:
            print(f"✅ {symbol}: найдено через {source.__name__} = {price}")
            return price
    print(f"❌ {symbol}: ни один источник не дал цену.")
    return 0.0
