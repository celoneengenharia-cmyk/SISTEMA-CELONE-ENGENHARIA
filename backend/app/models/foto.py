from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class Foto(Base):
    __tablename__ = "foto"

    id: Mapped[int] = mapped_column(primary_key=True)
    laudo_id: Mapped[int] = mapped_column(ForeignKey("laudo.id", ondelete="CASCADE"))
    # Chave no storage (não o binário). O banco guarda só a referência.
    storage_key: Mapped[str] = mapped_column(String(512))
    legenda: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ordem: Mapped[int] = mapped_column(Integer, default=0)
    ponto_risco: Mapped[str | None] = mapped_column(String(512), nullable=True)

    laudo: Mapped["Laudo"] = relationship(back_populates="fotos")  # noqa: F821
