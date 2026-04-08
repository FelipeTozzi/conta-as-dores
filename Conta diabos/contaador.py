import csv

# Contador de inserções
contador_insercoes = 0

# Variáveis
combinacao = {
    "mono white": 0,
    "mono blue": 0,
    "mono black": 0,
    "mono red": 0,
    "mono green": 0,
    "azorios (White Blue)": 0,
    "Boros (Red White)": 0,
    "Dimir (Blue Black)": 0,
    "Golgari (Black Green)": 0,
    "Gruul (Red Green)": 0,
    "Izzet (Blue Red)": 0,
    "Orzhov (White Black)": 0,
    "Rakdos (Black Red)": 0,
    "Selesnya (White Green)": 0,
    "Simic (Blue Green)": 0,
    "Abzan (White Black Green)": 0,
    "Bant (White Blue Green)": 0,
    "Esper (White Blue Black)": 0,
    "Grixis (Blue Black Red)": 0,
    "Jeskai (Blue Red White)": 0,
    "Jund (Black Red Green)": 0,
    "Mardu (Red White Black)": 0,
    "Naya (Red White Green)": 0,
    "Sultai (Blue Black Green)": 0,
    "Temur (Blue Red Green)": 0,
    "Glint (White Blue Red Green)": 0,
    "Dune (White Blue Black Green)": 0,
    "Ruin (White Blue Black Red)": 0,
    "Witch (Blue Black Red Green)": 0,
    "Yore (White Red Black Green)": 0
}

# Mapeamento de teclas -> variáveis
mapa_teclas = {
    "Q": "mono white",
    "W": "mono blue",
    "E": "mono black",
    "R": "mono red",
    "T": "mono green",
    "Y": "azorios (White Blue)",
    "U": "Boros (Red White)",
    "I": "Dimir (Blue Black)",
    "O": "Golgari (Black Green)",
    "P": "Gruul (Red Green)",
    "A": "Izzet (Blue Red)",
    "S": "Orzhov (White Black)",
    "D": "Rakdos (Black Red)",
    "F": "Selesnya (White Green)",
    "G": "Simic (Blue Green)",
    "H": "Abzan (White Black Green)",
    "J": "Bant (White Blue Green)",
    "K": "Esper (White Blue Black)",
    "L": "Grixis (Blue Black Red)",
    "Ç": "Jeskai (Blue Red White)",
    "Z": "Jund (Black Red Green)",
    "X": "Mardu (Red White Black)",
    "C": "Naya (Red White Green)",
    "V": "Sultai (Blue Black Green)",
    "B": "Temur (Blue Red Green)",
    "N": "Glint (White Blue Red Green)",
    "M": "Dune (White Blue Black Green)",
    "<": "Ruin (White Blue Black Red)",
    ">": "Witch (Blue Black Red Green)",
    ":": "Yore (White Red Black Green)"
}

def mostrar_menu():
    print("\n=== MENU ===")
    for tecla, nome in mapa_teclas.items():
        print(f"{tecla} - Incrementar {nome}")
    print("0 - Finalizar e salvar CSV")

def salvar_csv():
    with open("resultado.csv", "w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        
        writer.writerow(["Variável", "Valor"])
        
        for nome, valor in combinacao.items():
            writer.writerow([nome, valor])
        
        writer.writerow([])
        writer.writerow(["Total de Inserções", contador_insercoes])

    print("\nArquivo 'resultado.csv' criado com sucesso!")

# Loop principal
while True:
    mostrar_menu()
    
    opcao = input("Escolha uma opção: ").upper()
    
    if opcao in mapa_teclas:
        nome_variavel = mapa_teclas[opcao]
        combinacao[nome_variavel] += 1
        contador_insercoes += 1
        print(f"{nome_variavel} incrementado!")
        
    elif opcao == "0":
        salvar_csv()
        break
        
    else:
        print("Opção inválida, tente novamente.")

# Resumo final
print("\nResumo final:")
for nome, valor in combinacao.items():
    print(f"{nome}: {valor}")

print(f"Total de inserções: {contador_insercoes}")