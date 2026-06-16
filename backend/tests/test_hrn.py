"""Testes do motor HRN — cálculo e classificação são a lógica crítica."""
import math

import pytest

from app.services import hrn


# --- cálculo -------------------------------------------------------------


def test_hrn_multiplica_os_quatro_fatores():
    # 8 × 2.5 × 8 × 2 = 320
    assert hrn.calcular_hrn(8, 2.5, 8, 2) == 320

def test_hrn_arredonda_para_duas_casas():
    # 0.033 × 0.1 × 0.1 × 1 = 0.00033 -> 0.0
    assert hrn.calcular_hrn(0.033, 0.1, 0.1, 1) == 0.0
    # 1.5 × 1.5 × 0.5 × 1 = 1.125 -> 1.12 (half-even do round)
    assert hrn.calcular_hrn(1.5, 1.5, 0.5, 1) == 1.12

def test_hrn_minimo_e_maximo_da_escala():
    assert hrn.calcular_hrn(0.033, 0.1, 0.1, 1) == 0.0
    assert hrn.calcular_hrn(15, 5, 15, 12) == 13500.0

def test_fator_fora_da_escala_levanta_erro():
    with pytest.raises(hrn.HRNError):
        hrn.calcular_hrn(7, 2.5, 8, 2)  # 7 não existe na escala LO


# --- classificação por faixa --------------------------------------------


@pytest.mark.parametrize(
    "valor,esperado",
    [
        (0, "Aceitável"),
        (0.5, "Aceitável"),
        (1, "Muito baixo"),      # limite sobe de faixa
        (4.9, "Muito baixo"),
        (5, "Baixo"),
        (9.9, "Baixo"),
        (10, "Significativo"),
        (49, "Significativo"),
        (50, "Alto"),
        (99, "Alto"),
        (100, "Muito alto"),
        (499, "Muito alto"),
        (500, "Extremo"),
        (999, "Extremo"),
        (1000, "Inaceitável"),
        (13500, "Inaceitável"),
    ],
)
def test_classificacao_em_cada_faixa(valor, esperado):
    assert hrn.classificar_nome(valor) == esperado


def test_todas_as_faixas_cobrem_o_continuo_sem_buraco():
    # cada max é o min da faixa seguinte; a última é aberta
    for a, b in zip(hrn.BANDS, hrn.BANDS[1:]):
        assert a.maximo == b.minimo
    assert math.isinf(hrn.BANDS[-1].maximo)


# --- avaliação completa + validações ------------------------------------


def test_avaliacao_sem_pos_fica_incompleta():
    r = hrn.avaliar(lo=8, fe=2.5, dph=8, np=2)
    assert r.hrn_atual == 320
    assert r.classif_atual == "Muito alto"
    assert r.hrn_pos is None
    assert r.nivel_validacao == "incompleto"


def test_avaliacao_ok_quando_cai_pelo_menos_uma_faixa():
    r = hrn.avaliar(
        lo=8, fe=2.5, dph=8, np=2,        # 320 -> Muito alto (idx 5)
        lo_pos=0.5, fe_pos=2.5, dph_pos=8, np_pos=2,  # 20 -> Significativo (idx 3)
    )
    assert r.nivel_validacao == "ok"
    assert r.queda_faixas == 2


def test_avaliacao_warn_quando_nao_muda_de_faixa():
    r = hrn.avaliar(
        lo=8, fe=2.5, dph=8, np=2,        # 320 -> Muito alto
        lo_pos=5, fe_pos=2.5, dph_pos=8, np_pos=2,    # 200 -> Muito alto (mesma faixa)
    )
    assert r.nivel_validacao == "warn"
    assert r.queda_faixas == 0


def test_avaliacao_bad_quando_risco_aumenta():
    r = hrn.avaliar(
        lo=0.5, fe=2.5, dph=8, np=2,      # 20 -> Significativo
        lo_pos=8, fe_pos=2.5, dph_pos=8, np_pos=2,    # 320 -> Muito alto
    )
    assert r.nivel_validacao == "bad"


def test_fatores_sem_justificativa_ficam_pendentes():
    r = hrn.avaliar(lo=8, fe=2.5, dph=8, np=2, justificativas={"lo": "histórico"})
    assert "lo" not in r.fatores_pendentes
    assert set(r.fatores_pendentes) == {"fe", "dph", "np"}
