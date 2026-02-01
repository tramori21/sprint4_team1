from contextlib import asynccontextmanager
from elasticsearch import AsyncElasticsearch
import redis.asyncio as redis

from core.config import settings


@asynccontextmanager
async def lifespan(app):
    app.state.es = AsyncElasticsearch(
        hosts=[f"{settings.es_schema}{settings.es_host}:{settings.es_port}"]
    )
    app.state.redis = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=True,
    )
    yield
    await app.state.es.close()
    await app.state.redis.close()
