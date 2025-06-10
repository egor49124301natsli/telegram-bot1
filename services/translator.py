import os
import requests
from dotenv import load_dotenv

load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def translate_with_deepl(text, target_lang):
    url = "https://api-free.deepl.com/v2/translate"
    try:
        if not DEEPL_API_KEY:
            raise ValueError("DEEPL key missing")
        response = requests.post(url, data={
            "auth_key": DEEPL_API_KEY,
            "text": text,
            "target_lang": target_lang.upper()
        })
        response.raise_for_status()
        return response.json()["translations"][0]["text"]
    except Exception as e:
        print("DeepL failed:", e)
        return None

def translate_with_google(text, target_lang):
    try:
        if not GOOGLE_API_KEY:
            raise ValueError("Google key missing")
        url = f"https://translation.googleapis.com/language/translate/v2"
        response = requests.post(url, params={
            "q": text,
            "target": target_lang,
            "key": GOOGLE_API_KEY
        })
        response.raise_for_status()
        return response.json()["data"]["translations"][0]["translatedText"]
    except Exception as e:
        print("Google failed:", e)
        return None

def translate(text, target_lang):
    result = translate_with_deepl(text, target_lang)
    if result:
        return result
    return translate_with_google(text, target_lang)
