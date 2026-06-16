from .cliente import ClienteCreate, ClienteUpdate, ClienteOut
from .maquina import MaquinaCreate, MaquinaUpdate, MaquinaOut
from .laudo import LaudoCreate, LaudoUpdate, LaudoOut, LaudoDetalhe
from .foto import FotoCreate, FotoUpdate, FotoOut, FotoReorder
from .perigo import PerigoCreate, PerigoUpdate, PerigoOut
from .acao import AcaoCreate, AcaoUpdate, AcaoOut
from .hrn import HRNAvaliarIn, HRNAvaliarOut

__all__ = [
    "ClienteCreate", "ClienteUpdate", "ClienteOut",
    "MaquinaCreate", "MaquinaUpdate", "MaquinaOut",
    "LaudoCreate", "LaudoUpdate", "LaudoOut", "LaudoDetalhe",
    "FotoCreate", "FotoUpdate", "FotoOut", "FotoReorder",
    "PerigoCreate", "PerigoUpdate", "PerigoOut",
    "AcaoCreate", "AcaoUpdate", "AcaoOut",
    "HRNAvaliarIn", "HRNAvaliarOut",
]
