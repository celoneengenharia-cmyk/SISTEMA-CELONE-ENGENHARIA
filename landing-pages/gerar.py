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
        seo_desc="Projeto de exaustão, ventilação e climatização (HVAC) com memorial de cálculo, desenhos e ART. Atendemos empresas em todo o Brasil.",
        servicos=["Projeto de exaustão", "Projeto de ventilação e antecâmara", "Projeto de climatização e HVAC", "Projeto de redes de vapor e ar comprimido"],
        rotulo="Projetos mecânicos com ART",
        titulo='Projeto de exaustão e climatização <em class="g">pronto para aprovar</em>',
        sub="Memorial, desenhos e ART na mão para aprovar na vigilância sanitária e nos bombeiros. Seu instalador recebe tudo pronto para cotar e executar. <strong>Atendemos empresas em todo o Brasil.</strong>",
        btn="Receber proposta hoje",
        nota="Escopo, valor e prazo no mesmo dia, pelo WhatsApp.",
        faixa=[("Responsável técnico", "Eng. Matteo Celone · CREA 2118861648"), ("Entrega", "Memorial, desenhos (DWG, PDF, Revit) e ART"), ("Proposta", "No mesmo dia · todo o Brasil")],
        # Bloco "Empresas que já confiam" logo após o topo, com espaços para preencher
        prova_topo=dict(
            titulo='Empresas que já confiam na <em class="g">Celone Engenharia</em>',
            vagas=8,
            # (arquivo em _base/img/clientes/, nome da empresa) — logos em branco, fundo transparente
            logos=[
                ("axia-energia.png", "AXIA Energia"),
                ("jt-express.png", "J&T Express"),
                ("acotubo.png", "Grupo Açotubo"),
                ("guararapes-riachuelo.png", "Guararapes | Riachuelo"),
            ],
        ),
        prova_rotulo=None,
        destaque=["LAFEPE", "Karne Keijo", "N1MED", "LD Diagnósticos", "AABB Natal", "Sesc"],
        mostrar_clientes=False,
        rt_no_inicio=True,  # responsável técnico logo após "Quando você precisa"
        alerta=None,
        quando_titulo='Prazo para aprovar? <em class="g">A gente resolve.</em>',
        quando=[
            ("Vigilância sanitária", "Pediu o projeto de exaustão ou ventilação. Entregamos pronto para protocolar.", "doc"),
            ("Bombeiros", "O projeto de incêndio travou na exaustão ou na ventilação da antecâmara. Dimensionamos e assinamos.", "fogo"),
            ("Obra ou reforma", "A climatização precisa fechar com a arquitetura e a elétrica antes da obra começar.", "obra"),
            ("Conforto e qualidade do ar", "Ambiente quente, ar parado, fumaça ou cheiro incomodando a equipe ou os vizinhos. Resolvemos na origem.", "ar"),
            ("Escritórios e construtoras", "Terceirize a disciplina de HVAC com quem calcula, desenha e assina.", "camadas"),
        ],
        fazemos_titulo='Exaustão, ventilação e climatização <em class="g">num só projeto</em>',
        blocos=[
            ("Exaustão", None, "Captação, dutos, exaustor e filtragem dimensionados para a sua operação. Ar limpo dentro e fora da empresa.", ["Exaustão industrial e de processos", "Coifas e cozinhas industriais (NBR 14518)", "Filtragem de fumaça, gordura e odores"]),
            ("Ventilação e antecâmara", None, "Vazões e renovação de ar calculadas ambiente por ambiente, prontas para o projeto de incêndio.", ["Antecâmara exigida pelos bombeiros", "Laboratórios, áreas técnicas e sanitários", "Casa de máquinas e exaustão de solda"]),
            ("Climatização e HVAC", None, "Carga térmica por ambiente e a tecnologia certa para o seu uso, com dutos, tubulações e drenos.", ["Split, cassete, VRF e água gelada", "Qualidade do ar conforme a NBR 16401", "Gradiente de pressão entre salas"]),
            ("Vapor e ar comprimido", None, "Redes de utilidades projetadas junto com o HVAC e compatibilizadas no entreforro.", ["Troncais, ramais e pontos por sala", "Ar em contato com o produto (ISO 8573-1)", "Interface com a NR-13"]),
        ],
        recebe_titulo='Tudo o que você recebe, <em class="g">pronto para protocolar</em>',
        recebe=[
            ("Memorial de cálculo", "Vazões, carga térmica, perdas de carga e dimensionamento", "PDF assinado", False),
            ("Memorial descritivo", "Especificação completa do sistema e dos equipamentos", "PDF · DOCX", False),
            ("Desenhos", "Planta, cortes, isométricos e detalhes", "PDF · DWG · Revit", False),
            ("Lista de materiais", "Seu instalador cota e compra sem retrabalho", "PDF · XLSX", False),
            ("ART", "Responsabilidade técnica recolhida no CREA", "PDF", False),
            ("Acompanhamento", "Seguimos com você até a aprovação no órgão", "—", False),
        ],
        como_titulo='Do primeiro contato à <em class="g">aprovação</em>, em 4 passos',
        como_lead="Sem esperar visita: o levantamento pode ser feito por vídeo, com a nossa equipe guiando cada medida.",
        passos=[
            ("Mande o que você tem", "Planta ou croqui, fotos, lista de equipamentos e quem está exigindo o projeto."),
            ("Receba a proposta no mesmo dia", "Escopo, valor e prazo, direto no WhatsApp."),
            ("Levantamento presencial ou por vídeo", "Orientamos o que fotografar e medir. O projeto e a ART são os mesmos."),
            ("Projeto entregue com ART", "E seguimos com você até a aprovação na vigilância ou nos bombeiros."),
        ],
        nao_fazemos=None,
        numeros=[("300+", "clientes atendidos"), ("15", "estados"), ("5.450 m²", "de centro de distribuição em um só projeto"), ("2019", "desde, com ART em todo trabalho")],
        casos=[
            ("Recife/PE", "LAFEPE", "HVAC e utilidades de planta farmacêutica", "Unidades de tratamento de ar, água gelada, gradiente de pressão entre salas, vapor e ar comprimido."),
            ("5.450 m²", "Karne Keijo · Parnamirim/RN", "Centro de distribuição climatizado", "Climatização, renovação de ar, exaustão da cozinha coifa por coifa e GLP."),
            ("Rio/RJ", "N1MED · Copacabana", "Hamburgueria com cheiro na vizinhança", "Coifa, duto até a cobertura, exaustor e filtro eletrostático. Problema resolvido na origem."),
        ],
        tambem="LD Diagnósticos — ventilação de laboratório, Foz do Iguaçu/PR · AABB Natal — climatização.",
        avaliacoes=[("Matheus Gabriel Souza", "Projetos de engenharia"), ("Pedro Micali", "Projetos"), (None, "Projeto de exaustão ou HVAC")],
        faq_titulo='Dúvidas sobre o <em class="g">projeto de exaustão</em>',
        faq=[
            ("Vocês atendem a minha cidade?", "Sim. Atendemos todo o Brasil, com clientes em 15 estados. O levantamento pode ser presencial ou por vídeo, e o projeto e a ART são os mesmos."),
            ("O projeto serve para a vigilância sanitária e para os bombeiros?", "Sim. Sai com memorial de cálculo, desenhos e ART, conforme as normas ABNT aplicáveis, como a NBR 16401 (climatização e qualidade do ar). E seguimos com você até a aprovação."),
            ("Meu instalador consegue executar o projeto?", "Sim. Ele recebe desenhos detalhados e a lista de materiais pronta para cotar. Se você ainda não tem instalador, indicamos parceiros de confiança."),
            ("Em quanto tempo fica pronto?", "Depende do tamanho e do número de ambientes. O prazo vem junto com o valor na proposta, que você recebe no mesmo dia."),
            ("O que preciso mandar para o orçamento?", "Planta ou croqui, fotos do local, a lista de equipamentos e quem está exigindo o projeto. Se não tiver tudo, mande o que tem que a gente orienta."),
            ("Vocês atendem escritórios de engenharia e construtoras?", "Sim. Assumimos a disciplina de HVAC com ART e entregamos em DWG, PDF e Revit, compatibilizado com arquitetura e elétrica."),
        ],
        fechamento='Mande a planta e receba hoje <em class="g">escopo, valor e prazo.</em>',
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


