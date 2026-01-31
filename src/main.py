from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from src.api.v1.routers import api_router
from src.core import config
from src.db import elastic, redis


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    redis.redis = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        decode_responses=True,
    )
    elastic.es = AsyncElasticsearch(
        hosts=[f"{config.ES_SCHEMA}{config.ES_HOST}:{config.ES_PORT}"]
    )


@app.on_event("shutdown")
async def shutdown():
    if redis.redis is not None:
        await redis.redis.close()

    if elastic.es is not None:
        await elastic.es.close()


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
