from letsrolld.db import models  # noqa
from letsrolld.db.models import Base

DB_URL = "sqlite:///movie.db"


def create_tables(engine):
    Base.metadata.create_all(engine)


def create_engine():
    from sqlalchemy import create_engine

    return create_engine(DB_URL)
