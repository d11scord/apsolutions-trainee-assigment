from typing import List

from fastapi import APIRouter
from starlette.responses import RedirectResponse

from src.store.models import (
    Document,
    Rubric,
    DocumentsRubrics,
)
from src.store.schemas import (
    DocumentSchema,
    CreateDocumentSchema,
    RubricSchema,
    CreateRubricSchema,
    DocumentRubricSchema,
)

router = APIRouter(tags=["documents"])


@router.get("/", tags=["index"])
def main():
    return RedirectResponse(url="/docs/")


@router.post("/documents/add", response_model=DocumentSchema)
async def add_document(document: CreateDocumentSchema):
    # rubrics = [rub.dict() for rub in document.rubrics]
    # # https://github.com/python-gino/gino/issues/314#issuecomment-496130292
    # item = await insert(Rubric).values(rubrics).on_conflict_do_nothing().gino.all()

    rubrics: List[Rubric] = list()
    for rub in document.rubrics:
        item = await Rubric.get_or_create(rub)
        rubrics.append(item)

    doc = await Document.create(text=document.text)
    await doc.add_rubrics(rubrics)
    return doc.to_dict()


@router.delete("/documents/{id}")
async def delete_document(doc_id: int):
    doc = await Document.get_or_404(doc_id)
    await doc.delete()
    return dict(id=doc_id)


@router.get("/documents/", response_model=List[DocumentSchema])
async def list_documents():
    documents = await Document.query.gino.all()
    return [DocumentSchema.from_orm(doc) for doc in documents]


@router.get("/documents/search/")
async def search():
    docs_ids = [1, 7, 9]

    # https://python-gino.org/docs/en/1.0/how-to/loaders.html#other-relationships
    query = (
        Document.outerjoin(DocumentsRubrics).outerjoin(Rubric)
        .select()
        .where(Document.id.in_(docs_ids))
    )
    full_docs = (
        await query.gino.load(Document.distinct(Document.id).load(
                add_rubric=Rubric.distinct(Rubric.id)
            )
        ).all()
    )

    return [DocumentRubricSchema.from_orm(doc) for doc in full_docs]


@router.post("/rubrics/add", response_model=RubricSchema)
async def add_rubric(rubric: CreateRubricSchema):
    rub = await Rubric.create(title=rubric.title)
    return rub.to_dict()


@router.get("/rubrics/", response_model=List[RubricSchema])
async def list_rubrics():
    rubs = await Rubric.query.gino.all()
    return [RubricSchema.from_orm(rub) for rub in rubs]
