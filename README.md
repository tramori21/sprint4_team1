## Как проверить проект

1. Склонировать репозиторий
2. Запустить:
   docker compose up -d --build
3. Проверить логи ETL:
   docker compose logs etl
4. Проверить Elasticsearch:
   http://localhost:9200/movies/_count
   http://localhost:9200/genres/_count
   http://localhost:9200/persons/_count

Для восстановления БД:
postgres/dump.sql
