#!/usr/bin/env python3
"""Gera as landing pages de serviço da Celone a partir de um modelo único.

Uso: python3 gerar.py   -> grava <pasta>/index.html para cada página.
Os textos vêm do "Briefing do novo site Celone" (19/11/2026). Para mudar o
layout, edite _base/estilo.css; para mudar textos, edite PAGINAS abaixo.
"""
import html
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
ZAP = "https://wa.me/5518991137803"
CSS = open(os.path.join(AQUI, "_base", "estilo.css"), encoding="utf-8").read()
ICONE = open(os.path.join(AQUI, "_base", "icone-whatsapp.svg"), encoding="utf-8").read()

# Lista geral de clientes (briefing, "Provas"), na ordem do briefing.
CLIENTES_GERAL = [
    "Ambev", "Três Corações", "ArcelorMittal Pecém", "Aunde", "Acotubo", "AXIA Energia",
    "BBTS", "CCCC", "Ecovias", "EPAV", "Gree", "J&T Express", "LAFEPE", "Karne Keijo",
    "PROK Brasil", "Sesc", "Supernosso", "UTC Óleo e Gás", "Enaex", "CREMESP",
    "Prefeitura de Pinhais", "Prefeitura de Mossoró",
]

MENU = [
    ("/projeto-exaustao-climatizacao/", "Exaustão e HVAC"),
    ("/laudo-nr12/", "NR-12"),
    ("/linha-de-vida-nr35/", "NR-35"),
    ("/laudo-tecnico-com-art/", "Laudo com ART"),
    ("/clientes-e-projetos/", "Clientes"),
    ("/#sobre", "Sobre"),
]

e = html.escape

