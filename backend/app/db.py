"""Engine, sessão e Base declarativa do SQLAlchemy."""
from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    """Base declarativa compartilhada por todos os modelos."""


def get_db() -> Generator:
    """Dependência FastAPI: abre uma sessão por request e a fecha ao final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
