

from pydantic import BaseModel


class CustomResponse(BaseModel):
    data: list[BaseModel]
    total: int
    links: dict = {}
    current: int

class FilterQuery(BaseModel):
    email: str | None = None
    range: str = "0-100"
    sort: list[str] = []
    desc: list[str]  = []

