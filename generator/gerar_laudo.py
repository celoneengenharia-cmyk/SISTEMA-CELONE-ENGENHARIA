#!/usr/bin/env python3
"""Gerador de DOCX de laudos NR-12 no padrão Celone Engenharia.

Equivalente ao `gerar_laudo.py` original referido na arquitetura (que não estava
presente no repositório). Reproduz o padrão Celone descrito no brief:

- fonte EB Garamond no corpo;
- cabeçalho em texto (não imagem) com as constantes da Celone;
- recomendações/medidas renderizadas como tabela azul.

Consome um JSON (stdin ou --in) e escreve um .docx (--out). Pode rodar como
script de linha de comando ou ser chamado por `docx_service.gerar()`.

Esquema de entrada (chaves principais):
    {
      "variante": "enxuto" | "detalhado",
      "empresa": {...constantes Celone...},
      "cliente": {"nome","cnpj","endereco","contato"},
      "maquina": {"tipo","fabricante","modelo","serie","ano","funcao",
                  "localizacao","anexo_nr12"},
      "laudo":   {"data_emissao","escala_fe","parecer","status"},
      "fotos":   [{"path","legenda","ponto_risco"}],
      "perigos": [{"tipo","fase_vida","descricao",
                   "fatores_antes","justificativas","hrn_atual","classif_atual",
                   "medidas","fatores_apos","hrn_pos","classif_pos",
                   "normas_violadas"}],
      "plano_acao": [{"acao","prioridade","prazo","responsavel","classif_hrn"}],
      "normas":   ["..."],
      "conclusao": "texto do parecer"
    }
`perigos` é aceito também sob a chave `avaliacoes` (compatibilidade).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

# Paleta Celone
AZUL = RGBColor(0x26, 0x41, 0x7A)
AZUL_SOFT = "E8EDF6"
CINZA = RGBColor(0x5C, 0x63, 0x6D)
FONTE = "EB Garamond"


# --------------------------------------------------------------------------
# Helpers de baixo nível (python-docx)
# --------------------------------------------------------------------------

def _set_base_font(doc: Document) -> None:
    style = doc.styles["Normal"]
    style.font.name = FONTE
    style.font.size = Pt(11)
    # garante a fonte também para east-asian/complex script runs
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        rfonts.set(qn(attr), FONTE)


def _shade_cell(cell, hex_fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.makeelement(qn("w:shd"), {qn("w:val"): "clear", qn("w:fill"): hex_fill})
    tc_pr.append(shd)


def _p(doc, text="", *, size=11, bold=False, italic=False, color=None,
       align=None, space_after=6):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        par.alignment = align
    if text:
        run = par.add_run(text)
        run.font.name = FONTE
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        if color is not None:
            run.font.color.rgb = color
    return par


def _heading(doc, num, title):
    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(12)
    par.paragraph_format.space_after = Pt(4)
    run = par.add_run(f"{num}. {title}" if num else title)
    run.font.name = FONTE
    run.font.size = Pt(13.5)
    run.bold = True
    run.font.color.rgb = AZUL
    return par


def _kv_table(doc, rows):
    """Tabela de duas colunas (rótulo / valor) para blocos de identificação."""
    visible = [(k, v) for k, v in rows if v]
    if not visible:
        return
    tbl = doc.add_table(rows=0, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    for k, v in visible:
        cells = tbl.add_row().cells
        rk = cells[0].paragraphs[0].add_run(k)
        rk.bold = True
        rk.font.name = FONTE
        rk.font.size = Pt(10.5)
        rv = cells[1].paragraphs[0].add_run(str(v))
        rv.font.name = FONTE
        rv.font.size = Pt(10.5)
    doc.add_paragraph()


# --------------------------------------------------------------------------
# Seções do laudo
# --------------------------------------------------------------------------

def _cabecalho(doc, data):
    """Cabeçalho em texto (padrão Celone), não imagem."""
    emp = data.get("empresa", {})
    title = _p(doc, emp.get("empresa", "Celone Engenharia LTDA"),
               size=18, bold=True, color=AZUL, align=WD_ALIGN_PARAGRAPH.CENTER,
               space_after=2)
    linha = " · ".join(
        x for x in [
            f"CNPJ {emp.get('cnpj')}" if emp.get("cnpj") else None,
            emp.get("site"),
            emp.get("telefone"),
        ] if x
    )
    _p(doc, linha, size=10, color=CINZA, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    resp = " · ".join(
        x for x in [
            f"Resp. Técnico: {emp.get('engenheiro')}" if emp.get("engenheiro") else None,
            f"CREA {emp.get('crea')}" if emp.get("crea") else None,
        ] if x
    )
    _p(doc, resp, size=10, color=CINZA, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    _p(doc, "LAUDO DE APRECIAÇÃO DE RISCOS — NR-12",
       size=15, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    variante = (data.get("variante") or "enxuto").capitalize()
    _p(doc, f"Variante: {variante}", size=10, color=CINZA,
       align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)


def _identificacao(doc, data):
    _heading(doc, 1, "Identificação")
    cli = data.get("cliente", {})
    maq = data.get("maquina", {})
    laudo = data.get("laudo", {})
    _p(doc, "Cliente", size=11.5, bold=True, color=AZUL, space_after=2)
    _kv_table(doc, [
        ("Nome", cli.get("nome")),
        ("CNPJ", cli.get("cnpj")),
        ("Endereço", cli.get("endereco")),
        ("Contato", cli.get("contato")),
    ])
    _p(doc, "Máquina / Equipamento", size=11.5, bold=True, color=AZUL, space_after=2)
    _kv_table(doc, [
        ("Tipo", maq.get("tipo")),
        ("Fabricante", maq.get("fabricante")),
        ("Modelo", maq.get("modelo")),
        ("Série", maq.get("serie")),
        ("Ano", maq.get("ano")),
        ("Função", maq.get("funcao")),
        ("Localização", maq.get("localizacao")),
        ("Anexo NR-12 aplicável", maq.get("anexo_nr12")),
    ])
    _kv_table(doc, [
        ("Data de emissão", laudo.get("data_emissao")),
        ("Escala de FE adotada", laudo.get("escala_fe")),
    ])


def _metodologia(doc, data):
    _heading(doc, 2, "Metodologia")
    escala = data.get("laudo", {}).get("escala_fe")
    _p(doc,
       "A apreciação de riscos segue a NR-12 e a ABNT NBR ISO 12100. A estimativa "
       "quantitativa do risco por perigo usa o método HRN (Hazard Rating Number), "
       "HRN = LO × FE × DPH × NP, com fatores da escala ABNT NBR ISO/TR 14121-2. "
       "As medidas de redução seguem a hierarquia da ISO 12100 (projeto "
       "intrinsecamente seguro → proteção/dispositivo → informação para uso → EPI), "
       "e o risco residual é reavaliado após as medidas.")
    if escala:
        _p(doc, f"Escala de frequência de exposição (FE) adotada: {escala}.")


def _registro_fotografico(doc, data):
    fotos = data.get("fotos") or []
    _heading(doc, 3, "Registro fotográfico")
    if not fotos:
        _p(doc, "Sem registro fotográfico anexado.", italic=True, color=CINZA)
        return
    from docx.shared import Inches
    for i, f in enumerate(fotos, 1):
        path = f.get("path")
        if path and Path(path).exists():
            try:
                doc.add_picture(path, width=Inches(4.5))
                doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            except Exception:  # imagem corrompida não derruba o laudo
                _p(doc, f"[imagem indisponível: {path}]", italic=True, color=CINZA)
        legenda = f.get("legenda") or ""
        ponto = f.get("ponto_risco")
        texto = f"Figura {i} — {legenda}".rstrip(" —")
        if ponto:
            texto += f" (ponto de risco: {ponto})"
        _p(doc, texto, size=10, italic=True, color=CINZA,
           align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)


def _norm_perigo(p):
    """Normaliza um perigo dos dois formatos aceitos (frontend ou API)."""
    fa = p.get("fatores_antes") or {
        "LO": p.get("lo"), "FE": p.get("fe"), "DPH": p.get("dph"), "NP": p.get("np")
    }
    fp = p.get("fatores_apos") or {
        "LO": p.get("lo_pos"), "FE": p.get("fe_pos"),
        "DPH": p.get("dph_pos"), "NP": p.get("np_pos")
    }
    return fa, fp


def _apreciacao(doc, data):
    perigos = data.get("perigos") or data.get("avaliacoes") or []
    _heading(doc, 4, "Apreciação de riscos")
    if not perigos:
        _p(doc, "Nenhum perigo registrado.", italic=True, color=CINZA)
        return
    for i, p in enumerate(perigos, 1):
        fa, fp = _norm_perigo(p)
        titulo = p.get("descricao") or p.get("tipo") or f"Perigo {i}"
        _p(doc, f"4.{i}  {titulo}", size=11.5, bold=True, color=AZUL, space_after=2)
        meta = " · ".join(x for x in [p.get("tipo"), p.get("fase_vida")] if x)
        if meta:
            _p(doc, meta, size=10, color=CINZA, space_after=4)

        def fmt(f):
            return f"LO {f.get('LO')} × FE {f.get('FE')} × DPH {f.get('DPH')} × NP {f.get('NP')}"

        _p(doc, f"HRN antes: {p.get('hrn_atual')} — {p.get('classif_atual')}  "
                f"({fmt(fa)})", size=10.5, space_after=2)

        just = p.get("justificativas") or {}
        if just:
            partes = [f"{k.upper()}: {v}" for k, v in just.items() if v]
            if partes:
                _p(doc, "Justificativa dos fatores — " + "; ".join(partes),
                   size=10, color=CINZA, space_after=4)

        medidas = p.get("medidas") or []
        if medidas:
            _tabela_medidas(doc, medidas)

        if p.get("hrn_pos") is not None:
            _p(doc, f"HRN após medidas: {p.get('hrn_pos')} — {p.get('classif_pos')}  "
                    f"({fmt(fp)})", size=10.5, bold=True, space_after=2)

        normas = p.get("normas_violadas") or []
        if normas:
            _p(doc, "Normas aplicáveis/violadas: " + "; ".join(normas),
               size=10, color=CINZA, space_after=8)
        doc.add_paragraph()


def _tabela_medidas(doc, medidas):
    """Recomendações/medidas como tabela azul (padrão Celone)."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    hdr = tbl.rows[0].cells[0]
    _shade_cell(hdr, "26417A")
    hr = hdr.paragraphs[0].add_run("Medidas de redução — hierarquia ISO 12100")
    hr.bold = True
    hr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    hr.font.name = FONTE
    hr.font.size = Pt(10.5)
    for m in medidas:
        cell = tbl.add_row().cells[0]
        _shade_cell(cell, AZUL_SOFT)
        run = cell.paragraphs[0].add_run(str(m))
        run.font.name = FONTE
        run.font.size = Pt(10.5)
    doc.add_paragraph()


