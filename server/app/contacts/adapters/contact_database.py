
import logging
from pydantic import EmailStr
from app.contacts.domain.exceptions import ContactNotFound
from sqlmodel import SQLModel, Field, Session, select, func
from sqlalchemy import asc, desc

from app.contacts.ports.database import Database, DatabaseFilter
from app.contacts.domain.entities import ContactCreate, ContactDTO, ContactUpdate

logger = logging.getLogger(__name__)
class Contact(SQLModel, table=True):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    job: str = Field(index=True, max_length=50)
    comment: str = Field(max_length=2000)
    id: int | None = Field(default=None, primary_key=True)


class ContactDatabase(Database):

    def __init__(self, session: Session):
        self.session = session

    
    def get_record_by_id(self, id:int) -> ContactDTO:
        contact = self.session.get(Contact, id)
        if not contact:
            raise ContactNotFound(f"Contact with id {id} not found")
        return ContactDTO.model_validate(contact.__dict__)
    
    def get_record_counts(self, _filter: DatabaseFilter) -> int:
        query = select(func.count(Contact.id))
        if _filter.select:
            for field, value in _filter.select.items():
                query = query.where(getattr(Contact, field) == value)
        result =  self.session.exec(query).one()
        return result

    
    def get_record_by_filter(self, _filter:DatabaseFilter) -> list[Contact]:
        

        if _filter.only:
            query = select(*[getattr(Contact,col) for col in _filter.only])

        else:
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

        result = list(self.session.exec(query).all())
        if _filter.only:
            return result
        return [ContactDTO.model_validate(contact.__dict__) for contact in result]

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
        return ContactDTO.model_validate(contact.__dict__)

    def delete(self, id:int):
        contact = self.session.get(Contact, id)
        if not contact:
            raise ContactNotFound(f"Contact with id {id} not found")
        self.session.delete(contact)
        self.session.commit()