from elasticsearch import Elasticsearch
import psycopg2
from psycopg2.extras import DictCursor
import os


def main():
    pg_conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )

    es = Elasticsearch(
        hosts=[f"{os.getenv('ES_SCHEMA')}{os.getenv('ES_HOST')}:{os.getenv('ES_PORT')}"]
    )

    with pg_conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("""
            SELECT
                id,
                name,
                description
            FROM content.genre
        """)
        rows = cursor.fetchall()

        print(f"Fetched genres from Postgres: {len(rows)}")
        if rows:
            print("First row:", dict(rows[0]))

        for row in rows:
            print("Indexing genre:", row["id"], row["name"])
            es.index(
                index="genres",
                id=str(row["id"]),
                document={
                    "id": str(row["id"]),
                    "name": row["name"],
                    "description": row["description"],
                },
            )

    pg_conn.close()


if __name__ == "__main__":
    main()
