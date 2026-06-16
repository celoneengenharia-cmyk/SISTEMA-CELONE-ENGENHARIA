"""Motor de cálculo HRN — fonte da verdade.

HRN = LO × FE × DPH × NP, com fatores escolhidos das tabelas fixas da escala
ABNT NBR ISO/TR 14121-2. O cálculo e a classificação por faixa rodam aqui, no
backend; o frontend espelha as mesmas tabelas apenas para refletir em tempo real.

Princípio inegociável da metodologia: o HRN é a estimativa quantitativa do risco.
Ele nunca se mistura com a Categoria de segurança (NBR 14153 / PL ISO 13849-1),
que pertence a uma função de segurança — entidade separada de uma fase futura.
"""
from __future__ import annotations

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Tabelas de fatores: valor -> descrição (escala ABNT NBR ISO/TR 14121-2).
# A ordem é a da metodologia; os valores são a fonte da verdade.
# ---------------------------------------------------------------------------

LO: dict[float, str] = {
    0.033: "Quase impossível — só em circunstâncias extremas",
    0.5: "Altamente improvável",
    1: "Improvável, embora possível",
    1.5: "Possível",
    2: "Alguma chance",
    5: "Provável",
    8: "Provável a alta",
    10: "Muito provável",
    15: "Certeza — já documentado",
}

FE: dict[float, str] = {
    0.1: "Anualmente",
    0.2: "Mensalmente",
    1: "Semanalmente",
    1.5: "Diariamente",
    2.5: "Por hora",
    4: "Constantemente",
    5: "A cada minuto",
}

DPH: dict[float, str] = {
    0.1: "Arranhão / hematoma",
    0.5: "Corte / laceração leve",
    1: "Lesão leve, afastamento curto",
    2: "Afastamento — corte profundo, fratura simples",
    4: "Perda de 1 dedo / sequela menor",
    6: "Amputação parcial mão-pé · perda de visão (1 olho) · perda auditiva",
    8: "Amputação de membro · cegueira · fatalidade individual",
    10: "Múltiplas amputações · fatalidade",
    15: "Múltiplas fatalidades",
}

NP: dict[float, str] = {
    1: "1 pessoa",
    2: "2 pessoas",
    4: "3 a 7 pessoas",
    8: "8 a 15 pessoas",
    12: "Mais de 15 pessoas",
}

FACTOR_TABLES: dict[str, dict[float, str]] = {"lo": LO, "fe": FE, "dph": DPH, "np": NP}
FACTOR_NAMES: dict[str, str] = {
    "lo": "Probabilidade de ocorrência",
    "fe": "Frequência de exposição",
    "dph": "Grau do possível dano",
    "np": "Pessoas expostas",
}


# ---------------------------------------------------------------------------
# Faixas de classificação do HRN.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Band:
    indice: int
    nome: str
    minimo: float
    maximo: float
    tratamento: str


# min inclusivo / max exclusivo, exceto a última (aberta). Um HRN igual ao limite
# sobe para a faixa seguinte — mesma convenção do protótipo (h >= min).
BANDS: list[Band] = [
    Band(0, "Aceitável", 0, 1, "Sem ação obrigatória"),
    Band(1, "Muito baixo", 1, 5, "Monitoramento, melhoria contínua"),
    Band(2, "Baixo", 5, 10, "Ação a planejar"),
    Band(3, "Significativo", 10, 50, "Ação necessária"),
    Band(4, "Alto", 50, 100, "Ação urgente"),
    Band(5, "Muito alto", 100, 500, "Ação imediata, condicionar operação"),
    Band(6, "Extremo", 500, 1000, "Parar a operação até mitigação"),
    Band(7, "Inaceitável", 1000, float("inf"), "Parar imediatamente"),
]


class HRNError(ValueError):
    """Fator fora da tabela fixa da escala."""


def _validate_factor(code: str, value: float) -> float:
    table = FACTOR_TABLES[code]
    # Comparação tolerante a float (0.033 etc.) contra as chaves da tabela.
    for key in table:
        if abs(float(key) - float(value)) < 1e-9:
            return float(key)
    raise HRNError(
        f"Valor {value!r} inválido para o fator {code.upper()}; "
        f"use um da escala: {sorted(table)}"
    )


def calcular_hrn(lo: float, fe: float, dph: float, np: float) -> float:
    """HRN = LO × FE × DPH × NP, validando cada fator contra a escala."""
    lo = _validate_factor("lo", lo)
    fe = _validate_factor("fe", fe)
    dph = _validate_factor("dph", dph)
    np = _validate_factor("np", np)
    return round(lo * fe * dph * np, 2)