ICONES = {
    "doc": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/><path d="M10 14l2 2 4-4"/>',
    "fogo": '<path d="M12 3c1 4 6 6 6 11a6 6 0 0 1-12 0c0-3 2-5 3-6 0 2 1 3 2 3 0-3 0-6 1-8z"/>',
    "obra": '<path d="M4 21V9l8-5 8 5v12"/><path d="M9 21v-6h6v6"/>',
    "ar": '<path d="M3 9h11a3 3 0 1 0-3-3"/><path d="M3 15h15a3 3 0 1 1-3 3"/><path d="M3 12h7"/>',
    "camadas": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    "calc": '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M8 7h8"/><path d="M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 18h.01M12 18h.01M16 18h.01"/>',
    "texto": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/><path d="M10 13h6M10 17h6"/>',
    "desenho": '<rect x="3" y="4" width="18" height="16"/><path d="M3 10h8v10M11 14h10"/>',
    "lista": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6h.01M4 12h.01M4 18h.01"/>',
    "selo": '<circle cx="12" cy="9" r="5"/><path d="M9 13.5L8 21l4-2 4 2-1-7.5"/>',
    "aprova": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
    "clipe": '<path d="M20 11l-8.5 8.5a5 5 0 0 1-7-7L13 4a3.5 3.5 0 0 1 5 5l-8.5 8.5a2 2 0 0 1-3-3L14 7"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8"/>',
    "video": '<rect x="3" y="7" width="13" height="10" rx="1"/><path d="M16 11l5-3v8l-5-3"/>',
}

