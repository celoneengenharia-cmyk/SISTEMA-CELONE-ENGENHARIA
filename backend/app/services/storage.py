"""Abstração de storage de arquivos.

Nesta fase o backend é disco local, mas tudo passa pela interface
`StorageBackend` para que trocar por S3/R2/MinIO depois não toque no resto.
"""
from __future__ import annotations

import shutil
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO

from ..config import get_settings


class StorageBackend(ABC):
    """Contrato de storage. O resto do sistema só conhece `key` (string)."""

    @abstractmethod
    def save(self, fileobj: BinaryIO, *, prefix: str, filename: str) -> str:
        """Grava o conteúdo e devolve a chave para recuperá-lo depois."""

    @abstractmethod
    def save_bytes(self, data: bytes, *, prefix: str, filename: str) -> str:
        ...

    @abstractmethod
    def path(self, key: str) -> Path:
        """Caminho físico de uma chave (usado pelo gerador de DOCX)."""

    @abstractmethod
    def delete(self, key: str) -> None:
        ...

    @abstractmethod
    def exists(self, key: str) -> bool:
        ...


class LocalStorage(StorageBackend):
    """Storage em disco local sob `settings.storage_dir`."""

    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = Path(base_dir or get_settings().storage_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _resolve(self, key: str) -> Path:
        p = (self.base_dir / key).resolve()
        # Defesa contra path traversal: a chave nunca pode escapar do base_dir.
        if not str(p).startswith(str(self.base_dir.resolve())):
            raise ValueError(f"Chave de storage inválida: {key!r}")
        return p

    def _new_key(self, prefix: str, filename: str) -> str:
        ext = Path(filename).suffix.lower()
        return f"{prefix.strip('/')}/{uuid.uuid4().hex}{ext}"

    def save(self, fileobj: BinaryIO, *, prefix: str, filename: str) -> str:
        key = self._new_key(prefix, filename)
        dest = self._resolve(key)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb") as out:
            shutil.copyfileobj(fileobj, out)
        return key

    def save_bytes(self, data: bytes, *, prefix: str, filename: str) -> str:
        key = self._new_key(prefix, filename)
        dest = self._resolve(key)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return key

    def path(self, key: str) -> Path:
        return self._resolve(key)

    def delete(self, key: str) -> None:
        p = self._resolve(key)
        if p.exists():
            p.unlink()

    def exists(self, key: str) -> bool:
        return self._resolve(key).exists()


_storage: StorageBackend | None = None


def get_storage() -> StorageBackend:
    """Singleton do storage (trocar a implementação aqui no futuro)."""
    global _storage
    if _storage is None:
        _storage = LocalStorage()
    return _storage
