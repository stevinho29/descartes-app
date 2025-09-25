from pydantic import BaseModel


class DatabaseFilter(BaseModel):
    
    select: BaseModel | None = None
    offset: int | None = None
    limit: int | None = None
    order_by: list[str] | None = None
    only: list[str] | None = None
    
class Database:

    def get_record_by_id(self, id:int) -> BaseModel:
        raise NotImplementedError("Sub classes must implement this method")

    def get_record_counts(self, _filter: DatabaseFilter) -> int:
        raise NotImplementedError("Sub classes must implement this method")
    
    def get_record_by_filter(self, _filter:DatabaseFilter) -> BaseModel:
        raise NotImplementedError("Sub classes must implement this method")

    def insert(self, data:BaseModel) -> BaseModel:
        raise NotImplementedError("Sub classes must implement this method")

    def update(self, data:BaseModel) -> BaseModel:
        raise NotImplementedError("Sub classes must implement this method")
    
    def delete(self, int:id):
        raise NotImplementedError("Sub classes must implement this method")