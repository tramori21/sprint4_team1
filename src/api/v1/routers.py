from fastapi import APIRouter

from src.api.v1.films import router as films_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(films_router)
