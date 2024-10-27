# from sqlalchemy.orm import sessionmaker
# # Create SQLAlchemy engine
# engine = create_engine(connection_str)

# # Create a configured "Session" class
# Session = sessionmaker(bind=engine)

# # Create a session
# session = Session()

# # Example usage: Query all users
# users = session.query(User).all()
# for user in users:
#     print(user.id, user.name, user.email, user.age)

# # Example usage: Query specific columns
# users = session.query(User.name, User.email).all()
# for user in users:
#     print(user.name, user.email)

# # Example usage: Order by
# users = session.query(User).order_by(User.age).all()
# for user in users:
#     print(user.id, user.name, user.email, user.age)

# # Close the session
# session.close()

from contextlib import contextmanager

from config.settings import (
    MAIN_DB_HOST,
    MAIN_DB_NAME,
    MAIN_DB_PASSWORD,
    MAIN_DB_PORT,
    MAIN_DB_USER,
)

from models.db import Base
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


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


# def save_to_db(table_name: str, data: pl.DataFrame) -> None:
#     """
#     Manual saving to DB. It was created to save data frame to 'temporary' table.

#     Args:
#         table_name (str): имя временной таблицы без указания схемы.
#         data (pl.DataFrame): дата фрейм, из которого берутся данные для записи
#     """
#     columns = [
#         column(column_name) for column_name in data.columns
#     ]  # Work for both (pd, pl)
#     db_table = table(table_name, *columns, schema=TEMPLATE_DB_SCHEMA_NAME)

#     data = {}

#     with (
#         create_sa_engine_to_main_db() as engine,
#         Session(engine) as session,
#         session.begin(),
#     ):
#         # We clear temporary table first
#         truncate_command = f"TRUNCATE TABLE {TEMPLATE_DB_SCHEMA_NAME}.{table_name}"
#         session.execute(truncate_command)

#         session.execute(
#             insert(db_table),
#             data,
#         )
