import os
import json
import time
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import ParseMode
from dotenv import load_dotenv

from services.translator import translate
from services.binance_api import get_binance_price
from services.news import get_crypto_news, get_latest_sport_news
from services.anti_spam import AntiSpamMiddleware
from database.session import add_user, get_all_users
from handlers import users, admin, premium
from handlers.admin import ADMIN_IDS, CHANNELS

# Загружаем .env
load_dotenv()

DEEP_API_KEY = os.getenv('DEEPL_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CMC_API_KEY = os.getenv("CMC_API_KEY")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
SPORTS_API_KEY = os.getenv("SPORTS_API_KEY")

# Создаём бота и диспетчер
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(AntiSpamMiddleware())  # Подключаем антиспам

# Локализация
class Localization:
    def __init__(self):
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        for filename in os.listdir('locales'):
            if filename.endswith('.json'):
                lang = filename.split('.')[0]
                with open(f'locales/{filename}', 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)

    def get(self, key, lang, default=None):
        return self.translations.get(lang, {}).get(key, default)

i18n = Localization()

# Регистрация всех хэндлеров
users.register_handlers(dp)
admin.register_handlers(dp)
premium.register_handlers(dp)

# Криптовалютные команды
@dp.message_handler(commands=['btc', 'eth', 'ton', 'xrp'])
async def get_crypto_price(message: types.Message):
    crypto = message.get_command().replace("/", "").strip().lower()
    mapping = {
        "btc": "BTCUSDT",
        "eth": "ETHUSDT",
        "ton": "TONUSDT",
        "xrp": "XRPUSDT"
    }
    if crypto in mapping:
        price = get_binance_price(mapping[crypto])
        await message.answer(f"{crypto.upper()}/USDT: {price}")
    else:
        await message.answer("❌ Неверная команда. Используйте: /btc, /eth, /ton, /xrp")

# Новости
@dp.message_handler(commands=['news', 'sportnews'])
async def get_news(message: types.Message):
    if message.get_command() == '/news':
        news = get_crypto_news()
    else:
        news = get_latest_sport_news()

    if not news:
        await message.answer("No latest news.")
    else:
        for n in news:
            await message.answer(n)

# Подписка
@dp.message_handler(commands=['subscribe'])
async def subscribe_user(message: types.Message):
    user_id = message.from_user.id
    # Логика подписки (предположительно добавление в базу)
    await message.answer("✅ You are now subscribed to premium features.")

# Проверка API-ключей и каналов
@dp.message_handler(commands=['check_config'])
async def check_config(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Access denied.")
        return

    keys = {
        "DEEPL_API_KEY": DEEP_API_KEY,
        "BINANCE_API_KEY": BINANCE_API_KEY,
        "SPORTS_API_KEY": SPORTS_API_KEY,
    }

    report = ['🛠 <b>API Keys:</b>']
    for name, val in keys.items():
        report.append(f"{name}: {'✅' if val != 'xxx' else '❌'}")

    report.append("\n<b>Channels:</b>")
    for lang, channel_id in CHANNELS.items():
        report.append(f"{lang}: {channel_id}")

    report.append("\n<b>Translations (Hello):</b>")
    for lang in CHANNELS.keys():
        translated = translate("Hello", lang)
        report.append(f"{lang}: {translated or '❌ Error'}")

    await message.answer("\n".join(report))

# Рассылка
@dp.message_handler(commands=['broadcast'])
async def broadcast_command(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Access denied.")
        return

    text = message.get_args()
    if not text:
        await message.answer("Please provide text for broadcast: /broadcast Your text")
        return

    user_ids = get_all_users()
    sent = 0
    for uid in user_ids:
        try:
            await message.bot.send_message(uid, text)
            sent += 1
        except Exception as e:
            print(f"Failed to send to {uid}: {e}")
            continue

    await message.answer(f"✅ Sent to {sent} users.")

# Сброс вебхука на старте
async def on_startup(dp):
    await bot.delete_webhook(drop_pending_updates=True)
    print("🚀 Webhook удалён, начинаем polling.")

# Запуск
if __name__ == "__main__":
    print("✅ Бот готов к запуску.")
    if os.getenv("RENDER") or os.getenv("RUN_BOT") == "1":
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    else:
        print("⚠️ Локальный запуск отключён (ожидается запуск на Render).")