PAGINAS = [
    # ------------------------------------------------------------------ HVAC
    dict(
        pasta="projeto-exaustao-climatizacao",
        codigo="HVAC",
        assunto="projeto de exaustão ou climatização",
        seo_titulo="Projeto de Exaustão e Climatização com ART | Celone Engenharia",
        seo_desc="Projeto de exaustão de cozinha, ventilação e climatização (HVAC) com memorial de cálculo, desenhos e ART. Atendimento em todo o Brasil.",
        servicos=["Projeto de exaustão de cozinha", "Projeto de ventilação e antecâmara", "Projeto de climatização e HVAC", "Projeto de redes de vapor e ar comprimido"],
        rotulo="Projetos mecânicos",
        titulo='Projeto de exaustão e <em class="g">climatização</em>',
        sub="Da coifa da cozinha à planta farmacêutica. Calculamos, desenhamos e assinamos o projeto que a vigilância sanitária, os bombeiros e o seu instalador vão usar. <strong>Atendemos todo o Brasil.</strong>",
        btn="Pedir proposta do projeto",
        nota="Escopo, valor e prazo no mesmo dia, pelo WhatsApp. Não vendemos nem instalamos equipamentos: fazemos o projeto e a ART.",
        faixa=[("Responsável técnico", "Eng. Matteo Celone · CREA 2118861648"), ("Entrega", "Memorial, desenhos e ART"), ("Atendimento", "Todo o Brasil, desde 2019")],
        prova_rotulo="Projetos de HVAC para",
        destaque=["LAFEPE", "Karne Keijo", "N1MED", "LD Diagnósticos", "AABB Natal", "Sesc"],
        alerta=None,
        quando_titulo='Quando você precisa do <em class="g">projeto de exaustão</em>',
        quando=[
            ("Vigilância sanitária", "Pediu o projeto de exaustão da cozinha ou a ventilação do laboratório."),
            ("Bombeiros", "O projeto de incêndio exige exaustão ou ventilação de antecâmara."),
            ("Obra ou reforma", "A climatização precisa ser compatibilizada com arquitetura e elétrica."),
            ("Calor, fumo e cheiro", "O ambiente esquenta, junta fumo, gordura ou cheiro — inclusive com o vizinho reclamando."),
            ("Escritórios e construtoras", "Você quer terceirizar a disciplina de HVAC com quem assina."),
        ],
        fazemos_titulo='Exaustão, ventilação e <em class="g">climatização</em> com ART',
        blocos=[
            ("Exaustão de cozinha", None, "Coifa dimensionada por equipamento de cocção, dutos, exaustor, filtro e caixa de ventilação, conforme a NBR 14518.", ["Restaurantes, hamburguerias e refeitórios", "Filtro eletrostático para cheiro e gordura", "Ar de reposição"]),
            ("Ventilação e antecâmara", None, "Vazões, renovação de ar e exaustão mecânica por ramal.", ["Antecâmara do projeto de incêndio", "Laboratórios, sanitários e DML", "Casa de máquinas e exaustão de solda"]),
            ("Climatização e HVAC", None, "Carga térmica por ambiente, escolha da tecnologia, dutos, tubulações e drenos.", ["Split, cassete, VRF e água gelada", "Renovação e qualidade do ar (NBR 16401)", "Gradiente de pressão entre salas"]),
            ("Vapor e ar comprimido", None, "Redes de utilidades projetadas junto do HVAC, compatibilizadas no entreforro.", ["Troncais, ramais e pontos por sala", "Ar em contato com o produto (ISO 8573-1)", "Interface com a NR-13"]),
        ],
        recebe_titulo='O que vem no <em class="g">projeto de exaustão e climatização</em>',
        recebe=[
            ("Memorial de cálculo", "Vazões, carga térmica, perdas de carga e dimensionamento", "PDF assinado", False),
            ("Memorial descritivo", "Especificação do sistema e dos equipamentos", "PDF · DOCX", False),
            ("Desenhos", "Planta, cortes, isométricos e detalhes", "PDF · DWG · Revit", False),
            ("Lista de materiais", "Para o seu instalador cotar", "PDF · XLSX", False),
            ("ART", "Anotação de responsabilidade técnica recolhida no CREA", "PDF", False),
            ("Acompanhamento", "Quando há protocolo em órgão, acompanhamos até a aprovação", "—", False),
        ],
        como_titulo='Como funciona o <em class="g">projeto de climatização</em>',
        como_lead="Você não precisa esperar visita: o levantamento pode ser por vídeo, com as medidas guiadas pela nossa equipe.",
        passos=[
            ("Você manda o que tem", "Planta ou croqui, fotos, lista de equipamentos e quem está exigindo o projeto."),
            ("Respondemos com escopo, valor e prazo", "Em geral no mesmo dia, pelo WhatsApp."),
            ("Levantamento por visita ou vídeo", "Na vistoria assistida, orientamos por vídeo o que fotografar e medir. O projeto e a ART são os mesmos."),
            ("Entrega com ART", "E acompanhamento até a aprovação na vigilância ou nos bombeiros."),
        ],
        nao_fazemos="Não vendemos nem instalamos equipamentos. Fazemos o projeto e a ART; o seu instalador executa com as medidas certas. Se precisar, indicamos um parceiro.",
        numeros=[("300+", "clientes atendidos"), ("15", "estados"), ("5.450 m²", "de centro de distribuição em um só projeto"), ("2019", "desde, com ART em todo trabalho")],
        casos=[
            ("Recife/PE", "LAFEPE", "HVAC e utilidades de planta farmacêutica", "Unidades de tratamento de ar, água gelada, gradiente de pressão entre salas, vapor e ar comprimido."),
            ("5.450 m²", "Karne Keijo · Parnamirim/RN", "Centro de distribuição climatizado", "Climatização, renovação de ar, exaustão da cozinha coifa por coifa e GLP."),
            ("Rio/RJ", "N1MED · Copacabana", "Hamburgueria com cheiro na vizinhança", "Coifa, duto até a cobertura, exaustor e filtro eletrostático."),
        ],
        tambem="LD Diagnósticos — ventilação de laboratório, Foz do Iguaçu/PR · AABB Natal — climatização.",
        avaliacoes=[("Matheus Gabriel Souza", "Projetos de engenharia"), ("Pedro Micali", "Projetos"), (None, "Projeto de exaustão ou HVAC")],
        faq_titulo='Dúvidas sobre o <em class="g">projeto de exaustão</em>',
        faq=[
            ("Vocês atendem a minha cidade?", "Sim. Atendemos todo o Brasil — já são clientes em 15 estados. O levantamento pode ser presencial ou por vistoria assistida por vídeo, e o projeto e a ART são os mesmos."),
            ("O projeto serve para a vigilância sanitária e para os bombeiros?", "Sim. O projeto sai com memorial de cálculo, desenhos e ART, conforme a NBR 14518 (exaustão de cozinha) e a NBR 16401 (climatização e renovação de ar). Quando há protocolo em órgão, acompanhamos até a aprovação."),
            ("Vocês vendem ou instalam equipamentos?", "Não. Fazemos o projeto e a ART; o seu instalador executa com as medidas certas, usando a lista de materiais do projeto. Se precisar, indicamos um parceiro."),
            ("Em quanto tempo fica pronto?", "Depende do tamanho e do número de ambientes. O prazo vem junto com o valor na proposta, em geral no mesmo dia do contato."),
            ("O que preciso mandar para o orçamento?", "Planta ou croqui, fotos do local, a lista de equipamentos (de cocção, de laboratório ou de produção) e quem está exigindo o projeto."),
            ("Vocês atendem escritórios de engenharia e construtoras?", "Sim. Assumimos a disciplina de HVAC com ART e entregamos em DWG, PDF e Revit, compatibilizado com arquitetura e elétrica."),
        ],
        fechamento='Mande a planta e diga quem está pedindo o projeto. <em class="g">Respondemos com escopo, valor e prazo.</em>',
    ),
    # ------------------------------------------------------------------ NR-35
    dict(
        pasta="linha-de-vida-nr35",
        codigo="NR35",
        assunto="linha de vida ou escadas NR-35",
        seo_titulo="Projeto e Laudo de Linha de Vida NR-35 com ART | Celone Engenharia",
        seo_desc="Projeto e laudo de linha de vida, ancoragem e escada marinheiro conforme a NR-35, com memorial de cálculo e ART. Todo o Brasil.",
        servicos=["Projeto de linha de vida", "Laudo de linha de vida", "Projeto e inspeção de ancoragem", "Laudo de escada marinheiro"],
        rotulo="NR-35 · Trabalho em altura",
        titulo='Projeto e laudo de <em class="g">linha de vida</em> e escadas fixas',
        sub="A linha de vida só protege se a estrutura onde ela está presa aguenta uma queda. O memorial de cálculo comprova isso, e a ART garante. <strong>Atendemos todo o Brasil.</strong>",
        btn="Pedir valor da linha de vida",
        nota="Valor e prazo no mesmo dia, pelo WhatsApp. Não vendemos nem instalamos linha de vida: fazemos o projeto, o laudo e a ART.",
        faixa=[("Responsável técnico", "Eng. Matteo Celone · CREA 2118861648"), ("Entrega", "Memorial de cálculo, desenhos e ART"), ("Atendimento", "Todo o Brasil, desde 2019")],
        prova_rotulo="Linha de vida e escadas para",
        destaque=["Enaex (Mina Borborema)", "KSS Motos", "Galvão Tayrones"],
        # CONFIRMAR com o Matteo o número e a data da portaria antes de publicar.
        alerta='A NR-35 mudou em julho de 2026 e as escadas fixas passaram a exigir análise antes do uso. <b>Sua escada marinheiro está documentada?</b>',
        quando_titulo='Quando você precisa do <em class="g">laudo de linha de vida</em>',
        quando=[
            ("Auditoria ou cliente", "A fiscalização, a auditoria ou o seu cliente pediu o projeto ou o laudo da linha de vida."),
            ("Linha sem documento", "A linha foi instalada sem projeto, ou ninguém sabe se a estrutura aguenta."),
            ("Escada marinheiro", "Há escadas fixas sem linha de vida vertical ou sem laudo."),
            ("Serviço em altura", "Vai começar um serviço em telhado, galpão ou carga e descarga de caminhão e falta a ancoragem."),
        ],
        fazemos_titulo='Linha de vida, ancoragem e <em class="g">escada marinheiro</em>',
        blocos=[
            ("Projeto de linha de vida", None, "Horizontal ou vertical, fixa ou temporária, dimensionada junto com a estrutura que vai segurá-la.", ["Memorial de cálculo e desenhos", "Especificação dos componentes", "ART"]),
            ("Laudo de linha de vida existente", None, "Inspeção da linha já instalada, com parecer sobre a linha e a estrutura.", ["Relatório fotográfico", "Parecer técnico e ART", "Data da próxima inspeção"]),
            ("Ancoragem", None, "Projeto ou inspeção de pontos de ancoragem, inclusive em prédios e fachadas.", ["Telhados e galpões", "Caminhões e carga e descarga", "Ancoragem predial"]),
            ("Escadas fixas", None, "Inspeção e laudo de cada escada, com gaiola, degraus e ancoragem avaliados.", ["Escada marinheiro conforme a nova NR-35", "Linha de vida vertical quando precisar", "Pacote para várias escadas"]),
        ],
        recebe_titulo='O que vem no <em class="g">projeto e laudo NR-35</em>',
        recebe=[
            ("Memorial de cálculo", "Da linha de vida e da estrutura onde ela é fixada", "PDF assinado", False),
            ("Desenhos e especificação", "Componentes e detalhes para o instalador", "PDF · DWG", False),
            ("Laudo", "Inspeção com registro fotográfico, parecer e data da próxima inspeção", "PDF", False),
            ("ART", "Anotação de responsabilidade técnica recolhida no CREA", "PDF", False),
        ],
        como_titulo='Como funciona o <em class="g">projeto de linha de vida</em>',
        como_lead="Na maioria dos casos, não precisa de visita: a vistoria assistida tem fotos e medidas guiadas pela nossa equipe.",
        passos=[
            ("Você diz onde é", "Telhado, galpão, caminhão ou fachada; o comprimento ou quantas escadas são; e o que motivou o pedido."),
            ("Mandamos valor e prazo no mesmo dia", "Proposta pelo WhatsApp, com pacote quando são várias escadas."),
            ("Vistoria presencial ou assistida", "Orientamos por vídeo o que fotografar e medir. O laudo e a ART são os mesmos."),
            ("Entregamos projeto ou laudo com ART", "Pronto para a fiscalização e para o instalador."),
        ],
        nao_fazemos="Não vendemos nem instalamos linha de vida, cabo, trava-quedas ou EPI. Projetamos e inspecionamos; se precisar, indicamos um instalador.",
        numeros=[("300+", "clientes atendidos"), ("15", "estados"), ("10", "escadas em um só pacote, em Manaus"), ("2019", "desde, com ART em todo trabalho")],
        casos=[
            ("3 normas", "Mina Borborema · Enaex", "NR-35 junto com NR-12 e NR-13", "Trabalho em altura junto com NR-12 e NR-13 de caminhões e compressores, no mesmo trabalho."),
            ("6 escadas", "KSS Motos", "Laudo de escadas fixas em pacote", "Seis escadas no mesmo local, inspecionadas e laudadas de uma vez."),
            ("Temporária", "Galvão Tayrones", "Projeto de linha de vida temporária", "Projeto de linha de vida temporária com memorial de cálculo e ART."),
        ],
        tambem="10 escadas em Manaus/AM, em pacote.",
        avaliacoes=[(None, "Linha de vida NR-35"), (None, "Laudo de escada marinheiro"), (None, "Serviço")],
        faq_titulo='Dúvidas sobre <em class="g">linha de vida e escadas</em>',
        faq=[
            ("Vocês instalam a linha de vida?", "Não. Fazemos o projeto, o laudo e a ART; a instalação fica com o seu instalador. Se precisar, indicamos um."),
            ("Minha escada antiga precisa se adequar?", "Depende da escada e do uso. O laudo diz o que se aplica a ela e em que prazo."),
            ("Vocês atendem a minha cidade?", "Sim. Atendemos todo o Brasil — já são clientes em 15 estados — com vistoria presencial ou assistida por vídeo."),
            ("O laudo tem validade?", "A linha de vida precisa de inspeção periódica. O laudo indica a data da próxima."),
            ("O que preciso mandar?", "Onde fica, o comprimento da linha ou o número de escadas, a altura aproximada e fotos."),
        ],
        fechamento='Diga onde fica a linha ou quantas escadas são e a altura. <em class="g">Mandamos valor e prazo no mesmo dia.</em>',
    ),
    # ------------------------------------------------------------ LAUDO ART
    dict(
        pasta="laudo-tecnico-com-art",
        codigo="ART",
        assunto="laudo com ART",
        seo_titulo="Laudo Técnico com ART e Responsável Técnico CREA | Celone Engenharia",
        seo_desc="Laudo de engenheiro mecânico com ART para licitação, banco, seguradora e concessionária, e responsável técnico no CREA. Preço fechado no WhatsApp.",
        servicos=["Laudo técnico com ART", "Laudo de queima de equipamento", "Responsável técnico no CREA"],
        rotulo="Laudos técnicos · Engenharia mecânica",
        titulo='Laudo técnico com ART <em class="g">para quem tem prazo</em>',
        sub="Licitação, seguradora, banco, concessionária ou CREA pediu? Engenheiro mecânico com CREA, preço fechado antes de começar e laudo em poucos dias. <strong>Atendemos todo o Brasil.</strong>",
        btn="Pedir preço do laudo",
        nota="Preço fechado e prazo no mesmo dia, pelo WhatsApp. Pagamento por PIX ou boleto.",
        faixa=[("Responsável técnico", "Eng. Matteo Celone · CREA 2118861648"), ("Preço", "Fechado no WhatsApp, antes de começar"), ("Pagamento", "PIX ou boleto")],
        prova_rotulo="Laudos com ART para",
        destaque=["Mundial Telhas Térmicas", "BBTS (Grupo Banco do Brasil)", "WHS"],
        alerta=None,
        quando_titulo=None,  # esta página pula "Quando você precisa" (briefing)
        quando=[],
        fazemos_titulo='Laudo com ART, queima de equipamento e <em class="g">responsável técnico</em>',
        blocos=[
            ("Laudo técnico com ART", "Para empresa que precisa comprovar segurança ou resistência", "De máquina, equipamento, estrutura metálica ou produto — para licitação, banco ou seguradora.", ["Análise técnica", "Registro fotográfico e parecer", "ART"]),
            ("Laudo de queima de equipamento", "Para quem vai pedir ressarcimento à concessionária", "Laudo de danos elétricos com o nexo técnico do dano, para o pedido de ressarcimento.", ["Motor, compressor ou máquina", "Nexo técnico do dano", "ART"]),
            ("Responsável técnico no CREA", "Para empresa notificada ou sem RT", "Montagem, manutenção, climatização ou fabricação: resolva a notificação do CREA com engenheiro mecânico como RT.", ["Contrato anual com valor fixo", "ART de cargo e função", "Requerimento no CREA"]),
        ],
        recebe_titulo='O que você recebe no <em class="g">laudo com ART</em>',
        recebe=[
            ("Laudo técnico", "Análise, registro fotográfico e parecer assinado por engenheiro mecânico", "PDF assinado", False),
            ("Laudo de queima", "Nexo técnico do dano elétrico para a concessionária", "PDF assinado", False),
            ("ART", "Anotação de responsabilidade técnica recolhida no CREA", "PDF", False),
            ("Responsável técnico", "Contrato anual, ART de cargo e função e requerimento no CREA", "Contrato · PDF", False),
        ],
        como_titulo='Como funciona o <em class="g">laudo técnico com ART</em>',
        como_lead="Com prazo de licitação, diga a data já na primeira mensagem.",
        passos=[
            ("Diga o que precisa e quem exige", "Licitação, banco, seguradora, concessionária ou CREA."),
            ("Mandamos valor e prazo no mesmo dia", "Preço fechado antes de começar."),
            ("Vistoria assistida por vídeo ou visita", "Na maioria dos casos, não precisa de visita presencial."),
            ("Laudo com ART entregue", "Em geral em poucos dias. Pagamento por PIX ou boleto."),
        ],
        nao_fazemos="Não vendemos, consertamos nem instalamos equipamentos. Avaliamos, emitimos o laudo e assinamos a ART.",
        numeros=[("300+", "clientes atendidos"), ("15", "estados"), ("3 dias", "do pedido ao laudo entregue e pago, para licitação"), ("2019", "desde, com ART em todo trabalho")],
        casos=[
            ("3 dias", "Mundial Telhas Térmicas", "Laudo de resistência mecânica para licitação", "Laudo para licitação entregue e pago em 3 dias."),
            ("38 modelos", "BBTS · Grupo Banco do Brasil", "Laudo técnico de equipamentos", "Laudo técnico de 38 modelos de equipamentos."),
            ("CREA-GO", "WHS", "Responsável técnico com contrato anual", "Eng. Matteo como RT da empresa no CREA de Goiás."),
        ],
        tambem=None,
        avaliacoes=[("Manoela Barbosa", "Laudo de estrutura metálica"), ("Carlos Magno", "Laudo de caminhão munck"), (None, "Laudo com ART")],
        faq_titulo='Dúvidas sobre o <em class="g">laudo com ART</em>',
        faq=[
            ("Em quanto tempo sai o laudo?", "Em poucos dias após a vistoria. Se houver prazo de licitação, diga a data na primeira mensagem."),
            ("O laudo é aceito pelo órgão?", "Sim: o laudo tem ART recolhida e a assinatura de engenheiro mecânico com CREA."),
            ("Preciso de visita presencial?", "Na maioria dos casos, não. Fazemos a vistoria assistida por vídeo."),
            ("Vocês atendem a minha cidade?", "Sim. Atendemos todo o Brasil — já são clientes em 15 estados."),
            ("Como pago?", "Por PIX ou boleto, com o preço fechado antes de começar."),
        ],
        fechamento='Diga o que precisa e quem está exigindo. <em class="g">Respondemos com valor e prazo no mesmo dia.</em>',
    ),
]


