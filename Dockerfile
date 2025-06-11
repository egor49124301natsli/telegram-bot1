# Используем официальный Python-образ
FROM python:3.11-slim

# Задаём рабочую директорию внутри контейнера
WORKDIR /app

# Сначала копируем только requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное в контейнер
COPY . .

# Запускаем сервер
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
