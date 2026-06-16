# Plataforma de Laudos NR-12 — Celone Engenharia

Plataforma web para elaboração de **laudos de apreciação de riscos NR-12**. Automatiza
o trabalho repetitivo (identificação, registro fotográfico, cálculo e classificação do
HRN, formatação do DOCX) para que o engenheiro foque na análise crítica.

> **Fase 1 (MVP)** — um usuário, um laudo por vez, com três capacidades:
> **motor de cálculo HRN**, **galeria de fotos** e **geração de DOCX** no padrão Celone.
> Sem autenticação, biblioteca de seções, catálogo reutilizável avançado, funções de
> segurança/Categoria ou workflow multiusuário (fases futuras).

## Arquitetura

```
/backend      FastAPI + SQLAlchemy + Alembic + Pydantic (API e motor HRN)
/frontend     React + TypeScript + Vite (editor do laudo)
/generator    gerar_laudo.py — gerador de DOCX no padrão Celone (python-docx)
docker-compose.yml   PostgreSQL para desenvolvimento
```

- **Motor HRN** (`backend/app/services/hrn.py`) é a **fonte da verdade** do cálculo
  `HRN = LO × FE × DPH × NP` e da classificação por faixa. O frontend
  (`frontend/src/lib/hrn.ts`) espelha as tabelas só para recálculo em tempo real.
- **Storage** de fotos/DOCX fica atrás da interface `StorageBackend`
  (`backend/app/services/storage.py`). Nesta fase usa disco local; trocar por
  S3/R2/MinIO depois não toca no resto.
- **Regra de projeto inegociável:** `Perigo` **não tem campo de Categoria**. HRN é a
  estimativa quantitativa do risco; Categoria (NBR 14153 / PL ISO 13849-1) pertence a
  uma *função de segurança* — entidade separada de uma fase futura.

## Pré-requisitos

- Python 3.11+
- Node 18+
- Docker (para o PostgreSQL de desenvolvimento)

## 1. Banco de dados

```bash
docker compose up -d db
```

Sobe um PostgreSQL em `localhost:5432` (usuário/senha/db: `celone`).

## 2. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# aplica as migrações
alembic upgrade head

# sobe a API em http://localhost:8000 (docs em /docs)
uvicorn app.main:app --reload
```

Configuração opcional via `.env` (veja `backend/.env.example`). Variáveis usam o
prefixo `CELONE_` (ex.: `CELONE_DATABASE_URL`).

### Testes (lógica crítica do HRN)

```bash
cd backend
source .venv/bin/activate
pytest -q
```

## 3. Frontend

```bash
cd frontend
npm install
npm run dev    # http://localhost:5173
```

O Vite faz proxy de `/api` para o backend em `localhost:8000`.

## Fluxo de uso

1. Crie/abra um laudo escolhendo cliente e máquina.
2. **Registro fotográfico** — faça upload em lote, escreva legendas, marque o ponto de
   risco e reordene arrastando.
3. **Apreciação de riscos** — para cada perigo, escolha os fatores LO/FE/DPH/NP (antes e
   depois das medidas), justifique cada fator ("nunca suponha"), liste as medidas pela
   hierarquia ISO 12100. O HRN e a faixa são calculados em tempo real; o sistema alerta
   quando o risco não cai pelo menos uma faixa.
4. **Parecer** — defina status e o parecer de conformidade (decisão explícita do
   engenheiro, nunca derivada do HRN).
5. **Gerar DOCX** — baixa o `.docx` no padrão Celone (EB Garamond, cabeçalho em texto,
   medidas como tabela azul). O arquivo é arquivado junto ao laudo.

## Endpoints principais

| Método | Rota | Função |
|---|---|---|
| `GET` | `/meta/hrn` | tabelas de fatores, faixas e níveis ISO 12100 |
| `POST` | `/hrn/avaliar` | avaliação ad-hoc do HRN (preview) |
| `POST` | `/clientes`, `/maquinas`, `/laudos` | cadastros |
| `GET/POST` | `/laudos/{id}/perigos` | apreciação (HRN recalculado no servidor) |
| `POST` | `/laudos/{id}/fotos` | upload em lote |
| `PUT` | `/laudos/{id}/fotos/ordem` | reordenação |
| `POST` | `/laudos/{id}/docx` | gera e baixa o DOCX |

## Gerador de DOCX

`generator/gerar_laudo.py` é chamado pela API (`backend/app/services/docx_service.py`),
mas também roda como CLI:

```bash
python generator/gerar_laudo.py --in dados.json --out laudo.docx --variante enxuto
```

> O `gerar_laudo.py` original citado na arquitetura não estava no repositório; este
> gerador foi construído como equivalente em `python-docx`, seguindo o padrão Celone.