# Ícone de cada entregável, pela palavra-chave do nome
ICONE_ENTREGA = [("cálculo", "calc"), ("descritivo", "texto"), ("desenho", "desenho"), ("lista", "lista"),
                 ("art", "selo"), ("responsável", "selo"), ("acompanhamento", "aprova"), ("laudo", "texto")]
# Ícone dos 4 passos de "Como funciona"
ICONE_PASSOS = ["clipe", "chat", "video", "aprova"]


def icone_entrega(nome):
    n = nome.lower()
    for chave, ic in ICONE_ENTREGA:
        if (n == chave) if chave == "art" else (chave in n):
            return ic
    return "texto"


def icone(nome):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICONES[nome]}</svg>'


def btn(texto):
    return f'<a class="btn js-zap" href="{ZAP}"><svg><use href="#wa"/></svg>{texto}</a>'


def nomes(lista):
    return ' <i>·</i> '.join(e(n) for n in lista)


def prova_topo(p):
    """Faixa de prova logo após o topo.

    - prova_topo=dict(titulo, vagas): bloco "Empresas que já confiam" com espaços
      para preencher (nome em texto ou logo autorizado).
    - senão: faixa com os nomes de `destaque`.
    """
    pt = p.get("prova_topo")
    if pt:
        logos = pt.get("logos", [])
        itens = [f'<div class="slot"><img src="../_base/img/clientes/{arq}" alt="{e(nome)}" loading="lazy"></div>'
                 for arq, nome in logos]
        itens += [f'<div class="slot"><!-- trocar pelo nome ou <img> do logo autorizado -->[Empresa {i}]</div>'
                  for i in range(len(logos) + 1, pt["vagas"] + 1)]
        vagas = "\n      ".join(itens)
        return f'''
<!-- PROVA SOCIAL NO TOPO: preencher com as empresas escolhidas pelo Matteo -->
<section class="trust">
  <div class="wrap">
    <h2>{pt["titulo"]}</h2>
    <div class="slots">
      {vagas}
    </div>
    <p class="trust-num"><b>+300 clientes</b> em <b>15 estados</b>, com ART em todo trabalho desde 2019.</p>
  </div>
</section>
'''
    return f'''
<!-- Prova acima da dobra: clientes deste serviço logo após o topo -->
<div class="proofbar">
  <div class="wrap">
    <span class="label">{e(p["prova_rotulo"])}</span>
    <p class="names">{nomes(p["destaque"])} <i>·</i> <span style="color:var(--muted)">e mais de 300 clientes em 15 estados</span></p>
  </div>
</div>
'''


