import csv
import matplotlib.pyplot as plt
import os
import re

arquivos = [
    "resultadoEDHMX",
    "resultadoSTMX",
    "resultadoEDHLI",
    "resultadoSTLI"
]

cores_mtg = {
    "W": "#F8F6D8",
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


def desenhar_circulos(ax, labels, y_base):
    for i, label in enumerate(labels):
        cores = label.split("/")

        for j, cor in enumerate(cores):
            cor_hex = cores_mtg.get(cor, "#000000")

            # empilhamento vertical
            circulo = plt.Circle(
                (i, y_base - (j * 1.2)),  # desce verticalmente
                0.25,
                color=cor_hex,
                clip_on=False
            )
            ax.add_patch(circulo)


def gerar_grafico(nome_arquivo):
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

    # 🔥 Aumenta espaçamento entre barras
    espacamento = 1.8
    posicoes = [i * espacamento for i in range(len(valores))]

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.bar(posicoes, valores, width=0.8)

    ax.set_xticks(posicoes)
    ax.set_xticklabels([""] * len(nomes))

    # Ajustar limite inferior para caber círculos
    min_val = - (max(len(n.split("/")) for n in nomes) * 1.5)
    ax.set_ylim(min_val, max(valores) * 1.1)

    # Desenhar círculos abaixo do gráfico
    desenhar_circulos(ax, nomes, y_base=0)

    ax.set_title(f"{nome_arquivo} - Distribuição")

    plt.tight_layout()
    plt.savefig(f"{nome_arquivo}_barras.png")
    plt.close()

    print(f"Gráfico melhorado gerado: {nome_arquivo}")


for arquivo in arquivos:
    gerar_grafico(arquivo)