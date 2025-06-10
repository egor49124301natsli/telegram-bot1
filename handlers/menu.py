# handlers/menu.py
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot import i18n

def get_main_menu(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton(i18n.get("price_btc", lang)),
        KeyboardButton(i18n.get("price_eth", lang)),
        KeyboardButton(i18n.get("price_ton", lang)),
        KeyboardButton(i18n.get("price_xrp", lang)),
        KeyboardButton(i18n.get("news_crypto", lang)),
        KeyboardButton(i18n.get("news_sport", lang)),
        KeyboardButton(i18n.get("change_lang", lang))
    )

async def start_command(message: types.Message):
    user_id = message.from_user.id
    lang = message.from_user.language_code or "en"
    from database.session import add_user
    add_user(user_id)

    text = i18n.get("welcome", lang)
    await message.answer(text, reply_markup=get_main_menu(lang))

async def lang_command(message: types.Message):
    lang_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("English"), KeyboardButton("русский"),
        KeyboardButton("Polski"), KeyboardButton("українська")
    )
    await message.answer("Choose your language:", reply_markup=lang_buttons)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start", "help"])
    dp.register_message_handler(lang_command, commands=["lang"])
