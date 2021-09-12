from fastapi import APIRouter

from src.store.models import Document
from src.store.schemas import DocumentModel

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Hello World"}


@router.post("/documents/add")
async def add_document(document: DocumentModel):
    doc = await Document.create(text=document.text)
    return doc.to_dict()


@router.delete("/documents/{id}")
async def delete_user(doc_id: int):
    doc = await Document.get_or_404(doc_id)
    await doc.delete()
    return dict(id=doc_id)
