from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Foto, Laudo
from ..schemas import FotoOut, FotoReorder, FotoUpdate
from ..services.storage import get_storage

router = APIRouter(tags=["fotos"])

_IMG_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


def _to_out(f: Foto) -> FotoOut:
    out = FotoOut.model_validate(f)
    out.url = f"/fotos/{f.id}/arquivo"
    return out


@router.get("/laudos/{laudo_id}/fotos", response_model=list[FotoOut])
def listar(laudo_id: int, db: Session = Depends(get_db)):
    laudo = db.get(Laudo, laudo_id)
    if not laudo:
        raise HTTPException(404, "Laudo não encontrado")
    return [_to_out(f) for f in laudo.fotos]


@router.post("/laudos/{laudo_id}/fotos", response_model=list[FotoOut], status_code=201)
def upload(
    laudo_id: int,
    arquivos: list[UploadFile] = File(...),
    legenda: str | None = Form(None),
    db: Session = Depends(get_db),
):
    """Upload em lote. Cada arquivo entra ao final da ordem atual."""
    laudo = db.get(Laudo, laudo_id)
    if not laudo:
        raise HTTPException(404, "Laudo não encontrado")
    storage = get_storage()
    base_ordem = db.scalar(
        select(func.coalesce(func.max(Foto.ordem), -1)).where(Foto.laudo_id == laudo_id)
    )
    criadas: list[Foto] = []
    for i, up in enumerate(arquivos, start=1):
        if up.content_type not in _IMG_TYPES:
            raise HTTPException(415, f"Tipo não suportado: {up.content_type}")
        key = storage.save(up.file, prefix=f"fotos/{laudo_id}", filename=up.filename or "foto")
        foto = Foto(
            laudo_id=laudo_id, storage_key=key, legenda=legenda,
            ordem=base_ordem + i,
        )
        db.add(foto)
        criadas.append(foto)
    db.commit()
    for f in criadas:
        db.refresh(f)
    return [_to_out(f) for f in criadas]


@router.get("/fotos/{foto_id}/arquivo")
def baixar(foto_id: int, db: Session = Depends(get_db)):
    foto = db.get(Foto, foto_id)
    if not foto:
        raise HTTPException(404, "Foto não encontrada")
    path = get_storage().path(foto.storage_key)
    if not path.exists():
        raise HTTPException(404, "Arquivo não encontrado no storage")
    return FileResponse(path)


@router.patch("/fotos/{foto_id}", response_model=FotoOut)
def atualizar(foto_id: int, payload: FotoUpdate, db: Session = Depends(get_db)):
    foto = db.get(Foto, foto_id)
    if not foto:
        raise HTTPException(404, "Foto não encontrada")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(foto, k, v)
    db.commit()
    db.refresh(foto)
    return _to_out(foto)


@router.put("/laudos/{laudo_id}/fotos/ordem", response_model=list[FotoOut])
def reordenar(laudo_id: int, payload: FotoReorder, db: Session = Depends(get_db)):
    laudo = db.get(Laudo, laudo_id)
    if not laudo:
        raise HTTPException(404, "Laudo não encontrado")
    por_id = {f.id: f for f in laudo.fotos}
    if set(payload.ordem_ids) != set(por_id):
        raise HTTPException(422, "A lista de ids deve conter exatamente as fotos do laudo")
    for ordem, fid in enumerate(payload.ordem_ids):
        por_id[fid].ordem = ordem
    db.commit()
    return [_to_out(f) for f in sorted(por_id.values(), key=lambda x: x.ordem)]


@router.delete("/fotos/{foto_id}", status_code=204)
def remover(foto_id: int, db: Session = Depends(get_db)):
    foto = db.get(Foto, foto_id)
    if not foto:
        raise HTTPException(404, "Foto não encontrada")
    get_storage().delete(foto.storage_key)
    db.delete(foto)
    db.commit()
