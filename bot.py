import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Импорт хендлеров
from handlers import users, admin, premium

users.register_handlers(dp)
admin.register_handlers(dp)
premium.register_handlers(dp)

if __name__ == "__main__":
    print("Бот запущен!")
    executor.start_polling(dp, skip_updates=True)