def btn(texto):
    return f'<a class="btn js-zap" href="{ZAP}"><svg><use href="#wa"/></svg>{texto}</a>'


def nomes(lista):
    return ' <i>·</i> '.join(e(n) for n in lista)


def gerar(p):
    secao = 0

    def rot(nome):
        nonlocal secao
        secao += 1
        return f'<span class="label">{secao} · {nome}</span>'

    destaque_base = {n.split(" (")[0] for n in p["destaque"]}
    outros = [c for c in CLIENTES_GERAL if c not in destaque_base]
    menu = "\n      ".join(
        f'<a href="{u}"{" aria-current=\"page\"" if u.strip("/") == p["pasta"] else ""}>{t}</a>' for u, t in MENU)

    ld = {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": "Celone Engenharia LTDA", "taxID": "55.514.523/0001-48",
        "url": f"https://celoneengenharia.com/{p['pasta']}/",
        "telephone": "+55 18 99113-7803", "email": "celoneengenharia@gmail.com", "areaServed": "BR",
        "address": {"@type": "PostalAddress", "streetAddress": "Av. Engenheiro Roberto Freire, 1962, Capim Macio",
                    "addressLocality": "Natal", "addressRegion": "RN", "postalCode": "59082-095", "addressCountry": "BR"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": p["rotulo"], "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s}} for s in p["servicos"]]},
    }

    o = []
    w = o.append
    w(f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["seo_titulo"])}</title>
