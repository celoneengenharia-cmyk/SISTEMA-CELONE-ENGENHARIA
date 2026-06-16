"""Modelos do domínio. Importar este pacote registra tudo no metadata da Base."""
from .cliente import Cliente
from .maquina import Maquina
from .laudo import Laudo
from .foto import Foto
from .perigo import Perigo
from .acao_plano import AcaoPlano

__all__ = ["Cliente", "Maquina", "Laudo", "Foto", "Perigo", "AcaoPlano"]
