import csv
import matplotlib.pyplot as plt
import os
import re
import matplotlib.colors as mcolors

arquivos = [
    "resultadoEDHMX",
    "resultadoSTMX",
    "resultadoEDHLI",
    "resultadoSTLI"
]

PASTA_GRAFICOS = "graficos"
os.makedirs(PASTA_GRAFICOS, exist_ok=True)

cores_mtg = {
    "W": "#FFF2B2",
    "U": "#0E68AB",
    "B": "#150B00",
    "R": "#D3202A",
    "G": "#00733E",
    "C": "#AAAAAA"
}

mapa_cores = {
    "White": "W",
    "Blue": "U",
    "Black": "B",
    "Red": "R",
    "Green": "G"
}

def converter_nome(nome):
    nome = nome.strip()

    if nome.lower().startswith("mono"):
        return mapa_cores.get(nome.split()[1].capitalize(), nome)

    if nome == "Todas Cores":
        return "W/U/B/R/G"

    if nome == "Colorless":
        return "C"

    match = re.search(r"\((.*?)\)", nome)
    if match:
        cores = match.group(1).split()
        return "/".join([mapa_cores.get(c, c) for c in cores])

    return nome


def misturar_cores(lista_cores):
    rgbs = [mcolors.to_rgb(cores_mtg.get(c, "#000000")) for c in lista_cores]
    media = [sum(c[i] for c in rgbs) / len(rgbs) for i in range(3)]
    return media


def desenhar_circulos(ax, x_positions, labels):
    for x, label in zip(x_positions, labels):
        cores = label.split("/")

        for i, cor in enumerate(cores):
            y = -1.2 - (i * 0.7)

            ax.scatter(
                x,
                y,
                s=220,
                c=cores_mtg.get(cor, "#000000"),
                edgecolors="black",
                linewidths=0.6,
                zorder=5,
                clip_on=False
            )


def gerar_graficos(nome_arquivo):
    nomes = []
    valores = []

    caminho_csv = f"{nome_arquivo}.csv"

    if not os.path.exists(caminho_csv):
        print(f"{caminho_csv} não encontrado")
        return

    with open(caminho_csv, "r", encoding="utf-8") as arquivo:
        reader = csv.reader(arquivo)
        next(reader)

        for linha in reader:
            if not linha or linha[0] == "Total de Inserções":
                break

            nome = converter_nome(linha[0])
            valor = int(linha[1])

            if valor > 0:
                nomes.append(nome)
                valores.append(valor)

    espacamento = 1.6
    x_positions = [i * espacamento for i in range(len(valores))]

    # =====================
    # 📊 GRÁFICO DE BARRAS
    # =====================
    fig, ax = plt.subplots(figsize=(18, 10), dpi=200)

    ax.bar(x_positions, valores, width=0.7)

    ax.set_xticks(x_positions)
    ax.set_xticklabels(nomes, rotation=45, ha="right", fontsize=10)

    max_cores = max(len(n.split("/")) for n in nomes)
    limite_inferior = - (max_cores * 0.8 + 2)

    ax.set_ylim(limite_inferior, max(valores) * 1.2)

    desenhar_circulos(ax, x_positions, nomes)

    ax.set_title(f"{nome_arquivo} - Barras", fontsize=14)

    plt.subplots_adjust(bottom=0.3)

    caminho_saida = os.path.join(PASTA_GRAFICOS, f"{nome_arquivo}_barras.png")
    plt.savefig(caminho_saida, dpi=200)
    plt.close()

    # =====================
    # 🥧 GRÁFICO DE PIZZA (TOP 10 LIMPO)
    # =====================

    dados = sorted(zip(valores, nomes), reverse=True)

    top10 = dados[:10]

    valores_top = [v for v, n in top10]
    nomes_top = [n for v, n in top10]

    outros = sum(valores) - sum(valores_top)

    if outros > 0:
        valores_top.append(outros)
        nomes_top.append("Outros")

    # 🎨 cores das fatias
    cores_pizza = []
    for nome in nomes_top:
        if nome == "Outros":
            cores_pizza.append("#CCCCCC")
        else:
            lista = nome.split("/")
            cores_pizza.append(misturar_cores(lista))

    fig2, ax2 = plt.subplots(figsize=(14, 14), dpi=300)

    wedges, texts, autotexts = ax2.pie(
        valores_top,
        labels=nomes_top,
        autopct='%1.1f%%',
        colors=cores_pizza,
        startangle=90,
        textprops={'fontsize': 11},
        labeldistance=1.25,
        pctdistance=0.70
    )

    for t in texts:
        t.set_horizontalalignment('center')

    for t in autotexts:
        t.set_fontsize(10)

    ax2.set_title(f"{nome_arquivo} - Top 10 Combinações", fontsize=16)

    plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05)

    caminho_saida_pizza = os.path.join(PASTA_GRAFICOS, f"{nome_arquivo}_pizza_top10.png")
    plt.savefig(caminho_saida_pizza, dpi=300)
    plt.close()

    print(f"Gráficos gerados: {nome_arquivo}")


for arquivo in arquivos:
    gerar_graficos(arquivo)