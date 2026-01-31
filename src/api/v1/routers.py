from fastapi import APIRouter

from src.api.v1.films import router as films_router


api_router = APIRouter()
api_router.include_router(films_router)
