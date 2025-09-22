
from pydantic import EmailStr
from app.contacts.domain.exceptions import ContactNotFound
from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import asc, desc

from app.contacts.ports.database import Database, DatabaseFilter

class ContactBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    job: str
    comment: str

class Contact(ContactBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    id: int

class ContactDatabase(Database):

    def __init__(self, session: Session):
        self.session = session

    
    def get_record_by_id(self, id:int) -> Contact:
        contact = self.session.get(Contact, id)
        if not contact:
            raise ContactNotFound(f"Contact with id {id} not found")
        return contact
    
    def get_record_counts(self, _filter: DatabaseFilter) -> int:
        query = select(Contact)
        if _filter.select:
            for field, value in _filter.select.items():
                query = query.where(getattr(Contact, field) == value)
        return self.session.exec(query).count()

    
    def get_record_by_filter(self, _filter:dict) -> list[Contact]:
        query = select(Contact)

        if _filter.select:
            for field, value in _filter.select.items():
                query = query.where(getattr(Contact, field) == value)

        if _filter.order_by:
            for field in _filter.order_by:
                if field.startswith("-"):
                    query = query.order_by(desc(getattr(Contact, field[1:])))
                else:
                    query = query.order_by(asc(getattr(Contact, field)))

        if _filter.offset is not None:
            query = query.offset(_filter.offset)
        if _filter.limit is not None:
            query = query.limit(_filter.limit)

        return list(self.session.exec(query).all())

    def insert(self, data: ContactCreate) -> Contact:
        contact = Contact.model_validate(data)
        self.session.add(contact)
        self.session.commit()
        self.session.refresh(contact)
        return contact

    def update(self, data: ContactUpdate) -> Contact:
        contact = self.session.get(Contact, data.id)
        if not contact:
            raise ContactNotFound(f"Contact with id {data.id} not found")
        contact_data = data.model_dump(exclude_unset=True)
        contact.sqlmodel_update(contact_data)
        self.session.add(contact)
        self.session.commit()
        self.session.refresh(contact)
        return contact

    def delete(self, id:int):
        contact = self.session.get(Contact, id)
        if not contact:
            raise ContactNotFound(f"Contact with id {id} not found")
        self.session.delete(contact)
        self.session.commit()