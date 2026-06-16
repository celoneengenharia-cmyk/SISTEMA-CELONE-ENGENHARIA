from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class MaquinaBase(BaseModel):
    tipo: str
    fabricante: str | None = None
    modelo: str | None = None
    serie: str | None = None
    ano: str | None = None
    funcao: str | None = None
    localizacao: str | None = None
    anexo_nr12: str | None = None


class MaquinaCreate(MaquinaBase):
    pass


class MaquinaUpdate(BaseModel):
    tipo: str | None = None
    fabricante: str | None = None
    modelo: str | None = None
    serie: str | None = None
    ano: str | None = None
    funcao: str | None = None
    localizacao: str | None = None
    anexo_nr12: str | None = None


class MaquinaOut(MaquinaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
