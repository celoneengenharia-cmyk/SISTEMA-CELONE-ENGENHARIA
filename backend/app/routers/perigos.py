from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Laudo, Perigo
from ..schemas import PerigoCreate, PerigoOut, PerigoUpdate
from ..services import hrn

router = APIRouter(tags=["perigos"])


def aplicar_hrn(perigo: Perigo) -> hrn.AvaliacaoHRN:
    """Recalcula HRN/classificação no servidor (fonte da verdade) e grava no obj."""
    av = hrn.avaliar(
        lo=perigo.lo, fe=perigo.fe, dph=perigo.dph, np=perigo.np,
        lo_pos=perigo.lo_pos, fe_pos=perigo.fe_pos,
        dph_pos=perigo.dph_pos, np_pos=perigo.np_pos,
        justificativas=perigo.justificativas or {},
    )
    perigo.hrn_atual = av.hrn_atual
    perigo.classif_atual = av.classif_atual
    perigo.hrn_pos = av.hrn_pos
    perigo.classif_pos = av.classif_pos
    return av


def to_out(perigo: Perigo, av: hrn.AvaliacaoHRN | None = None) -> PerigoOut:
    if av is None:
        av = hrn.avaliar(
            lo=perigo.lo, fe=perigo.fe, dph=perigo.dph, np=perigo.np,
            lo_pos=perigo.lo_pos, fe_pos=perigo.fe_pos,
            dph_pos=perigo.dph_pos, np_pos=perigo.np_pos,
            justificativas=perigo.justificativas or {},
        )
    out = PerigoOut.model_validate(perigo)
    out.queda_faixas = av.queda_faixas
    out.nivel_validacao = av.nivel_validacao
    out.mensagem_validacao = av.mensagem_validacao
    out.fatores_pendentes = av.fatores_pendentes
    return out


@router.get("/laudos/{laudo_id}/perigos", response_model=list[PerigoOut])
def listar(laudo_id: int, db: Session = Depends(get_db)):
    laudo = db.get(Laudo, laudo_id)
    if not laudo:
        raise HTTPException(404, "Laudo não encontrado")
    return [to_out(p) for p in laudo.perigos]


@router.post("/laudos/{laudo_id}/perigos", response_model=PerigoOut, status_code=201)
def criar(laudo_id: int, payload: PerigoCreate, db: Session = Depends(get_db)):
    laudo = db.get(Laudo, laudo_id)
    if not laudo:
        raise HTTPException(404, "Laudo não encontrado")
    try:
        perigo = Perigo(laudo_id=laudo_id, **payload.model_dump())
        av = aplicar_hrn(perigo)
    except hrn.HRNError as e:
        raise HTTPException(422, str(e))
    db.add(perigo)
    db.commit()
    db.refresh(perigo)
    return to_out(perigo, av)


@router.patch("/perigos/{perigo_id}", response_model=PerigoOut)
def atualizar(perigo_id: int, payload: PerigoUpdate, db: Session = Depends(get_db)):
    perigo = db.get(Perigo, perigo_id)
    if not perigo:
        raise HTTPException(404, "Perigo não encontrado")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(perigo, k, v)
    try:
        av = aplicar_hrn(perigo)
    except hrn.HRNError as e:
        raise HTTPException(422, str(e))
    db.commit()
    db.refresh(perigo)
    return to_out(perigo, av)


@router.delete("/perigos/{perigo_id}", status_code=204)
def remover(perigo_id: int, db: Session = Depends(get_db)):
    perigo = db.get(Perigo, perigo_id)
    if not perigo:
        raise HTTPException(404, "Perigo não encontrado")
    db.delete(perigo)
    db.commit()
