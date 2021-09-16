import asyncio
import csv
import re
from datetime import datetime
from typing import List

from src.store.database import db
from src.store.config import DB_DSN, ES_INDEX
from src.store.es_management import EsManagement
from src.store.models import Rubric, Document
from src.store.schemas import CreateRubricSchema, DocumentSchema


async def populate():
    await db.set_bind(DB_DSN)
    await db.gino.create_all()

    es_client = EsManagement()
    await es_client.create_index(ES_INDEX)

    with open("posts.csv", encoding="utf-8") as f:
        posts = csv.reader(f)

        next(posts)  # skip headers

        for i, post in enumerate(posts, start=1):
            text, raw_created_date, raw_rubrics = post

            created_date = datetime.strptime(raw_created_date, '%Y-%m-%d %H:%M:%S')
            rubrics = re.sub(r"(\[)|(\])|(,)|(')|(\")", "", raw_rubrics).split(" ")

            clean_rubrics: List[Rubric] = list()
            for rub in rubrics:
                item = await Rubric.get_or_create(CreateRubricSchema(title=rub))
                clean_rubrics.append(item)

            doc = await Document.create(text=text, created_date=created_date)
            await doc.add_rubrics(clean_rubrics)
            doc = DocumentSchema(**doc.to_dict())
            await es_client.add_document(doc)

            print("Added post", i)

    await db.pop_bind().close()
    await es_client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(populate())
