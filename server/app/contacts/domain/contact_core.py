

import logging
from app.contacts.domain.entities import FilterQuery
from app.contacts.adapters.contact_database import Contact
from app.contacts.ports.database import Database, DatabaseFilter
from app.contacts.domain.exceptions import ContactNotFound

logger = logging.getLogger(__name__)

class ContactCore:

    ORDERABLE_FIELDS = ["first_name", "last_name", "job", "email"]

    def __init__(self, db:Database) -> None:
        self.contact_db = db
        self.log_header = "[ContactCore]"
    
    @classmethod
    def _get_order_by(cls, sort: list, desc: list):
        order_by = []
        for field in sort:
            if field in desc:
                order_by.append(f"-{field}")
            else:
                order_by.append(field)
        return order_by
    
    def get_contact(self, id:int):
        log_header = f"{self.log_header}[get_contact]"
        contact = self.contact_db.get_record_by_id(id)
        logger.info(f"{log_header} contact with id {id} retrieved with success")
        return contact
    
    def get_contacts(self, params:FilterQuery):
        log_header = f"{self.log_header}[get_contacts]"
        _filter = DatabaseFilter()
        contact = {}
        if params.email:
            contact["email"] = params.email
        _filter.select = contact

        total = self.contact_db.get_record_counts(_filter)

        if total == 0:
            raise ContactNotFound("Contact not found")
        
        order_by = self._get_order_by(params.sort, params.desc)
        _filter.order_by = order_by

        offset, limit = params.range.split("-")
        _filter.limit = limit
        _filter.offset = offset

        contact = self.contact_db.get_record_by_filter(_filter)
        logger.info(f"{log_header} contact with id {id} retrieved with success")
        return contact

    def create_contact(self, data:Contact):
        log_header = f"{self.log_header}[create_contact]"
        contact = self.contact_db.insert(data)
        logger.info(f"{log_header} new contact created with success")
        return contact

    def update_contact(self, data:Contact):
        log_header = f"{self.log_header}[update_contact]"
        contact = self.contact_db.update(data)
        logger.info(f"{log_header} contact updated with success")
        return contact
    
    def delete_contact(self, contact_id:int):
        log_header = f"{self.log_header}[delete_contact]"
        self.contact_db.delete(contact_id)
        logger.info(f"{log_header} contact deleted with success")