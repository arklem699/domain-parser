# Используем базовый образ Python
FROM python:3.11

# Установка переменной окружения для запуска в непроизводственном режиме
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование зависимостей и файла requirements.txt
COPY requirements.txt /app/

# Установка зависимостей проекта
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip list

# Копирование всего проекта в контейнер
COPY . .

# Определение порта, который будет использоваться Django
EXPOSE 8000

# Команда для запуска сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]