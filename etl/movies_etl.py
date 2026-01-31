from elasticsearch import Elasticsearch, helpers
from psycopg2.extras import RealDictCursor
import psycopg2
import os

BATCH_SIZE = 1000


def get_pg_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        cursor_factory=RealDictCursor,
    )


def get_es_client():
    return Elasticsearch(hosts=["http://elasticsearch:9200"])


def fetch_movies_batch(cursor, offset):
    cursor.execute(
        """
        SELECT
            fw.id,
            fw.title,
            fw.description,
            fw.rating,
            fw.creation_date,
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
        LEFT JOIN content.genre_film_work gfw ON fw.id = gfw.film_work_id
        LEFT JOIN content.genre g ON gfw.genre_id = g.id
        LEFT JOIN content.person_film_work pfw ON fw.id = pfw.film_work_id
        LEFT JOIN content.person p ON pfw.person_id = p.id
        GROUP BY fw.id
        ORDER BY fw.id
        LIMIT %s OFFSET %s;
        """,
        (BATCH_SIZE, offset),
    )
    return cursor.fetchall()


def generate_actions(movies):
    for movie in movies:
        yield {
            "_index": "movies",
            "_id": movie["id"],
            "_source": {
                "id": movie["id"],
                "title": movie["title"],
                "description": movie["description"],
                "rating": movie["rating"],
                "creation_date": movie["creation_date"],
                "genres": movie["genres"],
                "persons": movie["persons"],
            },
        }


def run():
    pg_conn = get_pg_connection()
    es = get_es_client()

    if not es.indices.exists(index="movies"):
        es.indices.create(index="movies")

    offset = 0
    total_indexed = 0

    with pg_conn.cursor() as cursor:
        while True:
            movies = fetch_movies_batch(cursor, offset)
            if not movies:
                break

            helpers.bulk(es, generate_actions(movies))
            total_indexed += len(movies)
            offset += BATCH_SIZE

            print(f"Movies indexed: {total_indexed}")

    pg_conn.close()
