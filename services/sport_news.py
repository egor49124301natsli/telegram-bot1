import os
import requests

API_ODDS_KEY = os.getenv("API_ODDS_KEY")
API_SPORTS_ALT = os.getenv("API_SPORTS_ALT")

def get_latest_sport_news(limit=5):
    """
    Получает свежие новости по спорту через TheOddsAPI или альтернативный API.
    Если оба недоступны — возвращает резервное сообщение.
    """
    # Пример получения новостей через TheOddsAPI
    if API_ODDS_KEY:
        url = f"https://api.the-odds-api.com/v4/sports/?apiKey={API_ODDS_KEY}"
        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            if isinstance(data, list):
                # Возвращаем названия/описания доступных спортивных событий
                return [item.get("title", "") for item in data[:limit]]
        except Exception:
            pass

    # Альтернативный спорт-API (если есть ключ и нужный endpoint)
    if API_SPORTS_ALT:
        url = f"https://api.sportsdata.io/v4/sports/news?apiKey={API_SPORTS_ALT}"
        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            if isinstance(data, list):
                return [item.get("Title", "") for item in data[:limit]]
        except Exception:
            pass

    return ["Нет спортивных новостей с доступных API."]
