FROM python:3.11-slim

# Установка зависимостей системы (опционально, если нужны)
RUN apt-get update && apt-get install -y build-essential

# Установка зависимостей Python
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
