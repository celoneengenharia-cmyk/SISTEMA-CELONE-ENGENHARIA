from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class AcaoPlano(Base):
    """Item do plano de ação consolidado, derivado de um perigo."""

    __tablename__ = "acao_plano"

    id: Mapped[int] = mapped_column(primary_key=True)
    laudo_id: Mapped[int] = mapped_column(ForeignKey("laudo.id", ondelete="CASCADE"))
    perigo_id: Mapped[int | None] = mapped_column(
        ForeignKey("perigo.id", ondelete="SET NULL"), nullable=True
    )

    acao: Mapped[str] = mapped_column(String(1024))
    prioridade: Mapped[str | None] = mapped_column(String(32), nullable=True)
    prazo: Mapped[date | None] = mapped_column(Date, nullable=True)
    responsavel: Mapped[str | None] = mapped_column(String(255), nullable=True)
    classif_hrn: Mapped[str | None] = mapped_column(String(32), nullable=True)

    laudo: Mapped["Laudo"] = relationship(back_populates="acoes")  # noqa: F821
    perigo: Mapped["Perigo"] = relationship(back_populates="acoes")  # noqa: F821
