from aiogram import types
from aiogram.dispatcher import Dispatcher
from services.binance_api import get_binance_price
from services.news import get_crypto_news
from services.sport_news import get_latest_sport_news
from database.session import add_user
from bot import i18n
from services.translator import translate


async def start_command(message: types.Message):
    add_user(message.from_user.id)
    lang = message.from_user.language_code or "en"
    text = i18n.get("welcome", lang)
    await message.answer(text)


async def btc_command(message: types.Message):
    add_user(message.from_user.id)
    lang = message.from_user.language_code or "en"
    price = get_binance_price("BTCUSDT")
    text = i18n.get("price_btc", lang).format(price=price)
    await message.answer(text)


async def eth_command(message: types.Message):
    add_user(message.from_user.id)
    lang = message.from_user.language_code or "en"
    price = get_binance_price("ETHUSDT")
    text = i18n.get("price_eth", lang).format(price=price)
    await message.answer(text)


async def ton_command(message: types.Message):
    add_user(message.from_user.id)
    lang = message.from_user.language_code or "en"
    price = get_binance_price("TONUSDT")
    text = i18n.get("price_ton", lang).format(price=price)
    await message.answer(text)


async def xrp_command(message: types.Message):
    add_user(message.from_user.id)
    lang = message.from_user.language_code or "en"
    price = get_binance_price("XRPUSDT")
    text = i18n.get("price_xrp", lang).format(price=price)
    await message.answer(text)


async def news_command(message: types.Message):
    add_user(message.from_user.id)
    lang = message.from_user.language_code or "en"
    news = get_crypto_news()

    if not news:
        await message.answer("Нет свежих новостей на данный момент.")
    else:
        for n in news:
            translated = translate(n, lang)
            await message.answer(translated or n)


async def sportnews_command(message: types.Message):
    add_user(message.from_user.id)
    lang = message.from_user.language_code or "en"
    news = get_latest_sport_news()

    if not news:
        await message.answer("Нет свежих спортивных новостей на данный момент.")
    else:
        for n in news:
            translated = translate(n, lang)
            await message.answer(translated or n)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
    dp.register_message_handler(btc_command, commands=['btc'])
    dp.register_message_handler(eth_command, commands=['eth'])
    dp.register_message_handler(ton_command, commands=['ton'])
    dp.register_message_handler(xrp_command, commands=['xrp'])
    dp.register_message_handler(news_command, commands=['news'])
    dp.register_message_handler(sportnews_command, commands=['sportnews'])
