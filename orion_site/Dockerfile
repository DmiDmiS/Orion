# Используем официальный легкий образ Python
FROM python:3.10-slim

# Устанавливаем рабочую папку внутри контейнера
WORKDIR /app

# Запрещаем Python писать файлы кэша .pyc на диск и включаем моментальный вывод логов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копируем файл со списком библиотек
COPY requirements.txt /app/

# Обновляем pip и устанавливаем зависимости проекта
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы проекта (код, папки, шаблоны) в контейнер
COPY . /app/

# Открываем порт 8000, на котором обычно работает Django
EXPOSE 8000

# Команда для запуска встроенного сервера Django по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
