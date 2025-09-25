

from pydantic import BaseModel, Field, EmailStr, field_validator

from typing import Any
class MutipleResponse(BaseModel):
    data: list[Any]
    total: int
    links: dict = {}
    current: int

class UniqueResponse(BaseModel):
    data: Any

class FilterQuery(BaseModel):
    email: str | None = None
    job: str | None = None
    range: str = Field(default="0-100", pattern=r"^\d+-\d+$")
    sort: list[str]  = []
    desc: list[str] = []
    only: list[str] = []

    MAX_LIMIT: int = 500

    @property
    def offset_limit(self) -> tuple[int, int]:
        """Retourne offset et limit (safe parsing)."""
        start, end = self.range.split("-")
        offset, limit = int(start), int(end)
        if limit - offset > self.MAX_LIMIT:
            raise ValueError(f"Limit {limit - offset} exceeds maximum {self.MAX_LIMIT}")
        return offset, limit

    @field_validator("sort", "desc", "only", mode="before")
    def validate_sort_fields(cls, v):
        """Assure que les champs de tri sont dans la whitelist définie côté domaine."""
        from app.contacts.domain.contact_core import ContactCore

        if v == [""]:
            return []
        if not v:
            return []
        invalid = [field for field in v if field not in ContactCore.ORDERABLE_FIELDS if field != ""]
        if invalid:
            raise ValueError(f"Invalid sort fields: {invalid}")
        return v
    
class ContactDTO(BaseModel):
    id : int | None
    first_name: str
    last_name: str
    email: EmailStr
    job: str
    comment: str

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    job: str
    comment: str

class ContactUpdate(BaseModel):
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    job: str | None = None
    comment: str | None = None