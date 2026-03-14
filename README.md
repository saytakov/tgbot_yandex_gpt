Учебный PET-проект телеграмм-бот с подключенным ИИ
<hr>
Цель проекта: ознакомиться с работой c redis, docker, асинхронной библиотекой asyncio, aiogram, API сервисом YandexCloud
<hr>
Функционал проекта:<br>
Использование чата с YandexGPT для ведения чата, а также генерирования картинок по промту
<hr>
Стек проекта:<br>
Python 3.11, SQLite, Redis, Docker, YandexCloud, Aiogram3
<hr>
Запуск проекта:
Запустите сервер redis (пока локально)

Получите токены для бота и для ии в яндексе
TOKEN_BOT - токен бота
IDENTKEY - ключ идентификатор
YAGPT_API_KEY - API ключ YandexCloud
YAGPT_CATALOG_ID - айди каталога

Установите необходимые библиотеки из requirements.txt в окружение
pip install -r requirements.txt

Загрузите фикстуру dump.sql
sqlite3 app/database/db.sqlite3 < dump.sql

Запустите проект
python run.py
<hr>