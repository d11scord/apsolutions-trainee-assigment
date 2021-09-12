from sqlalchemy.engine.url import URL

from os import getenv


DB_DRIVER = getenv("POSTGRES_DRIVER", default="postgresql")
DB_HOST = getenv("POSTGRES_HOST", default="localhost")
DB_PORT = getenv("POSTGRES_PORT", default=5432)
DB_USER = getenv("POSTGRES_USER", default="julia")
DB_PASSWORD = getenv("POSTGRES_PASSWORD", default="root")
DB_DATABASE = getenv("POSTGRES_DB", default="documents")

DB_DSN = URL(
    drivername=DB_DRIVER,
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
)
