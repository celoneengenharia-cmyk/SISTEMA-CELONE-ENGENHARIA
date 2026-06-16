from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict


class AcaoCreate(BaseModel):
    perigo_id: int | None = None
    acao: str
    prioridade: str | None = None
    prazo: date | None = None
    responsavel: str | None = None
    classif_hrn: str | None = None


class AcaoUpdate(BaseModel):
    perigo_id: int | None = None
    acao: str | None = None
    prioridade: str | None = None
    prazo: date | None = None
    responsavel: str | None = None
    classif_hrn: str | None = None


class AcaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    laudo_id: int
    perigo_id: int | None
    acao: str
    prioridade: str | None
    prazo: date | None
    responsavel: str | None
    classif_hrn: str | None
