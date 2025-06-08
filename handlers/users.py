from aiogram import types
from aiogram.dispatcher import Dispatcher
from services.binance_api import get_binance_price
from services.news import get_crypto_news
from services.sport_news import get_latest_sport_news
from database.session import add_user

async def start_command(message: types.Message):
    add_user(message.from_user.id)
    await message.answer(
        "👋 Добро пожаловать в Crypto-Bot!\n\n"
        "Доступны:\n"
        "— Курсы криптовалют (/btc, /eth, /ton, /xrp)\n"
        "— Крипто-новости (/news)\n"
        "— Спортивные новости (/sportnews)\n"
        "— Прогнозы и аналитика (премиум)\n"
        "Используйте меню или команды для взаимодействия."
    )

async def btc_command(message: types.Message):
    add_user(message.from_user.id)
    price = get_binance_price("BTCUSDT")
    await message.answer(f"Курс BTC/USDT на Binance: <b>{price}</b>")

async def eth_command(message: types.Message):
    add_user(message.from_user.id)
    price = get_binance_price("ETHUSDT")
    await message.answer(f"Курс ETH/USDT на Binance: <b>{price}</b>")

async def ton_command(message: types.Message):
    add_user(message.from_user.id)
    price = get_binance_price("TONUSDT")
    await message.answer(f"Курс TON/USDT на Binance: <b>{price}</b>")

async def xrp_command(message: types.Message):
    add_user(message.from_user.id)
    price = get_binance_price("XRPUSDT")
    await message.answer(f"Курс XRP/USDT на Binance: <b>{price}</b>")

async def news_command(message: types.Message):
    add_user(message.from_user.id)
    news = get_crypto_news()
    if not news:
        await message.answer("Нет свежих новостей на данный момент.")
    else:
        for n in news:
            await message.answer(n)

async def sportnews_command(message: types.Message):
    add_user(message.from_user.id)
    news = get_latest_sport_news()
    if not news:
        await message.answer("Нет свежих спортивных новостей на данный момент.")
    else:
        for n in news:
            await message.answer(n)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
    dp.register_message_handler(btc_command, commands=['btc'])
    dp.register_message_handler(eth_command, commands=['eth'])
    dp.register_message_handler(ton_command, commands=['ton'])
    dp.register_message_handler(xrp_command, commands=['xrp'])
    dp.register_message_handler(news_command, commands=['news'])
    dp.register_message_handler(sportnews_command, commands=['sportnews'])
