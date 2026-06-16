from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PerigoCreate(BaseModel):
    tipo: str | None = None
    fase_vida: str | None = None
    descricao: str | None = None

    # Fatores ANTES (obrigatórios — o HRN atual sempre existe).
    lo: float
    fe: float
    dph: float
    np: float
    justificativas: dict[str, str] = Field(default_factory=dict)

    medidas: list[str] = Field(default_factory=list)

    # Fatores APÓS (opcionais até o engenheiro reavaliar).
    lo_pos: float | None = None
    fe_pos: float | None = None
    dph_pos: float | None = None
    np_pos: float | None = None

    normas_violadas: list[str] = Field(default_factory=list)


class PerigoUpdate(BaseModel):
    tipo: str | None = None
    fase_vida: str | None = None
    descricao: str | None = None
    lo: float | None = None
    fe: float | None = None
    dph: float | None = None
    np: float | None = None
    justificativas: dict[str, str] | None = None
    medidas: list[str] | None = None
    lo_pos: float | None = None
    fe_pos: float | None = None
    dph_pos: float | None = None
    np_pos: float | None = None
    normas_violadas: list[str] | None = None


class PerigoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    laudo_id: int
    tipo: str | None
    fase_vida: str | None
    descricao: str | None
    lo: float
    fe: float
    dph: float
    np: float
    justificativas: dict[str, str]
    hrn_atual: float
    classif_atual: str | None
    medidas: list[str]
    lo_pos: float | None
    fe_pos: float | None
    dph_pos: float | None
    np_pos: float | None
    hrn_pos: float | None
    classif_pos: str | None
    normas_violadas: list[str]

    # Campos derivados da avaliação (não persistidos), úteis ao frontend.
    queda_faixas: int | None = None
    nivel_validacao: str | None = None
    mensagem_validacao: str | None = None
    fatores_pendentes: list[str] = []
