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

    if not es.indices.exists(index="genres"):
        es.indices.create(
            index="genres",
            settings={"refresh_interval": "1s"},
            mappings={
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
                    "description": {"type": "text"}
                }
            }
        )

    reader = PostgresReader(dsn)
    rows = reader.fetch_all("SELECT id, name, description FROM content.genre;")

    for row in rows:
        es.index(
            index="genres",
            id=str(row["id"]),
            document={
                "id": str(row["id"]),
                "name": row["name"],
                "description": row["description"],
            }
        )

    print(f"Genres indexed: {len(rows)}")
