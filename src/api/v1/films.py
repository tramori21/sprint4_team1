from fastapi import APIRouter, Request, Depends
from http import HTTPStatus
from elasticsearch import NotFoundError

from api.deps.pagination import Pagination

router = APIRouter(prefix="/films", tags=["Films"])


@router.get(
    "",
    summary="Список фильмов",
    description="Возвращает список фильмов из Elasticsearch с пагинацией",
    response_description="Список фильмов",
    status_code=HTTPStatus.OK,
)
async def films_list(
    request: Request,
    pagination: Pagination = Depends(),
):
    es = request.app.state.es

    try:
        response = await es.search(
            index="movies",
            body={
                "query": {"match_all": {}},
                "from": pagination.offset,
                "size": pagination.page_size,
            },
        )
    except NotFoundError:
        return {"count": 0, "results": []}

    hits = response["hits"]["hits"]
    return {
        "count": response["hits"]["total"]["value"],
        "results": [hit["_source"] for hit in hits],
    }
