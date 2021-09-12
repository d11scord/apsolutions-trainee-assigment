from typing import List

from pydantic import BaseModel
from pydantic.schema import datetime


class RubricSchema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class CreateRubricSchema(BaseModel):
    title: str


class DocumentSchema(BaseModel):
    id: int
    text: str
    created_date: datetime

    class Config:
        orm_mode = True


class CreateDocumentSchema(BaseModel):
    text: str
    rubrics: List[CreateRubricSchema]


class DocumentRubricSchema(DocumentSchema):
    rubrics: List[RubricSchema]
