from __future__ import annotations

import json
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from redis.asyncio import Redis

from src.core import config


class FilmService:
    def __init__(self, es: AsyncElasticsearch, redis_client: Redis | None = None):
        self.es = es
        self.redis = redis_client
        self.index = "movies"

    async def get_by_id(self, film_id: str) -> Optional[dict]:
        cache_key = f"film:{film_id}"

        if self.redis:
            cached = await self.redis.get(cache_key)
            if cached:
                return json.loads(cached)

        try:
            doc = await self.es.get(index=self.index, id=film_id)
        except NotFoundError:
            return None

        film = {"id": doc["_id"], **doc["_source"]}

        if self.redis:
            await self.redis.set(
                cache_key,
                json.dumps(film),
                ex=config.CACHE_EXPIRE_SECONDS,
            )

        return film

    async def search(
        self,
        query: str | None = None,
        page: int = 1,
        size: int = 10,
    ) -> dict:
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^3", "description"],
                    "fuzziness": "AUTO",
                }
            } if query else {"match_all": {}},
            "from": (page - 1) * size,
            "size": size,
        }

        resp = await self.es.search(index=self.index, body=body)

        return {
            "count": resp["hits"]["total"]["value"],
            "results": [
                {"id": hit["_id"], **hit["_source"]}
                for hit in resp["hits"]["hits"]
            ],
        }
