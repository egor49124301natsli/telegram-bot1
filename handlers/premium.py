from aiogram import types
from aiogram.dispatcher import Dispatcher
from services.stripe_pay import get_stripe_link

async def premium_command(message: types.Message):
    text = (
        "<b>Премиум-доступ:</b>\n"
        "— 1 день — /buy_1day\n"
        "— 1 месяц — /buy_1month\n"
        "— 3 месяца — /buy_3month\n"
        "— 1 прогноз — /buy_predict\n\n"
        "После оплаты отправьте /activate для активации доступа."
    )
    await message.answer(text)

async def buy_1day(message: types.Message):
    link = get_stripe_link("1day")
    await message.answer(f"Оплатить 1 день доступа:\n{link}")

async def buy_1month(message: types.Message):
    link = get_stripe_link("1month")
    await message.answer(f"Оплатить 1 месяц доступа:\n{link}")

async def buy_3month(message: types.Message):
    link = get_stripe_link("3month")
    await message.answer(f"Оплатить 3 месяца доступа:\n{link}")

async def buy_predict(message: types.Message):
    link = get_stripe_link("predict")
    await message.answer(f"Оплатить 1 прогноз:\n{link}")

async def activate_premium(message: types.Message):
    # Здесь логика активации: флаг в базе/файле/redis
    await message.answer("✅ Доступ к премиум-функциям активирован вручную (заглушка).")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(premium_command, commands=['premium'])
    dp.register_message_handler(buy_1day, commands=['buy_1day'])
    dp.register_message_handler(buy_1month, commands=['buy_1month'])

