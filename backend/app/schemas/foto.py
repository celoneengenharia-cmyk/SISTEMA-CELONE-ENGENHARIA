from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FotoCreate(BaseModel):
    # O binário vem via multipart; estes são os metadados.
    legenda: str | None = None
    ponto_risco: str | None = None


class FotoUpdate(BaseModel):
    legenda: str | None = None
    ponto_risco: str | None = None
    ordem: int | None = None


class FotoReorder(BaseModel):
    # Nova ordem: lista de ids de foto na sequência desejada.
    ordem_ids: list[int]


class FotoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    laudo_id: int
    storage_key: str
    legenda: str | None
    ordem: int
    ponto_risco: str | None
    url: str | None = None
