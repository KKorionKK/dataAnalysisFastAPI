# Сервер
## Как это запустить?
Сервер с базой данных запускаются в докере. **Перед запуском** нужно заполнить `.env` файл и изменить переменные в `docker-compose.yml` такие как `POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB` в соответствии с переменными в `.env` файле.

Файл с переменными окружения должен лежать в корне проекта рядом с файлом `app.py`.

`.env` файл должен выглядеть примерно следующим образом:
```
DB_NAME = "database_analysis"
PG_USER = "root"
PG_PASSWORD = "123gr"
DB_ADAPTER = "postgresql+asyncpg"
DB_HOST = "database"
DB_PORT = "5432"
```

## Описание
Сервер работает на **FastAPI** с использованием **SQLAlchemy** для доступа к базе данных. Для обработки файла использован **Pandas**, для тестов - **Pytest**.

Эндпоинты:
 - **/files/upload** - получает на вход *непустой* файл формата *.xlsx*
 - **/files/download/{file_id}** - получает на вход номер файла для скачивания
 - **/data** - получает на вход значения, по которым нужно вернуть данные

Примечание: 
Подразумевается, что в каком бы то ни было файле обязательно будут различные коды проекта, поэтому выбрала такая схема БД, где будет нарушаться целостность БД при совпадении кодов проектов даже из двух разных файлов. Не совсем было ясно, уникальное в рамках одного файла или в общем.
> Код проекта уникальное целое число.

