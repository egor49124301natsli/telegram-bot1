FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y build-essential

# Создаём рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной проект
COPY . .

# Запускаем FastAPI-приложение через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
