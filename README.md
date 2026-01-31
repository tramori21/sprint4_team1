## Как проверить проект

1. Склонировать репозиторий
2. Перейти в папку проекта
3. Создать файл окружения:
   cp .env.example .env
4. Запустить проект:
   docker compose up -d --build
5. Проверить логи ETL:
   docker compose logs etl

## Проверки

Elasticsearch:
- http://localhost:9200/movies/_count
- http://localhost:9200/genres/_count
- http://localhost:9200/persons/_count

API:
- http://localhost:8000/api/v1/films

## Восстановление базы данных

Готовый дамп PostgreSQL:
postgres/dump.sql
