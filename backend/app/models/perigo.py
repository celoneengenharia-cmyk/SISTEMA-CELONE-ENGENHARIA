from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base, JSONType


class Perigo(Base):
    """O coração da apreciação.

    REGRA DE PROJETO INEGOCIÁVEL: Perigo NÃO tem campo de Categoria de segurança.
    HRN é a estimativa quantitativa do risco; Categoria (NBR 14153 / PL ISO
    13849-1) é a robustez de um circuito de comando e pertence a uma *função de
    segurança* — entidade separada de uma fase futura. Nunca pendure Categoria
    num perigo.
    """

    __tablename__ = "perigo"

    id: Mapped[int] = mapped_column(primary_key=True)
    laudo_id: Mapped[int] = mapped_column(ForeignKey("laudo.id", ondelete="CASCADE"))

    tipo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fase_vida: Mapped[str | None] = mapped_column(String(255), nullable=True)
    descricao: Mapped[str | None] = mapped_column(String(1024), nullable=True)  # modo de falha

    # Fatores ANTES (valores numéricos da escala).
    lo: Mapped[float] = mapped_column(Float)
    fe: Mapped[float] = mapped_column(Float)
    dph: Mapped[float] = mapped_column(Float)
    np: Mapped[float] = mapped_column(Float)
    # Justificativa por fator (mapa fator -> texto). Regra: "nunca suponha".
    justificativas: Mapped[dict] = mapped_column(JSONType, default=dict)

    hrn_atual: Mapped[float] = mapped_column(Float, default=0)
    classif_atual: Mapped[str | None] = mapped_column(String(32), nullable=True)

    # Medidas pela hierarquia ISO 12100, prefixadas "M1 — …" … "M4 — …".
    medidas: Mapped[list] = mapped_column(JSONType, default=list)

    # Fatores APÓS as medidas (nulos até o engenheiro reavaliar).
    lo_pos: Mapped[float | None] = mapped_column(Float, nullable=True)
    fe_pos: Mapped[float | None] = mapped_column(Float, nullable=True)
    dph_pos: Mapped[float | None] = mapped_column(Float, nullable=True)
    np_pos: Mapped[float | None] = mapped_column(Float, nullable=True)

    hrn_pos: Mapped[float | None] = mapped_column(Float, nullable=True)
    classif_pos: Mapped[str | None] = mapped_column(String(32), nullable=True)

    normas_violadas: Mapped[list] = mapped_column(JSONType, default=list)
    ordem: Mapped[int] = mapped_column(Integer, default=0)

    laudo: Mapped["Laudo"] = relationship(back_populates="perigos")  # noqa: F821
    acoes: Mapped[list["AcaoPlano"]] = relationship(  # noqa: F821
        back_populates="perigo", cascade="all, delete-orphan"
    )
