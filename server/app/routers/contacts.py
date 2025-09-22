from typing import Annotated

from fastapi.exceptions import RequestValidationError


from app.contacts.domain.contact_core import ContactCore
from app.contacts.domain.entities import CustomResponse, FilterQuery
from app.settings import CONF
from sqlmodel import Session, create_engine
from fastapi import APIRouter, Depends, Query
from app.contacts.adapters.contact_database import (
    Contact,
    ContactCreate,
    ContactDatabase,
    ContactUpdate,
)

router = APIRouter()




postgre_url = f"postgresql+psycopg2://{CONF.DB_USER}:{CONF.DB_PASSWORD}@{CONF.DB_HOST}:{CONF.DB_PORT}/{CONF.DB_NAME}"
engine = create_engine(postgre_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_core(session: SessionDep):
    contact_core = ContactCore(db=ContactDatabase(session=session))
    return contact_core


def get_current_page(total: int, start: int, end: int):
    size = end - start
    ranges = []
    for i in range(0, total, size):
        ranges.append(f"{i}-{i + size}")
    return ranges.index(f"{start}-{end}") + 1


CoreDep = Annotated[ContactCore, Depends(get_core)]



@router.post("/contacts", response_model=Contact)
def create_contact(contact: ContactCreate, core: CoreDep):
    new_contact = core.create_contact(contact)
    return new_contact


@router.get("/contacts", response_model=list[Contact])
def get_contacts(core: CoreDep, filter_query: Annotated[FilterQuery, Query()]):
    if not all([field in ContactCore.ORDERABLE_FIELDS for field in filter_query.sort]):
        raise RequestValidationError(400, "Invalid sort field")
    if not all([field in ContactCore.ORDERABLE_FIELDS for field in filter_query.sort]):
        raise RequestValidationError(400, "Invalid desc field")

    range = filter_query.range
    try:
        offset, limit = [map(int, range.split("-"))]
    except ValueError:
        raise
    total, data = core.get_contacts(filter_query)
    current_page = get_current_page(total=total, start=offset, end=limit)
    response = CustomResponse(total=total, data=data, current=current_page)
    return response


@router.get("/contacts/{contact_id}", response_model=Contact)
def read_hero(contact_id: int, core: CoreDep):
    contact = core.get_contact(contact_id)
    return contact


@router.patch("/contacts/{contact_id}", response_model=Contact)
def update_hero(contact_id: int, contact: ContactUpdate, core: CoreDep):
    contact.id = contact_id
    updated_contact = core.update_contact(contact)

    return updated_contact


@router.delete("/contacts/{contact_id}")
def delete_hero(contact_id: int, core: CoreDep):
    core.delete_contact(contact_id)
    return {"msg": "Contact deleted with success"}
