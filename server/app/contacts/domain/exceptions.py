

class NotFound(Exception):
    pass

class ContactNotFound(NotFound):
    pass

class ConflictError(Exception):
    pass

class EmailAddressNotUnique(ConflictError):
    pass