<meta name="description" content="{e(p["seo_desc"])}">
<link rel="canonical" href="https://celoneengenharia.com/{p["pasta"]}/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400&family=Manrope:wght@400;600&family=Space+Grotesk:wght@300;400&display=swap" rel="stylesheet">
<!-- Gerado por landing-pages/gerar.py. Imagens: trocar os gradientes de .hero, .ph e .close por WebP (topo 16:9 / 4:5, serviços 3:2, fechamento 21:9), até 200 KB. -->
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<style>
{CSS}</style>
</head>
<body>
{ICONE}
<header class="top">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Celone Engenharia — início"><b>C</b>CELONE ENGENHARIA</a>
    <nav class="menu" aria-label="Serviços">
      {menu}
    </nav>
    <a class="nav-cta js-zap" href="{ZAP}">Falar com o engenheiro</a>
  </div>
</header>

<main>
<section class="hero">
  <div class="wrap">
    <span class="label">{e(p["rotulo"])}</span>
    <h1>{p["titulo"]}</h1>
    <p class="lead">{p["sub"]}</p>
    <div class="cta-row">
      {btn(p["btn"])}
      <p class="note">{e(p["nota"])}</p>
    </div>
    <div class="facts">
      {"".join(f'<div><span>{e(k)}</span><p>{e(v)}</p></div>' for k, v in p["faixa"])}
    </div>
  </div>
