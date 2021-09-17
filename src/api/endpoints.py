from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse

from src.store.db_management import DbManagement, get_db
from src.store.es_management import EsManagement, get_es
from src.store.models import (
    Document,
    Rubric,
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
    db: DbManagement = Depends(get_db),
    es: EsManagement = Depends(get_es),
):
    rubrics: List[Rubric] = list()
    for rub in document.rubrics:
        item = await Rubric.get_or_create(rub)
        rubrics.append(item)

    doc = await db.create_document_with_rubrics(document.text, rubrics)
    await es.add_document(doc)
    return doc


@router.get("/documents/search/{query}",
            response_model=List[DocumentRubricSchema],
            tags=["documents"])
async def search(
    query: str,
    db: DbManagement = Depends(get_db),
    es: EsManagement = Depends(get_es),
):
    docs_ids = await es.search(query)
    documents = await db.search_by_ids(docs_ids)
    return documents


@router.delete("/documents/{doc_id}", tags=["documents"])
async def delete_document(
    doc_id: int,
    db: DbManagement = Depends(get_db),
    es: EsManagement = Depends(get_es),
):
    id_ = await db.delete_document_by_id(doc_id)
    if not id_:
        raise HTTPException(status_code=404, detail=f"Document with id={doc_id} not found")
    await es.delete_document(doc_id)
    return dict(id=id_)


@router.get("/documents/",
            response_model=List[DocumentSchema],
            tags=["misc"])
async def list_documents(offset: int = 0, limit: int = 25):
    documents = (
        await Document.query
        .offset(offset)
        .limit(limit)
        .gino.all()
    )
    return [DocumentSchema.from_orm(doc) for doc in documents]


@router.get("/rubrics/", response_model=List[RubricSchema], tags=["misc"])
async def list_rubrics(offset: int = 0, limit: int = 25):
    rubs = (
        await Rubric.query
        .offset(offset)
        .limit(limit)
        .gino.all()
    )
    return [RubricSchema.from_orm(rub) for rub in rubs]
