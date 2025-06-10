import time
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from handlers.admin import ADMIN_IDS  # Список админов

class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self, limit_seconds: int = 5):
        super().__init__()
        self.limit = limit_seconds
        self.last_message_time = {}

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        now = time.time()

        # ✅ Администраторы — без ограничений
        if user_id in ADMIN_IDS:
            return

        banned_words = ["казино", "виза", "вк", "биткоин", "продажа", "обмен"]

        # ⚠️ Антифлуд
        if user_id in self.last_message_time:
            if now - self.last_message_time[user_id] < self.limit:
                print(f"[ ⚡️ FLOOD ] ID: {user_id}")
                await message.answer("🚫 Пожалуйста, не флуди.")
                raise Exception("Flood detected")

        # 🔒 Запрещённые слова
        for word in banned_words:
            if word.lower() in message.text.lower():
                print(f"[ ❌ SPAM ] ID: {user_id} — слово: {word}")
                await message.answer("🚫 Ваше сообщение содержит запрещённые слова.")
                raise Exception("Banned word detected")

        self.last_message_time[user_id] = now
