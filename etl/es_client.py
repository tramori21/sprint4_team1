import time
from elasticsearch import Elasticsearch, helpers

from etl.config import ES


class ElasticsearchClient:
    def __init__(self):
        self.client = Elasticsearch(
            hosts=[{'host': ES.host, 'port': ES.port, 'scheme': 'http'}]
        )
        self._wait_for_es()

    def _wait_for_es(self):
        for _ in range(30):
            try:
                if self.client.ping():
                    return
            except Exception:
                pass
            time.sleep(1)
        raise RuntimeError("Elasticsearch is not available")

    def recreate_movies_index(self):
        index_name = "movies"

        if self.client.indices.exists(index=index_name):
            self.client.indices.delete(index=index_name)

        body = {
            "settings": {
                "refresh_interval": "1s"
            },
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "title": {
                        "type": "text",
                        "fields": {
                            "raw": {"type": "keyword"}
                        }
                    },
                    "description": {"type": "text"},
                    "rating": {"type": "float"},
                    "type": {"type": "keyword"},
                    "genres": {
                        "type": "nested",
                        "properties": {
                            "id": {"type": "keyword"},
                            "name": {
                                "type": "text",
                                "fields": {
                                    "raw": {"type": "keyword"}
                                }
                            }
                        }
                    },
                    "actors": {
                        "type": "nested",
                        "properties": {
                            "id": {"type": "keyword"},
                            "name": {
                                "type": "text",
                                "fields": {
                                    "raw": {"type": "keyword"}
                                }
                            }
                        }
                    },
                    "writers": {
                        "type": "nested",
                        "properties": {
                            "id": {"type": "keyword"},
                            "name": {
                                "type": "text",
                                "fields": {
                                    "raw": {"type": "keyword"}
                                }
                            }
                        }
                    },
                    "directors": {
                        "type": "nested",
                        "properties": {
                            "id": {"type": "keyword"},
                            "name": {
                                "type": "text",
                                "fields": {
                                    "raw": {"type": "keyword"}
                                }
                            }
                        }
                    }
                }
            }
        }

        self.client.indices.create(index=index_name, body=body)

    def bulk_index_movies(self, movies: list[dict]):
        actions = (
            {
                "_index": "movies",
                "_id": movie["id"],
                "_source": movie
            }
            for movie in movies
        )

        helpers.bulk(self.client, actions)
