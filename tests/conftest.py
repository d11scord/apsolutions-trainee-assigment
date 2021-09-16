from typing import List, Optional

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from src.api.endpoints import router
from src.store.db_management import get_db
from src.store.es_management import get_es
from src.store.models import Rubric
from src.store.schemas import DocumentSchema, DocumentRubricSchema


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    return app


app = create_test_app()


@pytest.fixture()
def cli():
    return TestClient(app)


fake_document = DocumentSchema(
    id=1,
    text="text",
    created_date="2020-01-01 12:12:12",
)

fake_document_with_rubrics = DocumentRubricSchema(
    id=1,
    text="text",
    created_date="2020-01-01 12:12:12",
    rubrics=[
        "title",
    ],
)


class DbManagementTest:
    @staticmethod
    async def create_document_with_rubrics(
        doc_text: str, rubrics: List[Rubric]
    ) -> DocumentSchema:
        return fake_document

    @staticmethod
    async def search_by_ids(docs_ids: List[int]) -> List[DocumentRubricSchema]:
        return [fake_document_with_rubrics]

    @staticmethod
    async def delete_document_by_id(doc_id: int) -> Optional[int]:
        if doc_id == 1:
            return doc_id
        return None


class EsManagementTest:
    async def search(self, query: str) -> List[int]:
        return [1]

    async def add_document(self, document: DocumentSchema) -> None:
        return None

    async def delete_document(self, doc_id: int) -> None:
        return None


def get_db_test() -> DbManagementTest:
    return DbManagementTest()


def get_es_test() -> EsManagementTest:
    return EsManagementTest()


# https://fastapi.tiangolo.com/advanced/testing-database/#create-the-new-database-session
app.dependency_overrides[get_db] = get_db_test
app.dependency_overrides[get_es] = get_es_test


@pytest.fixture
def fake_document_from_db() -> DocumentSchema:
    return fake_document


@pytest.fixture
def fake_document_with_rubrics_from_db() -> DocumentRubricSchema:
    return fake_document_with_rubrics


@pytest.fixture
def document_schema() -> DocumentSchema:
    return DocumentSchema(
        id=1,
        text="text",
        created_date="2020-01-01 12:12:12",
    )


@pytest.fixture
def document_with_rubrics_schema() -> DocumentRubricSchema:
    return DocumentRubricSchema(
        id=1,
        text="text",
        created_date="2020-01-01 12:12:12",
        rubrics=[
            "title",
        ],
    )
