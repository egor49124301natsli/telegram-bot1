from aiogram import types
from aiogram.dispatcher import Dispatcher
import os
from services.translator import translate
from handlers.anti_spam import AntiSpamMiddleware

# ID админов (вставь сюда свои Telegram user_id)
ADMIN_IDS = [5369160932]  # Пример ID

# Каналы с языками
CHANNELS = {
    'ru': int(os.getenv("CHANNEL_RU_ID")),
    'en': int(os.getenv("CHANNEL_EN_ID")),
    'pl': int(os.getenv("CHANNEL_PL_ID")),
    'uk': int(os.getenv("CHANNEL_UK_ID")),
}

# Команда: рассылка всем пользователям
async def broadcast_command(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("\u274C Нет доступа")
        return

    text = message.get_args()
    if not text:
        await message.answer("Укажи текст рассылки: /broadcast Ваш текст")
        return

    user_ids = get_all_users()
    sent = 0
    for uid in user_ids:
        try:
            await message.bot.send_message(uid, text)
            sent += 1
        except Exception:
            continue

    await message.answer(f"\u2705 Разослано {sent} сообщений.")

# Команда: пост в каналы с переводом
async def post_command(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("\u274C Нет доступа")
        return

    original = message.get_args()
    if not original:
        await message.answer("Укажи текст для публикации: /post текст")
        return

    sent = 0
    for lang, channel_id in CHANNELS.items():
        translated = translate(original, lang)
        try:
            await message.bot.send_message(chat_id=channel_id, text=translated)
            sent += 1
        except Exception as e:
            print(f"\u274C Ошибка при отправке в канал {lang}: {e}")
            continue

    await message.answer(f"\u2705 Опубликовано в {sent} каналах.")

# Команда: проверка конфигурации
async def check_config(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("\u274C Нет доступа")
        return

    keys = {
        "DEEPL_API_KEY": os.getenv("DEEPL_API_KEY"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "COINGECKO_KEY": os.getenv("COINGECKO_KEY"),
        "BINANCE_API_KEY": os.getenv("BINANCE_API_KEY"),
        "API_FOOTBALL_KEY": os.getenv("API_FOOTBALL_KEY"),
        "API_ODDS_KEY": os.getenv("API_ODDS_KEY"),
        "API_SPORTS_ALT": os.getenv("API_SPORTS_ALT"),
    }

    report = ["\u1F510 API ключи:"]
    for name, val in keys.items():
        report.append(f"{name}: {'\u2705' if val and 'xxx' not in val else '\u274C'}")

    report.append("\n\u1F4E2 Каналы:")
    for lang, channel_id in CHANNELS.items():
        report.append(f"{lang}: {channel_id if channel_id else '\u274C'}")

    report.append("\n\u1F4AC Переводы слова 'Hello':")
    for lang in CHANNELS.keys():
        translated = translate("Hello", lang)
        report.append(f"{lang}: {translated or '\u274C Ошибка'}")

    await message.answer("\n".join(report))

# TODO: получить список пользователей из базы или файла

def get_all_users():
    # пример-заглушка
    return [5369160932]  # Добавь ID для теста или подключи базу

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(broadcast_command, commands=['broadcast'])
    dp.register_message_handler(post_command, commands=['post'])
    dp.register_message_handler(check_config, commands=['check_config'])
