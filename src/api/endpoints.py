from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from src.store.elastic import EsClient, get_es
from src.store.models import (
    Document,
    Rubric,
    DocumentsRubrics,
)
from src.store.schemas import (
    DocumentSchema,
    CreateDocumentSchema,
    RubricSchema,
    DocumentRubricSchema,
)

router = APIRouter()


@router.get("/", tags=["index"])
def main():
    return RedirectResponse(url="/docs/")


@router.post("/documents/add",
             response_model=DocumentSchema,
             tags=["documents"])
async def add_document(
    document: CreateDocumentSchema,
    es_client: EsClient = Depends(get_es),
):
    rubrics: List[Rubric] = list()
    for rub in document.rubrics:
        item = await Rubric.get_or_create(rub)
        rubrics.append(item)

    doc = await Document.create(text=document.text)
    await doc.add_rubrics(rubrics)
    doc = DocumentSchema(**doc.to_dict())
    await es_client.add_document(doc)
    return doc.dict()


@router.get("/documents/search/{query}",
            response_model=List[DocumentRubricSchema],
            tags=["documents"])
async def search(
    query: str,
    es_client: EsClient = Depends(get_es),
):
    docs_ids = await es_client.search(query)

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


@router.delete("/documents/{id}", tags=["misc"])
async def delete_document(
    doc_id: int,
    es_client: EsClient = Depends(get_es),
):
    doc = await Document.get_or_404(doc_id)
    await doc.delete()
    await es_client.delete_document(doc_id)
    return dict(id=doc_id)


@router.get("/documents/",
            response_model=List[DocumentSchema],
            tags=["misc"])
async def list_documents():
    documents = await Document.query.gino.all()
    return [DocumentSchema.from_orm(doc) for doc in documents]


@router.get("/rubrics/", response_model=List[RubricSchema], tags=["misc"])
async def list_rubrics():
    rubs = await Rubric.query.gino.all()
    return [RubricSchema.from_orm(rub) for rub in rubs]
