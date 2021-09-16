from gino.ext.starlette import Gino

from src.store.config import DB_DSN

db = Gino(
    dsn=DB_DSN,
    ssl=False,
    retry_limit=5,
    retry_interval=5,
)
