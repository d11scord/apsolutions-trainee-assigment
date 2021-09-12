from pydantic import BaseModel
from pydantic.schema import datetime


class DocumentModel(BaseModel):
    id: int
    text: str
    created_date: datetime
