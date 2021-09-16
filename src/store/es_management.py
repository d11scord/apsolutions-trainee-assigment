import json
from typing import Optional, List

from elasticsearch import AsyncElasticsearch, NotFoundError

from src.store.config import ES_INDEX, ES_HOST, ES_PORT
from src.store.schemas import DocumentSchema


class EsManagement:
    def __init__(self):
        self.es_client = AsyncElasticsearch(
            hosts=[{'host': ES_HOST, 'port': ES_PORT}]
        )
        self.index_name: Optional[str] = None

    async def create_index(self, index_name: str) -> None:
        mapping = {
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                }
            }
        }

        await self.es_client.indices.create(
            index=index_name,
            ignore=400,
            body=mapping
        )
        self.index_name = index_name

    async def search(self, query: str) -> List[int]:
        es_query = {
            "query": {
                "match": {
                    'text': query,
                }
            }
        }

        result = await self.es_client.search(
            index=self.index_name,
            body=es_query,
            size=20,
        )

        hits_list = result["hits"]["hits"]
        doc_ids = [int(hit["_id"]) for hit in hits_list]
        print(doc_ids)
        return doc_ids

    async def add_document(self, document: DocumentSchema) -> None:
        await self.es_client.index(
            index=self.index_name,
            id=document.id,
            body=json.dumps({
                "text": document.text,
            }),
        )

    async def delete_document(self, doc_id: int) -> None:
        try:
            await self.es_client.delete(
                index=self.index_name,
                id=doc_id,
            )
        except NotFoundError:
            print("not found")

    async def close(self):
        await self.es_client.close()


async def get_es():
    es = EsManagement()
    await es.create_index(ES_INDEX)
    try:
        yield es
    finally:
        await es.close()
