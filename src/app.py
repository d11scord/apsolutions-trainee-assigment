from fastapi import FastAPI

from src.api.endpoints import router
from src.store.database import db


def create_app():
    app = FastAPI(title="ESearch Engine", openapi_url="/docs.json")
    db.init_app(app=app)
    app.include_router(router)
    return app
