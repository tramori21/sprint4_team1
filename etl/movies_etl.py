import os
from elasticsearch import Elasticsearch
from etl.postgres_reader import PostgresReader


def run():
    dsn = {
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT"),
    }

    es = Elasticsearch(
        hosts=[f"{os.getenv('ES_SCHEMA')}{os.getenv('ES_HOST')}:{os.getenv('ES_PORT')}"]
    )

    if es.indices.exists(index="movies"):
        es.indices.delete(index="movies")

    es.indices.create(
        index="movies",
        settings={"refresh_interval": "1s"},
        mappings={
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "title": {"type": "text"},
                "rating": {"type": "float"},
                "genres": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "name": {"type": "keyword"}
                    }
                },
                "persons": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "full_name": {"type": "keyword"},
                        "role": {"type": "keyword"}
                    }
                }
            }
        }
    )

    reader = PostgresReader(dsn)

    films = reader.fetch_all(
        """
        SELECT
            fw.id,
            fw.title,
            fw.rating,
            COALESCE(
                json_agg(DISTINCT jsonb_build_object(
                    'id', g.id,
                    'name', g.name
                )) FILTER (WHERE g.id IS NOT NULL),
                '[]'
            ) AS genres,
            COALESCE(
                json_agg(DISTINCT jsonb_build_object(
                    'id', p.id,
                    'full_name', p.full_name,
                    'role', pfw.role
                )) FILTER (WHERE p.id IS NOT NULL),
                '[]'
            ) AS persons
        FROM content.film_work fw
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        GROUP BY fw.id;
        """
    )

    for film in films:
        es.index(
            index="movies",
            id=str(film["id"]),
            document={
                "id": str(film["id"]),
                "title": film["title"],
                "rating": film["rating"],
                "genres": film["genres"],
                "persons": film["persons"],
            }
        )

    print(f"Movies indexed: {len(films)}")
