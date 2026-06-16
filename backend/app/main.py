"""Aplicação FastAPI — Plataforma de Laudos NR-12 (Celone) · Fase 1."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import acoes, clientes, fotos, laudos, maquinas, meta, perigos

settings = get_settings()

app = FastAPI(
    title="Plataforma de Laudos NR-12 — Celone Engenharia",
    description="Fase 1 (MVP): motor HRN, galeria de fotos e geração de DOCX.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meta.router)
app.include_router(clientes.router)
app.include_router(maquinas.router)
app.include_router(laudos.router)
app.include_router(perigos.router)
app.include_router(fotos.router)
app.include_router(acoes.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}
