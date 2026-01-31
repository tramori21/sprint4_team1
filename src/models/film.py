from __future__ import annotations

from pydantic import BaseModel, Field


class GenreShort(BaseModel):
    id: str
    name: str


class PersonShort(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    title: str
    description: str | None = None
    rating: float | None = None
    type: str

    genres: list[GenreShort] = Field(default_factory=list)
    actors: list[PersonShort] = Field(default_factory=list)
    writers: list[PersonShort] = Field(default_factory=list)
    directors: list[PersonShort] = Field(default_factory=list)


class FilmListResponse(BaseModel):
    count: int
    results: list[Film]
