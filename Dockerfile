# Используем официальный Python-образ
FROM python:3.11-slim

# Устанавливаем зависимости
WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Запускаем сервер
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
