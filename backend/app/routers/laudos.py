from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Cliente, Laudo, Maquina
from ..schemas import LaudoCreate, LaudoDetalhe, LaudoOut, LaudoUpdate
from ..services import docx_service

router = APIRouter(prefix="/laudos", tags=["laudos"])


@router.get("", response_model=list[LaudoOut])
def listar(db: Session = Depends(get_db)):
    return db.scalars(select(Laudo).order_by(Laudo.id.desc())).all()


@router.post("", response_model=LaudoDetalhe, status_code=201)
def criar(payload: LaudoCreate, db: Session = Depends(get_db)):
    if not db.get(Cliente, payload.cliente_id):
        raise HTTPException(422, "Cliente inexistente")
    if not db.get(Maquina, payload.maquina_id):
        raise HTTPException(422, "Máquina inexistente")
    obj = Laudo(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{laudo_id}", response_model=LaudoDetalhe)
def obter(laudo_id: int, db: Session = Depends(get_db)):
    obj = db.get(Laudo, laudo_id)
    if not obj:
        raise HTTPException(404, "Laudo não encontrado")
    return obj


@router.patch("/{laudo_id}", response_model=LaudoDetalhe)
def atualizar(laudo_id: int, payload: LaudoUpdate, db: Session = Depends(get_db)):
    obj = db.get(Laudo, laudo_id)
    if not obj:
        raise HTTPException(404, "Laudo não encontrado")
    data = payload.model_dump(exclude_unset=True)
    if "cliente_id" in data and not db.get(Cliente, data["cliente_id"]):
        raise HTTPException(422, "Cliente inexistente")
    if "maquina_id" in data and not db.get(Maquina, data["maquina_id"]):
        raise HTTPException(422, "Máquina inexistente")
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{laudo_id}", status_code=204)
def remover(laudo_id: int, db: Session = Depends(get_db)):
    obj = db.get(Laudo, laudo_id)
    if not obj:
        raise HTTPException(404, "Laudo não encontrado")
    db.delete(obj)
    db.commit()


@router.post("/{laudo_id}/docx")
def gerar_docx(laudo_id: int, db: Session = Depends(get_db)):
    """Monta o JSON do laudo, chama o gerador e devolve o .docx (arquivando-o)."""
    laudo = db.get(Laudo, laudo_id)
    if not laudo:
        raise HTTPException(404, "Laudo não encontrado")
    key, conteudo = docx_service.gerar(laudo)
    laudo.docx_key = key
    db.commit()
    filename = f"laudo-{laudo_id}.docx"
    return Response(
        content=conteudo,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
