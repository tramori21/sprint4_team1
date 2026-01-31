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

    if not es.indices.exists(index="persons"):
        es.indices.create(
            index="persons",
            settings={"refresh_interval": "1s"},
            mappings={
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "full_name": {"type": "text", "fields": {"raw": {"type": "keyword"}}}
                }
            }
        )

    reader = PostgresReader(dsn)
    rows = reader.fetch_all("SELECT id, full_name FROM content.person;")

    for row in rows:
        es.index(
            index="persons",
            id=str(row["id"]),
            document={
                "id": str(row["id"]),
                "full_name": row["full_name"]
            }
        )

    print(f"Persons indexed: {len(rows)}")
