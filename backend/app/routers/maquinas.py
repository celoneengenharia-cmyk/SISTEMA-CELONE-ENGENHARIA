from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Maquina
from ..schemas import MaquinaCreate, MaquinaOut, MaquinaUpdate

router = APIRouter(prefix="/maquinas", tags=["maquinas"])


@router.get("", response_model=list[MaquinaOut])
def listar(db: Session = Depends(get_db)):
    return db.scalars(select(Maquina).order_by(Maquina.tipo)).all()


@router.post("", response_model=MaquinaOut, status_code=201)
def criar(payload: MaquinaCreate, db: Session = Depends(get_db)):
    obj = Maquina(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{maquina_id}", response_model=MaquinaOut)
def obter(maquina_id: int, db: Session = Depends(get_db)):
    obj = db.get(Maquina, maquina_id)
    if not obj:
        raise HTTPException(404, "Máquina não encontrada")
    return obj


@router.patch("/{maquina_id}", response_model=MaquinaOut)
def atualizar(maquina_id: int, payload: MaquinaUpdate, db: Session = Depends(get_db)):
    obj = db.get(Maquina, maquina_id)
    if not obj:
        raise HTTPException(404, "Máquina não encontrada")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{maquina_id}", status_code=204)
def remover(maquina_id: int, db: Session = Depends(get_db)):
    obj = db.get(Maquina, maquina_id)
    if not obj:
        raise HTTPException(404, "Máquina não encontrada")
    db.delete(obj)
    db.commit()
