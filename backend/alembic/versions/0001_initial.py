"""initial schema — Fase 1 (cliente, maquina, laudo, foto, perigo, acao_plano)

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-16
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cliente",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nome", sa.String(255), nullable=False),
        sa.Column("cnpj", sa.String(32)),
        sa.Column("endereco", sa.String(512)),
        sa.Column("contato", sa.String(255)),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "maquina",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("tipo", sa.String(255), nullable=False),
        sa.Column("fabricante", sa.String(255)),
        sa.Column("modelo", sa.String(255)),
        sa.Column("serie", sa.String(255)),
        sa.Column("ano", sa.String(16)),
        sa.Column("funcao", sa.String(512)),
        sa.Column("localizacao", sa.String(512)),
        sa.Column("anexo_nr12", sa.String(255)),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "laudo",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("cliente_id", sa.Integer, sa.ForeignKey("cliente.id"), nullable=False),
        sa.Column("maquina_id", sa.Integer, sa.ForeignKey("maquina.id"), nullable=False),
        sa.Column("variante", sa.String(16), nullable=False, server_default="enxuto"),
        sa.Column("status", sa.String(16), nullable=False, server_default="rascunho"),
        sa.Column("parecer", sa.String(16)),
        sa.Column("data_emissao", sa.Date),
        sa.Column("escala_fe", sa.String(512)),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("atualizado_em", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("docx_key", sa.String(512)),
    )

    op.create_table(
        "foto",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("laudo_id", sa.Integer,
                  sa.ForeignKey("laudo.id", ondelete="CASCADE"), nullable=False),
        sa.Column("storage_key", sa.String(512), nullable=False),
        sa.Column("legenda", sa.String(512)),
        sa.Column("ordem", sa.Integer, nullable=False, server_default="0"),
        sa.Column("ponto_risco", sa.String(512)),
    )
    op.create_index("ix_foto_laudo_id", "foto", ["laudo_id"])

    op.create_table(
        "perigo",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("laudo_id", sa.Integer,
                  sa.ForeignKey("laudo.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tipo", sa.String(255)),
        sa.Column("fase_vida", sa.String(255)),
        sa.Column("descricao", sa.String(1024)),
        sa.Column("lo", sa.Float, nullable=False),
        sa.Column("fe", sa.Float, nullable=False),
        sa.Column("dph", sa.Float, nullable=False),
        sa.Column("np", sa.Float, nullable=False),
        sa.Column("justificativas", postgresql.JSONB, server_default="{}"),
        sa.Column("hrn_atual", sa.Float, nullable=False, server_default="0"),
        sa.Column("classif_atual", sa.String(32)),
        sa.Column("medidas", postgresql.JSONB, server_default="[]"),
        sa.Column("lo_pos", sa.Float),
        sa.Column("fe_pos", sa.Float),
        sa.Column("dph_pos", sa.Float),
        sa.Column("np_pos", sa.Float),
        sa.Column("hrn_pos", sa.Float),
        sa.Column("classif_pos", sa.String(32)),
        sa.Column("normas_violadas", postgresql.JSONB, server_default="[]"),
        sa.Column("ordem", sa.Integer, nullable=False, server_default="0"),
    )
    op.create_index("ix_perigo_laudo_id", "perigo", ["laudo_id"])

    op.create_table(
        "acao_plano",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("laudo_id", sa.Integer,
                  sa.ForeignKey("laudo.id", ondelete="CASCADE"), nullable=False),
        sa.Column("perigo_id", sa.Integer,
                  sa.ForeignKey("perigo.id", ondelete="SET NULL")),
        sa.Column("acao", sa.String(1024), nullable=False),
        sa.Column("prioridade", sa.String(32)),
        sa.Column("prazo", sa.Date),
        sa.Column("responsavel", sa.String(255)),
        sa.Column("classif_hrn", sa.String(32)),
    )
    op.create_index("ix_acao_plano_laudo_id", "acao_plano", ["laudo_id"])


def downgrade() -> None:
    op.drop_table("acao_plano")
    op.drop_table("perigo")
    op.drop_table("foto")
    op.drop_table("laudo")
    op.drop_table("maquina")
    op.drop_table("cliente")
