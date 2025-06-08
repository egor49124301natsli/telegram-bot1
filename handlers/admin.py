from aiogram import types
from aiogram.dispatcher import Dispatcher

# Укажи ID своего Telegram (чтобы только ты мог пользоваться админкой)
ADMIN_IDS = [5369169032]  # <-- сюда вставь свой user_id

# Пример: рассылка всем пользователям
async def broadcast_command(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Нет доступа")
        return

    text = message.get_args()
    if not text:
        await message.answer("Укажи текст рассылки: /broadcast Ваш текст")
        return

    # Импортируй users из базы или файла
    user_ids = get_all_users()  # Эта функция должна возвращать список user_id

    sent = 0
    for uid in user_ids:
        try:
            await message.bot.send_message(uid, text)
            sent += 1
        except Exception:
            continue
    await message.answer(f"✅ Разослано {sent} сообщений.")

def get_all_users():
    # Заглушка. Здесь — твоя логика получения всех user_id (из файла, базы, redis и пр.)
    # Например, return [123456789, 987654321]
    return []

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(broadcast_command, commands=['broadcast'])
