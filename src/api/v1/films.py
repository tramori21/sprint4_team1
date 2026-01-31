from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.services.films import FilmService


router = APIRouter()


@router.get("/films", tags=["films"])
async def films_search(
    query: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    es: AsyncElasticsearch = Depends(get_elastic),
    redis: Redis | None = Depends(get_redis),
):
    service = FilmService(es, redis)
    return await service.search(query=query, page=page, size=size)


@router.get("/films/{film_id}", tags=["films"])
async def film_details(
    film_id: str,
    es: AsyncElasticsearch = Depends(get_elastic),
    redis: Redis | None = Depends(get_redis),
):
    service = FilmService(es, redis)
    film = await service.get_by_id(film_id)

    if film is None:
        raise HTTPException(status_code=404, detail="film not found")

    return film
