from fastapi import Query


class Pagination:
    def __init__(
        self,
        page_number: int = Query(1, ge=1, description="Номер страницы"),
        page_size: int = Query(50, ge=1, le=100, description="Размер страницы"),
    ):
        self.page_number = page_number
        self.page_size = page_size

    @property
    def offset(self) -> int:
        return (self.page_number - 1) * self.page_size
