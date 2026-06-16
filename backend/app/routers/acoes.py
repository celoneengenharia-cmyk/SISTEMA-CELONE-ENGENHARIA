from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import AcaoPlano, Laudo
from ..schemas import AcaoCreate, AcaoOut, AcaoUpdate

router = APIRouter(tags=["plano_acao"])


@router.get("/laudos/{laudo_id}/acoes", response_model=list[AcaoOut])
def listar(laudo_id: int, db: Session = Depends(get_db)):
    laudo = db.get(Laudo, laudo_id)
    if not laudo:
        raise HTTPException(404, "Laudo não encontrado")
    return laudo.acoes


@router.post("/laudos/{laudo_id}/acoes", response_model=AcaoOut, status_code=201)
def criar(laudo_id: int, payload: AcaoCreate, db: Session = Depends(get_db)):
    if not db.get(Laudo, laudo_id):
        raise HTTPException(404, "Laudo não encontrado")
    obj = AcaoPlano(laudo_id=laudo_id, **payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/acoes/{acao_id}", response_model=AcaoOut)
def atualizar(acao_id: int, payload: AcaoUpdate, db: Session = Depends(get_db)):
    obj = db.get(AcaoPlano, acao_id)
    if not obj:
        raise HTTPException(404, "Ação não encontrada")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/acoes/{acao_id}", status_code=204)
def remover(acao_id: int, db: Session = Depends(get_db)):
    obj = db.get(AcaoPlano, acao_id)
    if not obj:
        raise HTTPException(404, "Ação não encontrada")
    db.delete(obj)
    db.commit()
