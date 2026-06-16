from __future__ import annotations

from fastapi import APIRouter

from ..config import CELONE
from ..schemas import HRNAvaliarIn, HRNAvaliarOut
from ..services import hrn

router = APIRouter(tags=["meta"])


@router.get("/meta/hrn")
def tabelas_hrn():
    """Tabelas de fatores, faixas e níveis ISO 12100 para o frontend espelhar."""
    return hrn.tabelas_para_frontend()


@router.get("/meta/celone")
def constantes_celone():
    """Constantes fixas da Celone (cabeçalho, responsabilidade técnica)."""
    return CELONE


@router.post("/hrn/avaliar", response_model=HRNAvaliarOut)
def avaliar(payload: HRNAvaliarIn):
    """Avaliação ad-hoc do HRN (preview em tempo real, sem persistir)."""
    av = hrn.avaliar(**payload.model_dump())
    return HRNAvaliarOut(
        hrn_atual=av.hrn_atual,
        classif_atual=av.classif_atual,
        indice_atual=av.indice_atual,
        hrn_pos=av.hrn_pos,
        classif_pos=av.classif_pos,
        indice_pos=av.indice_pos,
        queda_faixas=av.queda_faixas,
        nivel_validacao=av.nivel_validacao,
        mensagem_validacao=av.mensagem_validacao,
        fatores_pendentes=av.fatores_pendentes,
    )