</section>

<!-- Prova acima da dobra: clientes deste serviço logo após o topo -->
<div class="proofbar">
  <div class="wrap">
    <span class="label">{e(p["prova_rotulo"])}</span>
    <p class="names">{nomes(p["destaque"])} <i>·</i> <span style="color:var(--muted)">e mais de 300 clientes em 15 estados</span></p>
  </div>
</div>
''')
    if p["alerta"]:
        w(f'''
<!-- CONFIRMAR número e data da portaria antes de publicar -->
<div class="alerta"><div class="wrap"><p>{p["alerta"]}</p></div></div>
''')

    if p["quando"]:
        linhas = "\n      ".join(f'<div><span class="k">{e(k)}</span><p class="v">{e(v)}</p></div>' for k, v in p["quando"])
        w(f'''
<section>
  <div class="wrap">
    {rot("Quando você precisa")}
    <h2>{p["quando_titulo"]}</h2>
    <div class="rows">
      {linhas}
    </div>
  </div>
</section>
''')

    blocos = []
    for titulo, para, texto, itens in p["blocos"]:
        li = "".join(f"<li>{e(i)}</li>" for i in itens)
        para_html = f'<p class="para">{e(para)}</p>' if para else ""
        blocos.append(f'''      <div class="block">
        <div class="ph" role="img" aria-label=""></div>
        <div>
          {para_html}<h3>{e(titulo)}</h3>
          <p>{e(texto)}</p>
          <ul class="dash">{li}</ul>
        </div>
      </div>''')
    w(f'''
