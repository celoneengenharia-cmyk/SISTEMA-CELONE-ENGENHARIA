from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Cliente
from ..schemas import ClienteCreate, ClienteOut, ClienteUpdate

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("", response_model=list[ClienteOut])
def listar(db: Session = Depends(get_db)):
    return db.scalars(select(Cliente).order_by(Cliente.nome)).all()


@router.post("", response_model=ClienteOut, status_code=201)
def criar(payload: ClienteCreate, db: Session = Depends(get_db)):
    obj = Cliente(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{cliente_id}", response_model=ClienteOut)
def obter(cliente_id: int, db: Session = Depends(get_db)):
    obj = db.get(Cliente, cliente_id)
    if not obj:
        raise HTTPException(404, "Cliente não encontrado")
    return obj


@router.patch("/{cliente_id}", response_model=ClienteOut)
def atualizar(cliente_id: int, payload: ClienteUpdate, db: Session = Depends(get_db)):
    obj = db.get(Cliente, cliente_id)
    if not obj:
        raise HTTPException(404, "Cliente não encontrado")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{cliente_id}", status_code=204)
def remover(cliente_id: int, db: Session = Depends(get_db)):
    obj = db.get(Cliente, cliente_id)
    if not obj:
        raise HTTPException(404, "Cliente não encontrado")
    db.delete(obj)
    db.commit()
