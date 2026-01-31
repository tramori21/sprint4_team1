import psycopg2
from psycopg2.extras import DictCursor


class PostgresReader:
    def __init__(self, dsn: dict):
        self.dsn = dsn

    def fetch_all(self, query: str):
        with psycopg2.connect(**self.dsn) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