def _plano_acao(doc, data):
    plano = data.get("plano_acao") or []
    if not plano:
        return
    _heading(doc, 5, "Plano de ação")
    tbl = doc.add_table(rows=1, cols=5)
    tbl.style = "Table Grid"
    headers = ["Ação", "Prioridade", "Prazo", "Responsável", "Classif. HRN"]
    for c, h in zip(tbl.rows[0].cells, headers):
        _shade_cell(c, "26417A")
        r = c.paragraphs[0].add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.name = FONTE
        r.font.size = Pt(10)
    for a in plano:
        cells = tbl.add_row().cells
        vals = [a.get("acao"), a.get("prioridade"), a.get("prazo"),
                a.get("responsavel"), a.get("classif_hrn")]
        for cell, v in zip(cells, vals):
            run = cell.paragraphs[0].add_run("" if v is None else str(v))
            run.font.name = FONTE
            run.font.size = Pt(10)
    doc.add_paragraph()


def _normas(doc, data):
    normas = data.get("normas") or []
    if not normas:
        return
    _heading(doc, 6, "Normas aplicáveis")
    for n in normas:
        par = doc.add_paragraph(style="List Bullet")
        run = par.add_run(str(n))
        run.font.name = FONTE
        run.font.size = Pt(10.5)


def _conclusao(doc, data):
    _heading(doc, 7, "Parecer e responsabilidade técnica")
    parecer = data.get("laudo", {}).get("parecer")
    if parecer:
        rotulo = {
            "conforme": "CONFORME",
            "com_ressalvas": "CONFORME COM RESSALVAS",
            "nao_conforme": "NÃO CONFORME",
        }.get(parecer, parecer)
        _p(doc, f"Parecer de conformidade: {rotulo}", bold=True, color=AZUL)
    conclusao = data.get("conclusao")
    if conclusao:
        _p(doc, conclusao)
    emp = data.get("empresa", {})
    doc.add_paragraph()
    _p(doc, "_" * 40, space_after=2)
    _p(doc, emp.get("engenheiro", ""), bold=True, space_after=0)
    _p(doc, f"Engenheiro responsável — CREA {emp.get('crea','')}",
       size=10, color=CINZA, space_after=0)
    _p(doc, emp.get("empresa", ""), size=10, color=CINZA)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def gerar_documento(data: dict) -> Document:
    doc = Document()
    _set_base_font(doc)
    _cabecalho(doc, data)
    _identificacao(doc, data)
    _metodologia(doc, data)
    _registro_fotografico(doc, data)
    _apreciacao(doc, data)
    _plano_acao(doc, data)
    _normas(doc, data)
    _conclusao(doc, data)
    return doc


def gerar_arquivo(data: dict, out_path: str | Path) -> Path:
    doc = gerar_documento(data)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gera o DOCX do laudo NR-12 (padrão Celone).")
    ap.add_argument("--in", dest="infile", help="JSON de entrada (default: stdin)")
    ap.add_argument("--out", dest="outfile", required=True, help="caminho do .docx de saída")
    ap.add_argument("--variante", choices=["enxuto", "detalhado"], help="sobrescreve a variante")
    args = ap.parse_args(argv)

    raw = Path(args.infile).read_text(encoding="utf-8") if args.infile else sys.stdin.read()
    data = json.loads(raw)
    if args.variante:
        data["variante"] = args.variante
    out = gerar_arquivo(data, args.outfile)
    print(str(out))


if __name__ == "__main__":
    main()
