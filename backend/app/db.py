"""Engine, sessão e Base declarativa do SQLAlchemy."""
from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import JSON, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import get_settings

settings = get_settings()

# JSONB no Postgres (produção) e JSON genérico no SQLite (teste rápido local).
JSONType = JSONB().with_variant(JSON(), "sqlite")

_is_sqlite = settings.database_url.startswith("sqlite")
engine = create_engine(
    settings.database_url,
    pool_pre_ping=not _is_sqlite,
    connect_args={"check_same_thread": False} if _is_sqlite else {},
    future=True,
)
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
