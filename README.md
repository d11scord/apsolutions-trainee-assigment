# Тестовое задание для стажера в *Аналитические программные решения*

В этом проекте реализована простая поисковая система по текстам документов. 

Данные хранятся в БД `PostgreSQL`, поисковый индекс в `ElasticSearch`.

Проект выполнен с помощью `FastAPI` и `Gino` и работает асинхронно.

Ссылка на тестовый массив данных: [[csv](https://api.onedrive.com/v1.0/shares/u!aHR0cHM6Ly8xZHJ2Lm1zL3UvcyFBdldqdXEtLW5zblNrYW8yUzVzMnpUTHpNMHBweHc_ZT1RQnJIMGQ/root/content)]

## Запуск проекта

### Запуск с помощью Docker-compose

Проверьте, что в системе установлены `Docker` и `Docker-compose`. После введите команду:
```
docker-compose up --build -d
```

Она запустит три контейнера — приложение `FastAPI`, `Elasticsearch` и `PostgreSQL`.
Ссылка может быть доступна не сразу, нужно немного времени, чтобы заполнить БД :)

После этого сервис будет доступен по ссылке [127.0.0.1:8080](http://127.0.0.1:8080).
Все методы описаны в документации `OpenAPI Swagger`, которая откроется на главной странице.

### Запуск локально

+ Убедитесь, что PostgreSQL и Elasticsearch запущены.

+ Создайте virtual env и установите зависимости:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

+ Создайте БД с нзванием `documents` и запустите скрипт из корня проекта для заполнения БД постами: 

```
alembic upgrade head
python populate.py
```

+ Запустите сервер:

```
python main.py
# или
uvicorn main:app --host 127.0.0.1 --port 8080
```

Сервис будет доступен по ссылке [127.0.0.1:8080](http://127.0.0.1:8080).

## Структура проекта

```
src
├── api                     - Список эндпоинтов.
└── store                   - Конфигурация БД и индекса, модели данных.
main.py                     - Входная точка приложения FastAPI.
populate.py                 - Скрипт для заполнения БД и индекса данными.
```

## Тесты

Запуск тестов:

```
pytest -v
```

Анализ покрытия тестами:

```
pytest --cov-report term --cov=src tests/
```
