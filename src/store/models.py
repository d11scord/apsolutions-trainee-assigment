from typing import List

from src.store import db
from src.store.schemas import CreateRubricSchema


class DocumentsRubrics(db.Model):
    __tablename__ = 'documents_rubrics'

    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
    rubric_id = db.Column(db.Integer, db.ForeignKey('rubrics.id'))


class Rubric(db.Model):
    __tablename__ = "rubrics"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)

    @classmethod
    async def get_or_create(cls, item: CreateRubricSchema):
        rubric = await cls.query.where(
            cls.title == item.title
        ).gino.first()

        if not rubric:
            rubric = await cls.create(**item.dict())
        return rubric


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime,
                             nullable=False,
                             default=db.func.now())

    def __init__(self, **kw):
        super().__init__(**kw)
        self.rubrics = set()

    def add_rubric(self, rubric):
        self.rubrics.add(rubric)

    async def add_rubrics(self, rubrics: List[Rubric]):
        for rub in rubrics:
            await DocumentsRubrics.create(
                document_id=self.id,
                rubric_id=rub.id,
            )
