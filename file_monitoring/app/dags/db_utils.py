from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from config.settings import (
    MAIN_DB_HOST,
    MAIN_DB_NAME,
    MAIN_DB_PASSWORD,
    MAIN_DB_PORT,
    MAIN_DB_USER,
)
from models import Base


@contextmanager
def create_sa_engine_to_main_db():
    connection_url = URL.create(
        "postgresql",
        MAIN_DB_USER,
        MAIN_DB_PASSWORD,
        MAIN_DB_HOST,
        MAIN_DB_PORT,
        database=MAIN_DB_NAME,
    )
    engine = create_engine(connection_url, future=True)

    try:
        yield engine
    finally:
        engine.dispose()


def create_tables_in_db():
    with create_sa_engine_to_main_db() as engine:
        Base.metadata.create_all(engine)