def gerar(p):
    secao = 0

    def rot(nome):
        nonlocal secao
        secao += 1
        return f'<span class="label">{secao} · {nome}</span>'

    def rt():
        marcas = ["Politecnico di Torino", "UFRN", "USP", "Nestlé Brasil", "Petrobras", "Brava Energia"]
        logos = "".join(f'<div class="logo-slot"><!-- trocar por <img> do logo, se autorizado -->{e(m)}</div>' for m in marcas)
        return f'''
<section class="rtx" id="sobre">
  <div class="wrap rt">
    <figure class="portrait-wrap">
      <img class="portrait-img" src="../_base/img/matteo-celone.webp" width="800" height="1000" loading="lazy" alt="Eng. Matteo Celone, responsável técnico da Celone Engenharia, no escritório em Natal/RN">
      <figcaption><b>Eng. Matteo Celone</b><span>Engenheiro mecânico · M.Sc. · CREA 2118861648</span></figcaption>
    </figure>
    <div class="bio">
      {rot("Responsável técnico")}
      <h2>Seu projeto assinado pelo <em class="g">Eng. Matteo Celone</em></h2>
      <p class="lead">Matteo é engenheiro mecânico formado pela UFRN e pela <strong>Politecnico di Torino</strong>, na Itália, mestre pela UFRN e especialista em análise de dados e gestão de projetos pela <strong>USP</strong>.</p>
      <p>Na carreira, foi gestor de projetos industriais na <strong>Nestlé Brasil</strong> e atuou na <strong>Petrobras</strong> e na <strong>Brava Energia</strong>. Essa vivência em grandes indústrias está em cada projeto da Celone: cálculo rigoroso, desenho claro e solução que funciona na prática.</p>
      <p>Todo projeto sai com a assinatura dele e ART recolhida no CREA.</p>
      <div class="cta-row">{btn("Pedir proposta")}</div>
    </div>
  </div>
  <div class="wrap">
    <p class="logos-label">Formação e experiência</p>
    <div class="logos">{logos}</div>
    <div class="ph ph-wide" role="img" aria-label="Escritório da Celone Engenharia em Natal/RN" data-foto="Foto real do escritório, com a marca na parede · 21:9"></div>
  </div>
</section>
'''

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
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
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
    <a class="nav-cta js-zap" href="{ZAP}">Pedir proposta</a>
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

''')
    w(prova_topo(p))
    if p["alerta"]:
        w(f'''
<!-- CONFIRMAR número e data da portaria antes de publicar -->
<div class="alerta"><div class="wrap"><p>{p["alerta"]}</p></div></div>
''')

    if p["quando"]:
        linhas = "\n      ".join(
            f'<div><span class="k">{icone(q[2]) if len(q) > 2 else ""}{e(q[0])}</span><p class="v">{e(q[1])}</p></div>' for q in p["quando"])
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

    if p.get("rt_no_inicio"):
        w(rt())

    blocos = []
    for titulo, para, texto, itens in p["blocos"]:
        li = "".join(f"<li>{e(i)}</li>" for i in itens)
        para_html = f'<p class="para">{e(para)}</p>' if para else ""
        blocos.append(f'''      <div class="block">
        <div class="ph" role="img" aria-label="" data-foto="Imagem ilustrativa 3:2 · {e(titulo)}"></div>
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
        f'<tr{" class=\"opt\"" if opt else ""}><td><span class="td-ico">{icone(icone_entrega(d))}{e(d)}</span></td><td>{e(c)}</td><td>{e(f)}</td></tr>' for d, c, f, opt in p["recebe"])
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

    passos = "\n      ".join(f"<li><div><b>{icone(ICONE_PASSOS[i % 4])}{e(t)}</b>{e(d)}</div></li>" for i, (t, d) in enumerate(p["passos"]))
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
''')
    if p.get("nao_fazemos"):
        w(f'''
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
        <div class="ph ph-case" role="img" aria-label="" data-foto="Foto real da entrega (com autorização do cliente)"></div>
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
    <div class="cta-row">{btn("Pedir proposta")}</div>
  </div>
</section>
''')
    if p.get("mostrar_clientes", True):
        w(f'''
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

''')
    if not p.get("rt_no_inicio"):
        w(rt())
    w(f'''
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
    <div class="cta-row">{btn("Pedir proposta")}</div>
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
