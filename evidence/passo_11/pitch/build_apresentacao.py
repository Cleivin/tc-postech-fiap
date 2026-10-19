"""Gera o PowerPoint do pitch executivo (Passo 11).

Saída: evidence/passo_11/pitch/pitch_executivo.pptx
Números da run 20d3623d0430. Não altera o pipeline.
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

OUT = Path(__file__).resolve().parent / "pitch_executivo.pptx"

NAVY = RGBColor(0x0B, 0x1E, 0x33)
NAVY_2 = RGBColor(0x14, 0x32, 0x4F)
INK = RGBColor(0x14, 0x20, 0x2B)
MUTED = RGBColor(0x5C, 0x6A, 0x78)
CREAM = RGBColor(0xF6, 0xF3, 0xEC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
AMBER = RGBColor(0xB5, 0x74, 0x12)
AMBER_SOFT = RGBColor(0xF8, 0xEB, 0xD0)
CARD = RGBColor(0xFF, 0xFC, 0xF8)
LINE = RGBColor(0xE3, 0xDB, 0xCC)
HAIR = RGBColor(0xD5, 0xCB, 0xB8)
UP = RGBColor(0x1B, 0x5E, 0x45)
DOWN = RGBColor(0x8C, 0x3A, 0x32)
FONT = "Calibri"

W, H = 13.333, 7.5

NOTES = [
    "O Brasil assumiu um compromisso: toda criança alfabetizada até o fim do segundo ano do ensino fundamental. O Inep definiu o corte em 743 pontos na escala do Saeb. O indicador é o percentual de estudantes que chegam a esse ponto. A régua deste projeto é a meta pactuada da rede pública: 80 por cento em 2030. Universalização é outra leitura, e fica de fora dessa conta.",
    "Um percentual nacional esconde o território. Em 2024, na rede pública, o Ceará está em 85,31 por cento, acima da meta. A Bahia está em 35,96. Quarenta e nove pontos percentuais separam os dois. No país, a taxa foi de 55,9 em 2023 para 59,2 em 2024. Ainda faltam 20,8 pontos para chegar a 80. Nos municípios da rede municipal, 1.141 de 5.448 atingiram a meta em 2024, cerca de 21 por cento. No ano anterior, 935, cerca de 17 por cento. O dado mostra onde o resultado já chegou, onde a distância é grande e onde a meta nem está cadastrada.",
    "Esta fase não prevê 2030 e não treina modelo. Ela organiza a evidência. Seis conjuntos oficiais entram crus, com histórico preservado: alunos, municípios, unidades da federação e as metas do país, da UF e do município. É a camada Bronze. Na Silver, o dicionário oficial traduz os códigos e o resultado encontra a meta do mesmo recorte. A rede vem como número numa tabela e como nome na outra. Sem esse alinhamento, o cruzamento falha em silêncio. Se a correspondência fica abaixo de 95 por cento, a publicação para. Ausência continua ausência. Não vira zero. A Gold guarda os produtos analíticos, com origem oficial. Um fluxo simulado de eventos corre separado e não mexe nesses números.",
    "A Gold já responde o que a política precisa enxergar, com os números da fonte. O Brasil de 2024 está em 59,2. Meta 80. Status: não atingiu. O Ceará, na rede pública, está em 85,31. É a única unidade da federação nesse recorte acima da meta. Em 2023 também estava, em 84,46. A comparação separa três situações: atingiu, não atingiu e sem meta. Há 242 linhas municipais sem meta. A taxa média delas é 53,7. A de quem não atingiu fica em 55,2. Tratar esse vazio como fracasso distorce a prioridade. A trajetória também já está na tabela, sem virar previsão. De 2023 para 2024, na rede pública, Minas Gerais subiu 12,26 pontos. O Rio Grande do Sul caiu 18,76.",
    "A confiança vem de uma auditoria. Quase 3,9 milhões de registros de alunos permitem recalcular a taxa e compará-la à oficial. A diferença mediana é de 0,0037 ponto percentual. O indicador publicado segue sendo o do Inep. E o corte de 743 está consistente com a classificação oficial: quem está alfabetizado fica em 743 ou acima. Quem não está, e tem nota, não alcança esse ponto. O projeto não reinventa o critério.",
    "Modelos e aplicações de inteligência artificial são a fase seguinte. Ainda não existem neste projeto. O uso natural da base é estimar a taxa de um ano que ainda não está na série, ou se um município cruza os 80. O insumo é o passado: taxa anterior, variação do ano anterior, rede, série e a composição por nível de proficiência em 2024. O resultado do mesmo ano, e a distância até a meta calculada a partir dele, não entram como insumo. Senão o modelo apenas inverte uma fórmula. Com dois anos de histórico, uma linha até 2030 seria cenário, não previsão. Essa conta não foi feita.",
    "O que está pronto é a base: território, trajetória e meta na mesma régua, com o número oficial preservado. A decisão continua humana. O que esta fase muda é a condição de tomá-la com evidência.",
]


def rect(slide, l, t, w, h, fill, line_color=None, radius=None, line_pt=1.0):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line_color is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_pt)
    if radius is not None:
        shape.adjustments[0] = radius
    sp_pr = shape._element.spPr
    effect = sp_pr.find(qn("a:effectLst"))
    if effect is not None:
        sp_pr.remove(effect)
    return shape


def tb(slide, l, t, w, h, anchor="top"):
    shape = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.word_wrap = True
    frame.auto_size = None
    frame.margin_left = Emu(0)
    frame.margin_right = Emu(0)
    frame.margin_top = Emu(0)
    frame.margin_bottom = Emu(0)
    frame._txBody.bodyPr.set("anchor", {"top": "t", "middle": "ctr", "bottom": "b"}[anchor])
    return frame


def run(paragraph, text, size, bold=False, color=INK, font=FONT):
    r = paragraph.add_run()
    r.text = text
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    return r


def write(slide, l, t, w, h, text, size, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor="top"):
    frame = tb(slide, l, t, w, h, anchor)
    p = frame.paragraphs[0]
    p.alignment = align
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    run(p, text, size, bold, color)
    return frame


def footer(slide, n, dark=False, left="Indicador Criança Alfabetizada"):
    color = RGBColor(0xC5, 0xD0, 0xDA) if dark else MUTED
    write(slide, 0.55, 7.12, 9.6, 0.26, left, 12, False, color)
    write(slide, 11.2, 7.12, 1.55, 0.26, f"{n}  /  7", 12, False, color, PP_ALIGN.RIGHT)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def bg(slide, color):
    rect(slide, 0, 0, W, H, color)


def kicker_title(slide, kicker, title):
    write(slide, 0.55, 0.32, 12.2, 0.28, kicker, 13, True, AMBER)
    write(slide, 0.55, 0.60, 12.2, 0.62, title, 30, True, NAVY)


def light(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, CREAM)
    rect(slide, 0, 0, 0.10, H, AMBER)
    return slide


def dark(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, NAVY)
    rect(slide, 0, 0, 0.10, H, AMBER)
    return slide


def slide_1(prs):
    s = dark(prs)
    write(s, 0.62, 0.48, 11.5, 0.32, "COMPROMISSO NACIONAL CRIANÇA ALFABETIZADA", 14, True, AMBER)
    write(s, 0.62, 1.55, 12.0, 1.7, "Toda criança alfabetizada\naté o 2º ano", 44, True, WHITE)
    write(
        s,
        0.64,
        3.55,
        10.5,
        0.40,
        "Indicador Criança Alfabetizada   ·   rede pública",
        18,
        False,
        RGBColor(0xC5, 0xD0, 0xDA),
    )

    cards = [
        ("743", "pontos", "Corte do Inep na escala do Saeb"),
        ("Indicador", "percentual", "Estudantes que chegam a esse patamar"),
        ("80%", "em 2030", "Meta pactuada da rede pública"),
    ]
    x = 0.62
    for value, unit, caption in cards:
        rect(s, x, 4.35, 3.85, 1.85, NAVY_2, radius=0.08)
        write(s, x + 0.28, 4.50, 3.3, 0.62, value, 32, True, WHITE)
        write(s, x + 0.28, 5.12, 3.3, 0.28, unit, 14, True, AMBER)
        write(s, x + 0.28, 5.46, 3.3, 0.50, caption, 15, False, RGBColor(0xE4, 0xEA, 0xF0))
        x += 4.05

    write(
        s,
        0.64,
        6.42,
        11.5,
        0.32,
        "A universalização é outra leitura e não entra nesta conta.",
        15,
        False,
        RGBColor(0xC5, 0xD0, 0xDA),
    )
    footer(s, 1, dark=True, left="Fase 2  ·  preparar a base até a Gold")
    notes(s, NOTES[0])


def slide_2(prs):
    s = light(prs)
    kicker_title(s, "POR QUE O DADO IMPORTA", "Onde o resultado já chegou, e onde não chegou")
    write(s, 0.55, 1.28, 8, 0.28, "Rede pública   ·   2024   ·   taxa de alfabetização (%)", 14, False, MUTED)

    labels = [("Bahia", 35.96, "35,96"), ("Brasil", 59.2, "59,2"), ("Ceará", 85.31, "85,31")]
    plot_l, plot_w = 2.95, 8.85
    row_y = [1.85, 2.78, 3.71]
    bar_h = 0.52
    axis_y = 4.48

    for i in (0, 20, 40, 60, 100):
        x = plot_l + plot_w * (i / 100)
        rect(s, x, 1.78, 0.012, axis_y - 1.78, RGBColor(0xE7, 0xE0, 0xD2))
        write(s, x - 0.28, axis_y + 0.08, 0.56, 0.24, str(i), 11, False, MUTED, PP_ALIGN.CENTER)

    meta_x = plot_l + plot_w * 0.80
    for name, value, label in labels:
        y = row_y[labels.index((name, value, label))]
        write(s, 0.40, y, 2.35, bar_h, name, 18, True, NAVY, PP_ALIGN.RIGHT, "middle")
        bw = plot_w * (value / 100)
        rect(s, plot_l, y, bw, bar_h, NAVY, radius=0.15)
        if value >= 80:
            write(s, plot_l + bw + 0.12, y, 1.20, bar_h, label, 16, True, NAVY, PP_ALIGN.LEFT, "middle")
        else:
            write(s, plot_l + bw - 1.15, y, 1.02, bar_h, label, 14, True, WHITE, PP_ALIGN.RIGHT, "middle")

    line = s.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(meta_x), Inches(1.72), Inches(meta_x), Inches(axis_y)
    )
    line.line.color.rgb = AMBER
    line.line.width = Pt(2.25)
    from pptx.enum.dml import MSO_LINE

    line.line.dash_style = MSO_LINE.DASH

    write(s, meta_x - 0.55, axis_y + 0.08, 1.10, 0.24, "80", 12, True, AMBER, PP_ALIGN.CENTER)
    rect(s, meta_x - 0.72, 1.38, 1.44, 0.32, AMBER, radius=0.5)
    write(s, meta_x - 0.72, 1.38, 1.44, 0.32, "Meta 80", 12, True, WHITE, PP_ALIGN.CENTER, "middle")

    rect(s, plot_l, axis_y, plot_w, 0.015, HAIR)
    write(s, plot_l, axis_y + 0.32, plot_w, 0.26, "Taxa de alfabetização (%)", 12, False, MUTED, PP_ALIGN.CENTER)

    rect(s, 0.55, 5.28, 6.00, 1.55, CARD, LINE, radius=0.08)
    write(s, 0.78, 5.42, 5.55, 0.28, "BRASIL, 2023 PARA 2024", 12, True, AMBER)
    write(s, 0.78, 5.74, 5.55, 0.42, "55,9   →   59,2", 26, True, NAVY)
    write(s, 0.78, 6.22, 5.55, 0.40, "Ainda faltam 20,8 pontos para chegar a 80.", 15, False, INK)

    rect(s, 6.75, 5.28, 6.00, 1.55, CARD, LINE, radius=0.08)
    write(s, 6.98, 5.42, 5.55, 0.28, "REDE MUNICIPAL", 12, True, AMBER)
    write(s, 6.98, 5.74, 5.55, 0.42, "1.141  de  5.448", 26, True, NAVY)
    write(s, 6.98, 6.22, 5.55, 0.42, "atingiram 80 em 2024. Em 2023, eram 935.", 15, False, INK)

    footer(s, 2, left="Gold  ·  origem oficial  ·  2024")
    notes(s, NOTES[1])


def slide_3(prs):
    s = light(prs)
    kicker_title(s, "COMO A BASE FOI ORGANIZADA", "Três camadas, um número oficial")
    write(s, 0.55, 1.28, 12, 0.32, "Esta fase organiza a evidência. Ainda não prevê 2030 e não treina modelo.", 15, False, MUTED)

    layers = [
        ("01", "Bronze", "Dado cru, com histórico preservado.", "Alunos, municípios, UFs e as metas de cada nível."),
        ("02", "Silver", "Código traduzido pelo dicionário oficial.", "Resultado ligado à meta do mesmo recorte. Publica só se o cruzamento fica em 95% ou mais."),
        ("03", "Gold", "Indicador, distância até a meta e trajetória.", "Origem marcada como oficial."),
    ]
    xs = [0.55, 4.72, 8.89]
    for x, (num, name, line1, line2) in zip(xs, layers):
        rect(s, x, 1.85, 3.85, 3.55, CARD, LINE, radius=0.06)
        rect(s, x, 1.85, 3.85, 0.10, AMBER)
        write(s, x + 0.28, 2.12, 3.3, 0.28, num, 13, True, AMBER)
        write(s, x + 0.28, 2.42, 3.3, 0.50, name, 28, True, NAVY)
        write(s, x + 0.28, 3.15, 3.3, 0.85, line1, 16, True, INK)
        write(s, x + 0.28, 4.05, 3.3, 1.05, line2, 15, False, MUTED)

    for x in (4.28, 8.45):
        arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(3.35), Inches(0.36), Inches(0.22))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = AMBER
        arrow.line.fill.background()

    rect(s, 0.55, 5.65, 12.22, 1.20, NAVY, radius=0.06)
    write(s, 0.82, 5.82, 11.7, 0.30, "FORA DO NÚMERO OFICIAL", 12, True, AMBER)
    write(
        s,
        0.82,
        6.14,
        11.7,
        0.48,
        "Um fluxo simulado de eventos corre em trilha separada e não altera a taxa.",
        18,
        False,
        WHITE,
    )
    footer(s, 3)
    notes(s, NOTES[2])


def slide_4(prs):
    s = light(prs)
    kicker_title(s, "O QUE A GOLD JÁ RESPONDE", "Três leituras que a base já entrega")

    # Resultado
    rect(s, 0.55, 1.55, 4.00, 5.25, CARD, LINE, radius=0.06)
    write(s, 0.80, 1.74, 3.5, 0.26, "RESULTADO", 13, True, AMBER)
    write(s, 0.80, 2.10, 3.5, 0.70, "59,2", 40, True, NAVY)
    write(s, 0.80, 2.80, 3.5, 0.55, "Brasil, 2024\nfrente à meta 80 · não atingiu", 15, False, INK)
    rect(s, 0.80, 3.55, 3.5, 0.015, LINE)
    write(s, 0.80, 3.75, 3.5, 0.65, "85,31", 36, True, NAVY)
    write(s, 0.80, 4.45, 3.5, 0.90, "Ceará, rede pública.\nÚnica UF nesse recorte acima da meta.", 15, False, INK)
    write(s, 0.80, 5.85, 3.5, 0.55, "Em 2023 o Ceará já estava acima: 84,46.", 14, False, MUTED)

    # Lacuna
    rect(s, 4.75, 1.55, 4.00, 5.25, CARD, LINE, radius=0.06)
    write(s, 5.00, 1.74, 3.5, 0.26, "LACUNA DE CADASTRO", 13, True, AMBER)
    write(s, 5.00, 2.15, 3.5, 0.70, "242", 44, True, NAVY)
    write(s, 5.00, 2.90, 3.5, 0.70, "linhas municipais\nsem meta cadastrada", 18, False, INK)
    rect(s, 5.00, 3.75, 3.5, 0.015, LINE)
    write(s, 5.00, 4.00, 3.5, 0.28, "TAXA MÉDIA", 12, True, MUTED)
    write(s, 5.00, 4.28, 3.5, 0.50, "53,7", 32, True, NAVY)
    write(s, 5.00, 4.85, 3.5, 0.70, "Perto de quem não atingiu, cuja média é 55,2.", 15, False, INK)
    write(s, 5.00, 5.70, 3.5, 0.75, "Ausência de meta não é o mesmo que não atingir.", 15, True, NAVY)

    # Trajetória
    rect(s, 8.95, 1.55, 3.85, 5.25, CARD, LINE, radius=0.06)
    write(s, 9.18, 1.74, 3.45, 0.26, "TRAJETÓRIA", 13, True, AMBER)
    write(s, 9.18, 2.15, 3.45, 0.28, "Rede pública · 2023 para 2024", 13, False, MUTED)
    write(s, 9.18, 2.65, 3.45, 0.62, "+12,26", 36, True, UP)
    write(s, 9.18, 3.28, 3.45, 0.36, "Minas Gerais", 18, True, INK)
    write(s, 9.18, 3.95, 3.45, 0.62, "−18,76", 36, True, DOWN)
    write(s, 9.18, 4.58, 3.45, 0.36, "Rio Grande do Sul", 18, True, INK)
    rect(s, 9.18, 5.20, 3.4, 0.015, LINE)
    write(s, 9.18, 5.45, 3.45, 0.90, "Variação observada.\nAinda sem previsão.", 16, False, INK)

    footer(s, 4, left="Gold  ·  origem oficial")
    notes(s, NOTES[3])


def slide_5(prs):
    s = light(prs)
    kicker_title(s, "A CONFIANÇA DO NÚMERO", "O indicador oficial se sustenta")

    write(s, 0.55, 1.70, 7.4, 1.35, "0,0037", 80, True, NAVY)
    write(s, 0.58, 3.15, 7.2, 0.40, "ponto percentual", 22, True, AMBER)
    write(
        s,
        0.58,
        3.65,
        7.0,
        0.90,
        "Diferença mediana entre a taxa recalculada pelos alunos e a taxa oficial.",
        18,
        False,
        INK,
    )
    write(
        s,
        0.58,
        4.60,
        7.0,
        0.70,
        "O microdado audita.\nO ranking permanece o do Inep.",
        18,
        True,
        NAVY,
    )

    rect(s, 8.15, 1.70, 4.60, 2.15, CARD, LINE, radius=0.06)
    write(s, 8.40, 1.88, 4.15, 0.26, "REGISTROS DE ALUNOS", 12, True, AMBER)
    write(s, 8.40, 2.22, 4.15, 0.70, "3,9 milhões", 32, True, NAVY)
    write(s, 8.40, 3.00, 4.15, 0.55, "Quase 3,9 milhões de registros permitem refazer a conta.", 15, False, INK)

    rect(s, 8.15, 4.05, 4.60, 2.15, NAVY, radius=0.06)
    write(s, 8.40, 4.23, 4.15, 0.26, "CORTE DE 743", 12, True, AMBER)
    write(s, 8.40, 4.55, 4.15, 0.60, "743", 32, True, WHITE)
    write(
        s,
        8.40,
        5.25,
        4.15,
        0.70,
        "A classificação oficial e a proficiência contam a mesma história.",
        15,
        False,
        RGBColor(0xE4, 0xEA, 0xF0),
    )

    footer(s, 5, left="Gold  ·  validação do microdado  ·  origem oficial")
    notes(s, NOTES[4])


def slide_6(prs):
    s = light(prs)
    kicker_title(s, "O QUE AINDA NÃO EXISTE", "A inteligência analítica é o próximo passo")

    rect(s, 0.55, 1.50, 6.00, 3.15, NAVY, radius=0.06)
    write(s, 0.82, 1.68, 5.5, 0.26, "PRONTO  ·  ESTA FASE", 13, True, AMBER)
    write(s, 0.82, 2.05, 5.5, 0.45, "Base Gold oficial", 26, True, WHITE)
    ready = "Indicador por território\nDistância até a meta 80\nTrajetória observada\nAuditoria do microdado"
    write(s, 0.82, 2.65, 5.5, 1.70, ready, 16, False, RGBColor(0xE4, 0xEA, 0xF0))

    rect(s, 6.78, 1.50, 6.00, 3.15, CARD, LINE, radius=0.06)
    write(s, 7.05, 1.68, 5.5, 0.26, "PLANEJADO  ·  PRÓXIMA FASE", 13, True, AMBER)
    write(s, 7.05, 2.05, 5.5, 0.45, "Ainda não construído", 26, True, NAVY)
    planned = "Análises mais profundas\nMachine learning\nAplicações de inteligência artificial\nEstimar um ano que ainda não está na série"
    write(s, 7.05, 2.65, 5.5, 1.70, planned, 16, False, INK)

    rect(s, 0.55, 4.85, 12.23, 0.95, AMBER_SOFT, radius=0.06)
    write(s, 0.80, 4.97, 11.8, 0.24, "PODE INFORMAR UM MODELO FUTURO", 12, True, AMBER)
    write(
        s,
        0.80,
        5.24,
        11.8,
        0.40,
        "Taxa anterior  ·  variação do ano anterior  ·  rede  ·  série  ·  composição por nível em 2024",
        15,
        False,
        INK,
    )

    rect(s, 0.55, 5.92, 12.23, 0.95, CARD, LINE, radius=0.06)
    write(s, 0.80, 6.04, 11.8, 0.24, "NÃO ENTRA COMO INSUMO DO ANO QUE SE QUER ESTIMAR", 12, True, DOWN)
    write(
        s,
        0.80,
        6.31,
        11.8,
        0.40,
        "A própria taxa  ·  a distância até a meta  ·  o status calculado a partir dela. Com dois anos, uma reta até 2030 seria cenário, não previsão.",
        15,
        False,
        INK,
    )

    footer(s, 6)
    notes(s, NOTES[5])


def slide_7(prs):
    s = dark(prs)
    write(s, 0.62, 0.42, 11.5, 0.30, "O QUE ESTA FASE MUDA", 14, True, AMBER)
    write(s, 0.62, 0.90, 12.0, 1.15, "Território, trajetória e meta\nna mesma régua", 36, True, WHITE)

    rect(s, 0.62, 2.45, 5.85, 1.85, NAVY_2, radius=0.08)
    write(s, 0.90, 2.60, 5.3, 0.28, "BRASIL, 2024", 13, True, AMBER)
    write(s, 0.90, 2.95, 5.3, 0.75, "59,2", 42, True, WHITE)
    write(s, 0.90, 3.75, 5.3, 0.32, "Meta 80  ·  não atingiu", 16, False, RGBColor(0xE4, 0xEA, 0xF0))

    rect(s, 6.70, 2.45, 5.95, 1.85, NAVY_2, radius=0.08)
    write(s, 6.98, 2.60, 5.4, 0.28, "META PACTUADA", 13, True, AMBER)
    write(s, 6.98, 2.95, 5.4, 0.75, "80", 42, True, WHITE)
    write(s, 6.98, 3.75, 5.4, 0.32, "Rede pública  ·  2030", 16, False, RGBColor(0xE4, 0xEA, 0xF0))

    write(s, 0.64, 4.60, 5.8, 0.28, "PRONTO AGORA", 13, True, AMBER)
    write(s, 0.64, 4.92, 5.8, 0.70, "Indicador oficial, distância até 80,\ntrajetória e auditoria.", 16, False, WHITE)

    write(s, 6.72, 4.60, 5.9, 0.28, "AINDA À FRENTE", 13, True, AMBER)
    write(
        s,
        6.72,
        4.92,
        5.9,
        0.70,
        "Modelos, aplicações de IA e, se fizer sentido,\num cenário nomeado como cenário.",
        16,
        False,
        WHITE,
    )

    write(
        s,
        0.62,
        6.05,
        12.0,
        0.70,
        "A decisão continua humana.\nA evidência já pode sustentá-la.",
        22,
        True,
        WHITE,
    )
    footer(s, 7, dark=True, left="Fase 2  ·  Gold, origem oficial")
    notes(s, NOTES[6])


def main():
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    prs.core_properties.title = "Toda criança alfabetizada até o 2º ano"
    prs.core_properties.subject = "Pitch executivo — Tech Challenge Fase 2"
    slide_1(prs)
    slide_2(prs)
    slide_3(prs)
    slide_4(prs)
    slide_5(prs)
    slide_6(prs)
    slide_7(prs)
    prs.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