<section class="alt">
  <div class="wrap">
    {rot("O que fazemos")}
    <h2>{p["fazemos_titulo"]}</h2>
    <div class="blocks">
{chr(10).join(blocos)}
    </div>
  </div>
</section>
''')

    linhas = "\n        ".join(
        f'<tr{" class=\"opt\"" if opt else ""}><td>{e(d)}</td><td>{e(c)}</td><td>{e(f)}</td></tr>' for d, c, f, opt in p["recebe"])
    w(f'''
<section>
  <div class="wrap">
    {rot("O que você recebe")}
    <h2>{p["recebe_titulo"]}</h2>
    <div style="overflow-x:auto">
    <table class="table">
      <thead><tr><th>Documento</th><th>O que contém</th><th>Formato</th></tr></thead>
      <tbody>
        {linhas}
      </tbody>
    </table>
    </div>
  </div>
</section>
''')

    passos = "\n      ".join(f"<li><div><b>{e(t)}</b>{e(d)}</div></li>" for t, d in p["passos"])
    w(f'''
<section class="alt">
  <div class="wrap">
    {rot("Como funciona")}
    <h2>{p["como_titulo"]}</h2>
    <p class="lead">{e(p["como_lead"])}</p>
    <ol class="steps">
      {passos}
    </ol>
    <div class="cta-row">{btn("Pedir valor e prazo")}</div>
  </div>
