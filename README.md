# telbot_test

Для запуска бота необходимо:
Тестовый бот доступен по @ART_999888_BOT

Локальный запуск:
1. Создать .env файл согласно паттерну "env.sample_local"  и прописать в него токен бота
2. pip install -r requirements.txt
3. python -m bot

Запуск через docker-compose:
1. Создать .env файл согласно паттерну "env.sample_docker"  и прописать в него токен бота
2. docker-compose up --build 

**главное отличие в хосте redis для локального и докер запуска (localhost и redis соответсвенно)