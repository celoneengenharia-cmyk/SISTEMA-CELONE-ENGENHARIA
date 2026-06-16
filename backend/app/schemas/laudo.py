from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict

from .cliente import ClienteOut
from .maquina import MaquinaOut

Variante = Literal["enxuto", "detalhado"]
Status = Literal["rascunho", "em_analise", "concluido"]
Parecer = Literal["conforme", "com_ressalvas", "nao_conforme"]


class LaudoCreate(BaseModel):
    cliente_id: int
    maquina_id: int
    variante: Variante = "enxuto"
    escala_fe: str | None = None
    data_emissao: date | None = None


class LaudoUpdate(BaseModel):
    cliente_id: int | None = None
    maquina_id: int | None = None
    variante: Variante | None = None
    status: Status | None = None
    parecer: Parecer | None = None
    escala_fe: str | None = None
    data_emissao: date | None = None


class LaudoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cliente_id: int
    maquina_id: int
    variante: Variante
    status: Status
    parecer: Parecer | None
    escala_fe: str | None
    data_emissao: date | None
    docx_key: str | None


class LaudoDetalhe(LaudoOut):
    """Laudo com cliente e máquina embutidos (resposta de detalhe)."""
    cliente: ClienteOut
    maquina: MaquinaOut