</section>

<section class="nofaz">
  <div class="wrap">
    <span class="label">O que não fazemos</span>
    <p>{e(p["nao_fazemos"])}</p>
  </div>
</section>
''')

    nums = "\n      ".join(f"<div><b>{e(n).replace(' ', '&nbsp;')}</b><span>{e(t)}</span></div>" for n, t in p["numeros"])
    casos = []
    for big, quem, titulo, texto in p["casos"]:
        casos.append(f'''      <article class="case">
        <div class="big{" txt" if (not big[0].isdigit() or len(big) > 6) else ""}">{e(big).replace(" ", "&nbsp;")}</div>
        <div><p class="who">{e(quem)}</p><h3>{e(titulo)}</h3><p>{e(texto)}</p></div>
      </article>''')
    tambem = f'<p class="also"><strong>Também:</strong> {e(p["tambem"])}</p>' if p["tambem"] else ""
    w(f'''
<section>
  <div class="wrap">
    {rot("Projetos entregues")}
    <h2>Projetos que <em class="g">já entregamos</em></h2>
    <div class="nums">
      {nums}
    </div>
    <div class="cases">
{chr(10).join(casos)}
    </div>
    {tambem}
    <div class="cta-row">{btn("Falar com o engenheiro")}</div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    {rot("Clientes")}
    <h2>Empresas que <em class="g">confiam</em> na Celone</h2>
    <p class="clients-hi">{nomes(p["destaque"])}</p>
    <p class="clients-all">{nomes(outros)}</p>
    <p class="clients-tag"><b>Mais de 300 clientes em 15 estados</b>, desde 2019.</p>
  </div>
</section>
''')

    av = []
    for nome, serv in p["avaliacoes"]:
        av.append(f'''      <figure class="review todo"><div class="stars" aria-label="5 estrelas">★★★★★</div><blockquote>[Colar o texto real da avaliação do Google, sem reescrever]</blockquote><cite><b>{e(nome or "Nome do cliente")}</b> · {e(serv)}</cite></figure>''')
    w(f'''
<!-- AVALIAÇÕES: só avaliações reais do Google, texto copiado sem reescrever, com nome e serviço.
     Remover a classe "todo" ao preencher. Se não houver ao menos 3, ocultar a seção. -->
<section>
  <div class="wrap">
    {rot("Avaliações")}
    <h2>O que dizem os <em class="g">clientes</em></h2>
    <div class="reviews">
{chr(10).join(av)}
    </div>
    <a class="gl" href="#LINK-PERFIL-GOOGLE" target="_blank" rel="noopener">Ver todas as avaliações no Google →</a>
  </div>
</section>

