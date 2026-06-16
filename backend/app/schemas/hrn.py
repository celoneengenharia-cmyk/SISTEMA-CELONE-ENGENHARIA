from __future__ import annotations

from pydantic import BaseModel, Field


class HRNAvaliarIn(BaseModel):
    """Avaliação ad-hoc do HRN (preview, sem persistir)."""
    lo: float
    fe: float
    dph: float
    np: float
    lo_pos: float | None = None
    fe_pos: float | None = None
    dph_pos: float | None = None
    np_pos: float | None = None
    justificativas: dict[str, str] = Field(default_factory=dict)


class HRNAvaliarOut(BaseModel):
    hrn_atual: float
    classif_atual: str
    indice_atual: int
    hrn_pos: float | None
    classif_pos: str | None
    indice_pos: int | None
    queda_faixas: int | None
    nivel_validacao: str
    mensagem_validacao: str
    fatores_pendentes: list[str]
