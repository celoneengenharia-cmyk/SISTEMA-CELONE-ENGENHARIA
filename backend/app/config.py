"""Configurações da aplicação e constantes fixas da Celone Engenharia."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings carregadas do ambiente (com defaults para desenvolvimento)."""

    model_config = SettingsConfigDict(env_prefix="CELONE_", env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://celone:celone@localhost:5432/celone"
    # Diretório do storage local de fotos e DOCX gerados nesta fase.
    storage_dir: Path = Path("storage")
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


# Constantes da Celone — fixas no sistema (Fase 1). Entram no cabeçalho,
# na identificação e na responsabilidade técnica do laudo.
CELONE = {
    "empresa": "Celone Engenharia LTDA",
    "cnpj": "55.514.523/0001-48",
    "engenheiro": "Matteo Celone",
    "crea": "2118861648 (RN)",
    "email": "celoneengenharia@gmail.com",
    "telefone": "(84) 99113-7803",
    "site": "www.celoneengenharia.com",
}


@lru_cache
def get_settings() -> Settings:
    return Settings()
