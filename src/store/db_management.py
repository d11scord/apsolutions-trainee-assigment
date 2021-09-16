from typing import List, Optional

from src.store.models import Rubric, Document, DocumentsRubrics
from src.store.schemas import DocumentSchema, DocumentRubricSchema


class DbManagement:
    @staticmethod
    async def create_document_with_rubrics(
        doc_text: str, rubrics: List[Rubric]
    ) -> DocumentSchema:

        doc = await Document.create(text=doc_text)
        await doc.add_rubrics(rubrics)
        doc = DocumentSchema.from_orm(doc)
        return doc

    @staticmethod
    async def search_by_ids(docs_ids: List[int]) -> List[DocumentRubricSchema]:
        # https://python-gino.org/docs/en/1.0/how-to/loaders.html#other-relationships
        query = (
            Document.outerjoin(DocumentsRubrics).outerjoin(Rubric)
            .select()
            .where(Document.id.in_(docs_ids))
            .order_by(Document.created_date.desc())
        )
        full_docs = (
            await query.gino.load(Document.distinct(Document.id).load(
                add_rubric=Rubric.distinct(Rubric.id)
                )
            ).all()
        )

        return [DocumentRubricSchema.from_orm(doc) for doc in full_docs]

    @staticmethod
    async def delete_document_by_id(doc_id: int) -> Optional[int]:
        doc = await Document.get(doc_id)
        if doc:
            await DocumentsRubrics.delete.where(Document.id == doc_id).gino.status()
            await doc.delete()
            return doc.id
        return None


def get_db():
    return DbManagement
