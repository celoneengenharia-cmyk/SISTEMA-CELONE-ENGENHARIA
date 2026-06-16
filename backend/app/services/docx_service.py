"""Ponte entre a API e o gerador de DOCX (generator/gerar_laudo.py).

Monta o JSON no esquema que o gerador consome, resolve os paths das fotos no
storage e produz o .docx na variante escolhida. Não reescreve o gerador — apenas
o envolve como serviço chamado pela API.
"""
from __future__ import annotations

import importlib.util
import sys
from datetime import datetime
from pathlib import Path

from ..config import CELONE
from ..models import Laudo
from .storage import get_storage

# Importa o gerador do diretório /generator (fora do pacote app).
_GEN_PATH = Path(__file__).resolve().parents[3] / "generator" / "gerar_laudo.py"


def _load_generator():
    spec = importlib.util.spec_from_file_location("gerar_laudo", _GEN_PATH)
    if spec is None or spec.loader is None:  # pragma: no cover
        raise RuntimeError(f"Gerador não encontrado em {_GEN_PATH}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gerar_laudo"] = mod
    spec.loader.exec_module(mod)
    return mod


def montar_json(laudo: Laudo) -> dict:
    """Constrói o dicionário de entrada do gerador a partir de um Laudo ORM."""
    storage = get_storage()
    cli = laudo.cliente
    maq = laudo.maquina

    fotos = []
    for f in sorted(laudo.fotos, key=lambda x: x.ordem):
        p = storage.path(f.storage_key)
        fotos.append({
            "path": str(p) if p.exists() else None,
            "legenda": f.legenda,
            "ponto_risco": f.ponto_risco,
        })

    perigos = []
    for pg in laudo.perigos:
        perigos.append({
            "tipo": pg.tipo,
            "fase_vida": pg.fase_vida,
            "descricao": pg.descricao,
            "fatores_antes": {"LO": pg.lo, "FE": pg.fe, "DPH": pg.dph, "NP": pg.np},
            "justificativas": pg.justificativas or {},
            "hrn_atual": pg.hrn_atual,
            "classif_atual": pg.classif_atual,
            "medidas": pg.medidas or [],
            "fatores_apos": {
                "LO": pg.lo_pos, "FE": pg.fe_pos, "DPH": pg.dph_pos, "NP": pg.np_pos
            },
            "hrn_pos": pg.hrn_pos,
            "classif_pos": pg.classif_pos,
            "normas_violadas": pg.normas_violadas or [],
        })

    plano = [{
        "acao": a.acao,
        "prioridade": a.prioridade,
        "prazo": a.prazo.isoformat() if a.prazo else None,
        "responsavel": a.responsavel,
        "classif_hrn": a.classif_hrn,
    } for a in laudo.acoes]

    # Normas consolidadas (união das normas citadas nos perigos).
    normas: list[str] = []
    for pg in laudo.perigos:
        for n in (pg.normas_violadas or []):
            if n and n not in normas:
                normas.append(n)

    return {
        "variante": laudo.variante,
        "empresa": CELONE,
        "cliente": {
            "nome": cli.nome, "cnpj": cli.cnpj,
            "endereco": cli.endereco, "contato": cli.contato,
        },
        "maquina": {
            "tipo": maq.tipo, "fabricante": maq.fabricante, "modelo": maq.modelo,
            "serie": maq.serie, "ano": maq.ano, "funcao": maq.funcao,
            "localizacao": maq.localizacao, "anexo_nr12": maq.anexo_nr12,
        },
        "laudo": {
            "data_emissao": laudo.data_emissao.isoformat() if laudo.data_emissao else None,
            "escala_fe": laudo.escala_fe,
            "parecer": laudo.parecer,
            "status": laudo.status,
        },
        "fotos": fotos,
        "perigos": perigos,
        "plano_acao": plano,
        "normas": normas,
        "conclusao": None,
    }


def gerar(laudo: Laudo) -> tuple[str, bytes]:
    """Gera o .docx do laudo, arquiva no storage e devolve (key, bytes)."""
    import io

    data = montar_json(laudo)
    gen = _load_generator()

    doc = gen.gerar_documento(data)
    buf = io.BytesIO()
    doc.save(buf)
    conteudo = buf.getvalue()

    nome = f"laudo-{laudo.id}-{datetime.now():%Y%m%d-%H%M%S}.docx"
    key = get_storage().save_bytes(conteudo, prefix="docx", filename=nome)
    return key, conteudo