def classificar(hrn: float) -> Band:
    """Retorna a faixa correta para um HRN (maior faixa cujo mínimo <= hrn)."""
    banda = BANDS[0]
    for b in BANDS:
        if hrn >= b.minimo:
            banda = b
    return banda


def classificar_nome(hrn: float) -> str:
    return classificar(hrn).nome


@dataclass
class AvaliacaoHRN:
    """Resultado completo da apreciação de um perigo (antes/depois + validação)."""

    hrn_atual: float
    classif_atual: str
    indice_atual: int
    hrn_pos: float | None
    classif_pos: str | None
    indice_pos: int | None
    queda_faixas: int | None
    nivel_validacao: str  # "ok" | "warn" | "bad" | "incompleto"
    mensagem_validacao: str
    fatores_pendentes: list[str]


def avaliar(
    *,
    lo: float,
    fe: float,
    dph: float,
    np: float,
    lo_pos: float | None = None,
    fe_pos: float | None = None,
    dph_pos: float | None = None,
    np_pos: float | None = None,
    justificativas: dict[str, str] | None = None,
) -> AvaliacaoHRN:
    """Avalia um perigo: HRN antes/depois, classificação e validações.

    As validações alertam, nunca bloqueiam (a decisão é do engenheiro):
    - o HRN depois deve cair pelo menos uma faixa;
    - o HRN depois não pode ser maior que o de antes (inconsistência);
    - cada fator deve ter justificativa — sem ela, o fator fica "pendente".
    """
    justificativas = justificativas or {}
    hrn_atual = calcular_hrn(lo, fe, dph, np)
    banda_atual = classificar(hrn_atual)

    pendentes = [
        c for c in ("lo", "fe", "dph", "np") if not (justificativas.get(c) or "").strip()
    ]

    tem_pos = None not in (lo_pos, fe_pos, dph_pos, np_pos)
    if not tem_pos:
        return AvaliacaoHRN(
            hrn_atual=hrn_atual,
            classif_atual=banda_atual.nome,
            indice_atual=banda_atual.indice,
            hrn_pos=None,
            classif_pos=None,
            indice_pos=None,
            queda_faixas=None,
            nivel_validacao="incompleto",
            mensagem_validacao="Apreciação incompleta — defina os fatores após as medidas.",
            fatores_pendentes=pendentes,
        )

    hrn_pos = calcular_hrn(lo_pos, fe_pos, dph_pos, np_pos)  # type: ignore[arg-type]
    banda_pos = classificar(hrn_pos)
    queda = banda_atual.indice - banda_pos.indice

    if banda_pos.indice > banda_atual.indice:
        nivel = "bad"
        msg = (
            "O risco aumentou após as medidas — o HRN de 'depois' não pode ser "
            "maior que o de 'antes'. Revise os fatores."
        )
    elif queda <= 0:
        nivel = "warn"
        msg = (
            "Sem redução de faixa. A apreciação só se completa quando o HRN cai "
            "pelo menos uma faixa; reforce as medidas de redução."
        )
    else:
        nivel = "ok"
        plural = "s" if queda > 1 else ""
        msg = (
            f"Risco reduzido em {queda} faixa{plural} — de '{banda_atual.nome}' "
            f"para '{banda_pos.nome}'."
        )

    return AvaliacaoHRN(
        hrn_atual=hrn_atual,
        classif_atual=banda_atual.nome,
        indice_atual=banda_atual.indice,
        hrn_pos=hrn_pos,
        classif_pos=banda_pos.nome,
        indice_pos=banda_pos.indice,
        queda_faixas=queda,
        nivel_validacao=nivel,
        mensagem_validacao=msg,
        fatores_pendentes=pendentes,
    )


def tabelas_para_frontend() -> dict:
    """Serializa as tabelas e faixas para o frontend espelhar a UI."""
    return {
        "fatores": {
            code: {
                "nome": FACTOR_NAMES[code],
                "opcoes": [{"valor": v, "descricao": d} for v, d in table.items()],
            }
            for code, table in FACTOR_TABLES.items()
        },
        "faixas": [
            {
                "indice": b.indice,
                "nome": b.nome,
                "min": b.minimo,
                "max": None if b.maximo == float("inf") else b.maximo,
                "tratamento": b.tratamento,
            }
            for b in BANDS
        ],
        "niveis_iso12100": [
            {"codigo": "M1", "descricao": "Projeto intrinsecamente seguro"},
            {"codigo": "M2", "descricao": "Proteção / dispositivo de segurança"},
            {"codigo": "M3", "descricao": "Informação para uso"},
            {"codigo": "M4", "descricao": "EPI"},
        ],
    }
