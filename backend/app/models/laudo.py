from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base

# Domínios controlados (validados também no Pydantic).
VARIANTES = ("enxuto", "detalhado")
STATUS = ("rascunho", "em_analise", "concluido")
PARECERES = ("conforme", "com_ressalvas", "nao_conforme")


class Laudo(Base):
    __tablename__ = "laudo"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    maquina_id: Mapped[int] = mapped_column(ForeignKey("maquina.id"))

    variante: Mapped[str] = mapped_column(String(16), default="enxuto")
    status: Mapped[str] = mapped_column(String(16), default="rascunho")
    # Parecer de conformidade: nulo até o engenheiro decidir explicitamente.
    # Nunca derivado automaticamente do HRN.
    parecer: Mapped[str | None] = mapped_column(String(16), nullable=True)

    data_emissao: Mapped[date | None] = mapped_column(Date, nullable=True)
    # Escala de FE adotada — documentar a escala é exigência da metodologia.
    escala_fe: Mapped[str | None] = mapped_column(String(512), nullable=True)

    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    # Chave do DOCX gerado mais recente, arquivado no storage.
    docx_key: Mapped[str | None] = mapped_column(String(512), nullable=True)

    cliente: Mapped["Cliente"] = relationship(back_populates="laudos")  # noqa: F821
    maquina: Mapped["Maquina"] = relationship(back_populates="laudos")  # noqa: F821
    fotos: Mapped[list["Foto"]] = relationship(  # noqa: F821
        back_populates="laudo", cascade="all, delete-orphan", order_by="Foto.ordem"
    )
    perigos: Mapped[list["Perigo"]] = relationship(  # noqa: F821
        back_populates="laudo", cascade="all, delete-orphan", order_by="Perigo.id"
    )
    acoes: Mapped[list["AcaoPlano"]] = relationship(  # noqa: F821
        back_populates="laudo", cascade="all, delete-orphan", order_by="AcaoPlano.id"
    )
