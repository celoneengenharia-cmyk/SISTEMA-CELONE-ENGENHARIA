from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Maquina(Base):
    __tablename__ = "maquina"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(255))
    fabricante: Mapped[str | None] = mapped_column(String(255), nullable=True)
    modelo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    serie: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ano: Mapped[str | None] = mapped_column(String(16), nullable=True)
    funcao: Mapped[str | None] = mapped_column(String(512), nullable=True)
    localizacao: Mapped[str | None] = mapped_column(String(512), nullable=True)
    # Anexo NR-12 aplicável — texto livre nesta fase.
    anexo_nr12: Mapped[str | None] = mapped_column(String(255), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    laudos: Mapped[list["Laudo"]] = relationship(back_populates="maquina")  # noqa: F821
