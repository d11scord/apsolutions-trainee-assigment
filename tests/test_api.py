from datetime import datetime

from starlette import status
from starlette.testclient import TestClient

from src.store.schemas import DocumentSchema, DocumentRubricSchema


class TestEndpoints:
    def test_document_create(
        self,
        cli: TestClient,
        document_schema: DocumentSchema,
    ) -> None:
        response = cli.post(
            "/documents/add",
            json={
                "text": "text",
                "rubrics": [],
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == document_schema.id
        assert response.json()["text"] == document_schema.text
        assert datetime.strptime(
            response.json()["created_date"],
            '%Y-%m-%dT%H:%M:%S') == document_schema.created_date

    def test_search_by_ids(
        self,
        cli: TestClient,
        document_with_rubrics_schema: DocumentRubricSchema,
    ) -> None:

        query = "text"
        response = cli.get(
            f"/documents/search/{query}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        response = response.json()[0]
        assert response["id"] == document_with_rubrics_schema.id
        assert response["text"] == document_with_rubrics_schema.text
        assert len(response["rubrics"]) == len(document_with_rubrics_schema.rubrics)

    def test_delete_document(
        self,
        cli: TestClient,
    ):
        doc_id = 1
        response = cli.delete(
            f"/documents/{doc_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"id": 1}

    def test_delete_document_404(
        self,
        cli: TestClient,
    ):
        doc_id = 999
        response = cli.delete(
            f"/documents/{doc_id}",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": f"Document with id={doc_id} not found"}