<section class="alt" id="sobre">
  <div class="wrap rt">
    <div class="portrait">Retrato real do Eng. Matteo Celone<br>(foto da proposta, alta resolução)</div>
    <div>
      {rot("Responsável técnico")}
      <h2>Quem assina o seu <em class="g">projeto</em></h2>
      <p>Engenheiro mecânico formado pela UFRN e pela Politecnico di Torino (Itália), mestre pela UFRN e com especialização em análise de dados e gestão de projetos pela USP. Foi gestor de projetos industriais na Nestlé Brasil e atuou na Petrobras e na Brava Energia. Mais do que documentos, entrega clareza, segurança e respaldo técnico.</p>
      <div class="creds">
        <div><span>Registro</span><p>CREA 2118861648</p></div>
        <div><span>Formação</span><p>UFRN · Politecnico di Torino · Mestrado UFRN · USP</p></div>
        <div><span>Indústria</span><p>Nestlé Brasil · Petrobras · Brava Energia</p></div>
        <div><span>Escritório</span><p>Natal/RN · atendimento em todo o Brasil</p></div>
      </div>
    </div>
  </div>
</section>
''')

    faq = "\n      ".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])
    w(f'''
<section>
  <div class="wrap">
    {rot("Perguntas frequentes")}
    <h2>{p["faq_titulo"]}</h2>
    <div class="faq">
      {faq}
    </div>
  </div>
</section>

<section class="close">
  <div class="wrap">
    <span class="label">Peça sua proposta</span>
    <h2>{p["fechamento"]}</h2>
    <div class="cta-row">{btn("Falar com o engenheiro")}</div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <p><strong>Celone Engenharia LTDA</strong> · CNPJ 55.514.523/0001-48</p>
    <p>Responsável técnico: Eng. Matteo Celone, CREA 2118861648</p>
    <p>Av. Engenheiro Roberto Freire, 1962, Capim Macio, Natal/RN, 59082-095</p>
    <p>WhatsApp <a class="js-zap" href="{ZAP}">(18) 99113-7803</a> · <a href="mailto:celoneengenharia@gmail.com">celoneengenharia@gmail.com</a> · <a href="https://www.instagram.com/celoneengenharia" rel="noopener">Instagram</a></p>
    <p>Imagens de ambientes e equipamentos meramente ilustrativas.</p>
  </div>
</footer>

<a class="float js-zap" href="{ZAP}" aria-label="Falar no WhatsApp"><svg><use href="#wa"/></svg><span>WhatsApp</span></a>

<script>
(function () {{
  var CODIGO_PAGINA = '{p["codigo"]}';
  var ASSUNTO = '{p["assunto"]}';
  var origem = 'site', codigo = CODIGO_PAGINA;
  try {{
    var q = new URLSearchParams(location.search);
    var c = q.get('utm_campaign'), g = q.get('gclid');
    if (c || g) {{ sessionStorage.setItem('celone_origem', JSON.stringify({{c: c || CODIGO_PAGINA, o: 'Google'}})); }}
    var s = JSON.parse(sessionStorage.getItem('celone_origem') || 'null');
    if (s) {{ origem = s.o; codigo = s.c; }}
  }} catch (e) {{}}
  var msg = 'Olá! Vim pelo ' + origem + ' (' + codigo + ') e quero orçamento de ' + ASSUNTO + '.';
  document.querySelectorAll('.js-zap, a[href*="wa.me"]').forEach(function (a) {{
    try {{ var u = new URL(a.href); u.searchParams.delete('text'); var b = u.toString();
      a.href = b + (b.indexOf('?') > -1 ? '&' : '?') + 'text=' + encodeURIComponent(msg); }} catch (e) {{}}
    a.addEventListener('click', function () {{
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({{event: 'clique_whatsapp', pagina: CODIGO_PAGINA}});
    }});
  }});
}})();
</script>
</body>
</html>
''')
    txt = "".join(o)
    # Evita quebrar "NR-12"/"NR-35" no hífen dentro dos títulos
    for n in ("NR-12", "NR-13", "NR-35"):
        txt = txt.replace(f"{n}</em>", n.replace("-", "&#8209;") + "</em>")
        txt = txt.replace(f"<h2>{n}", "<h2>" + n.replace("-", "&#8209;"))
    os.makedirs(os.path.join(AQUI, p["pasta"]), exist_ok=True)
    with open(os.path.join(AQUI, p["pasta"], "index.html"), "w", encoding="utf-8") as f:
        f.write(txt)
    return p["pasta"]


if __name__ == "__main__":
    for pg in PAGINAS:
        print("gerada:", gerar(pg) + "/index.html")
