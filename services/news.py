import os
import requests

COINGECKO_KEY = os.getenv("COINGECKO_KEY")
CMC_API_KEY = os.getenv("CMC_API_KEY")

def get_crypto_news(limit=5):
    """
    Получить свежие новости по крипте с CoinMarketCap (если есть ключ).
    Если ключа нет — возвращает новости из CoinGecko.
    """
    # CoinMarketCap NEWS (приоритет)
    if CMC_API_KEY:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/news/latest"
        headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
        params = {"count": limit}
        try:
            r = requests.get(url, headers=headers, params=params, timeout=10)
            data = r.json()
            if "data" in data:
                return [item.get("title", "") + "\n" + item.get("url", "") for item in data["data"][:limit]]
        except Exception as e:
            pass

    # CoinGecko NEWS (fallback)
    url = "https://api.coingecko.com/api/v3/status_updates"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if "status_updates" in data:
            return [item.get("description", "") for item in data["status_updates"][:limit]]
    except Exception as e:
        pass

    return ["Нет новостей от CoinGecko и CoinMarketCap."]
