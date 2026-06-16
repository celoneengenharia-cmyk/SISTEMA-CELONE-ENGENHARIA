from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ClienteBase(BaseModel):
    nome: str
    cnpj: str | None = None
    endereco: str | None = None
    contato: str | None = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: str | None = None
    cnpj: str | None = None
    endereco: str | None = None
    contato: str | None = None


class ClienteOut(ClienteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
