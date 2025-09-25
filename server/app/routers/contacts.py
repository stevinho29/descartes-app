from typing import Annotated
import logging

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.contacts.domain.contact_core import ContactCore
from app.contacts.domain.entities import ContactCreate, ContactUpdate, MutipleResponse, FilterQuery, UniqueResponse
from app.settings import CONF
from sqlmodel import Session, create_engine
from fastapi import APIRouter, Body, Depends, Query
from fastapi.responses import JSONResponse
from app.contacts.adapters.contact_database import (
    ContactDatabase,

)

logger = logging.getLogger(__name__)

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


@router.post("/contacts", response_model=UniqueResponse)
def create_contact( core: CoreDep, contact:ContactCreate):
    new_contact = core.create_contact(contact)
    return UniqueResponse(data=new_contact.model_dump())


@router.get("/contacts", response_model=MutipleResponse)
def get_contacts(core: CoreDep, filter_query: Annotated[FilterQuery, Query()]):

    offset, limit = filter_query.offset_limit
    total, data = core.get_contacts(filter_query)
    current_page = get_current_page(total=total, start=offset, end=limit)
    data_serialized = [c.model_dump() if isinstance(c, BaseModel) else c for c in data]
    if total < limit - offset:
        status_code = 200
    else:
        status_code = 206
    return JSONResponse(status_code=status_code, content=jsonable_encoder(MutipleResponse(total=total, data=data_serialized, current=current_page)))

@router.get("/contacts/{contact_id}", response_model=UniqueResponse)
def get_contact(contact_id: int, core: CoreDep):
    contact = core.get_contact(contact_id)
    return UniqueResponse(data=contact.model_dump())


@router.put("/contacts/{contact_id}", response_model=UniqueResponse)
def update_contact(contact_id: int, contact: ContactUpdate, core: CoreDep):
    contact.id = contact_id
    updated_contact = core.update_contact(contact)

    return UniqueResponse(data=updated_contact.model_dump())


@router.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, core: CoreDep):
    core.delete_contact(contact_id)
    return {"msg": "Contact deleted with success"}
