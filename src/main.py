from fastapi import FastAPI

from lifespan import lifespan
from api.v1 import films

app = FastAPI(
    title="Movies API",
    description="API для получения информации о фильмах",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(films.router, prefix="/api/v1")
