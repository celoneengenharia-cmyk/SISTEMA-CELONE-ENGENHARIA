from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255))
    cnpj: Mapped[str | None] = mapped_column(String(32), nullable=True)
    endereco: Mapped[str | None] = mapped_column(String(512), nullable=True)
    contato: Mapped[str | None] = mapped_column(String(255), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    laudos: Mapped[list["Laudo"]] = relationship(back_populates="cliente")  # noqa: F821
