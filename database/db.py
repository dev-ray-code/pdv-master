import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///pdv_store.db"
)


if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def criar_banco():
    Base.metadata.create_all(bind=engine)