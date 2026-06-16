"""Popula um laudo de exemplo para testar a plataforma sem digitar nada.

Uso (a partir de /backend, com a venv ativa):

    python seed.py

No SQLite (CELONE_DATABASE_URL=sqlite:///./celone.db) o script também cria as
tabelas automaticamente. No Postgres, rode antes `alembic upgrade head`.
"""
from __future__ import annotations

from datetime import date

from app.db import Base, SessionLocal, engine, settings
from app.models import AcaoPlano, Cliente, Laudo, Maquina, Perigo
from app.services import hrn


def _set_hrn(p: Perigo) -> None:
    """Calcula HRN/classificação no servidor (a mesma fonte da verdade da API)."""
    av = hrn.avaliar(
        lo=p.lo, fe=p.fe, dph=p.dph, np=p.np,
        lo_pos=p.lo_pos, fe_pos=p.fe_pos, dph_pos=p.dph_pos, np_pos=p.np_pos,
        justificativas=p.justificativas or {},
    )
    p.hrn_atual, p.classif_atual = av.hrn_atual, av.classif_atual
    p.hrn_pos, p.classif_pos = av.hrn_pos, av.classif_pos


def main() -> None:
    if settings.database_url.startswith("sqlite"):
        # Atalho de teste: no SQLite criamos o schema direto, sem Alembic.
        Base.metadata.create_all(engine)
        print("→ SQLite detectado: tabelas criadas via create_all.")

    db = SessionLocal()
    try:
        cliente = Cliente(
            nome="Indústria Exemplo S.A.", cnpj="00.000.000/0001-00",
            endereco="Av. das Indústrias, 1000 — Natal/RN", contato="João da Silva",
        )
        maquina = Maquina(
            tipo="Prensa hidráulica", fabricante="ACME", modelo="PH-200",
            serie="SN-2019-0042", ano="2019", funcao="Estampagem de chapas",
            localizacao="Setor A — linha 3", anexo_nr12="Anexo VIII",
        )
        db.add_all([cliente, maquina])
        db.flush()

        laudo = Laudo(
            cliente_id=cliente.id, maquina_id=maquina.id, variante="enxuto",
            status="em_analise", escala_fe="FE conforme ABNT NBR ISO/TR 14121-2",
            data_emissao=date.today(),
        )
        db.add(laudo)
        db.flush()

        p1 = Perigo(
            laudo_id=laudo.id, tipo="Mecânico — esmagamento", fase_vida="Operação normal",
            descricao="Esmagamento na zona de operação (entre punção e matriz)",
            lo=8, fe=2.5, dph=8, np=2,
            justificativas={
                "lo": "Acesso direto à zona sem proteção; histórico de quase-acidentes",
                "fe": "Operador alimenta peças por hora",
                "dph": "Membro superior exposto ao ponto de prensagem",
                "np": "Operador + auxiliar",
            },
            medidas=[
                "M2 — Proteção fixa distante com intertravamento na abertura",
                "M3 — Sinalização do ponto de risco e procedimento no POP",
            ],
            lo_pos=0.5, fe_pos=2.5, dph_pos=8, np_pos=2,
            normas_violadas=["NR-12 item 12.38", "ABNT NBR ISO 13849-1"],
        )
        p2 = Perigo(
            laudo_id=laudo.id, tipo="Ruído", fase_vida="Operação normal",
            descricao="Exposição a ruído contínuo acima do nível de ação",
            lo=10, fe=4, dph=6, np=4,
            justificativas={
                "lo": "Nível medido acima do limite de ação em toda a jornada",
                "fe": "Exposição constante durante o turno",
                "dph": "Risco de perda auditiva induzida por ruído",
                "np": "Equipe do setor (3 a 7 pessoas)",
            },
            medidas=[
                "M1 — Enclausuramento acústico da fonte",
                "M4 — Protetor auditivo enquanto a medida de projeto não é concluída",
            ],
            lo_pos=2, fe_pos=4, dph_pos=6, np_pos=4,
            normas_violadas=["NR-15 Anexo I", "NR-12 item 12.111"],
        )
        for p in (p1, p2):
            _set_hrn(p)
        db.add_all([p1, p2])
        db.flush()

        db.add(AcaoPlano(
            laudo_id=laudo.id, perigo_id=p1.id,
            acao="Instalar proteção fixa com intertravamento na prensa PH-200",
            prioridade="Alta", prazo=date.today().replace(month=min(12, date.today().month + 2)),
            responsavel="Manutenção industrial", classif_hrn=p1.classif_atual,
        ))
        db.commit()

        print("\n✔ Seed concluído.")
        print(f"   Cliente:  {cliente.nome} (id {cliente.id})")
        print(f"   Máquina:  {maquina.tipo} {maquina.modelo} (id {maquina.id})")
        print(f"   Laudo:    #{laudo.id} — {len([p1, p2])} perigos, 1 ação")
        print(f"   Perigo 1: HRN {p1.hrn_atual} ({p1.classif_atual}) → {p1.hrn_pos} ({p1.classif_pos})")
        print(f"   Perigo 2: HRN {p2.hrn_atual} ({p2.classif_atual}) → {p2.hrn_pos} ({p2.classif_pos})")
        print("\n   Suba o backend (uvicorn app.main:app --reload) e o frontend (npm run dev),")
        print("   abra http://localhost:5173 e clique em \"Abrir laudo existente\".")
    finally:
        db.close()


if __name__ == "__main__":
    main()
