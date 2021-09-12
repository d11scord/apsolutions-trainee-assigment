from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.store import db


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.BigInteger(), primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=db.func.now())

    rubrics = relationship("Rubric", back_populates="documents")


class Rubric(db.Model):
    __tablename__ = "rubric"

    id = db.Column(db.BigInteger(), primary_key=True)
    title = db.Column(db.String, nullable=False)
    document_id = db.Column(db.Integer, ForeignKey('documents.id'))
