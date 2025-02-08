import json
import os

def carregar_tabela_precos(arquivo):
    """
    Carrega a tabela de preços do arquivo JSON e retorna a lista de combinações.
    """
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        return dados.get("combinacoes", [])
    else:
        return []

def salvar_tabela_precos(arquivo, combinacoes):
    """
    Salva a lista de combinações (tabela de preços) em um arquivo JSON.
    """
    dados = {"combinacoes": combinacoes}
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def encontrar_combinacao(combinacoes, acabamento, papel, faca, impressao):
    """
    Procura na lista de combinações uma que tenha exatamente os mesmos valores de acabamento, papel, faca e impressão.
    """
    for comb in combinacoes:
        if (comb.get("acabamento") == acabamento and 
            comb.get("papel") == papel and 
            comb.get("faca") == faca and 
            comb.get("impressao") == impressao):
            return comb
    return None

def obter_opcao(titulo, opcoes):
    """
    Exibe um menu com as opções e retorna o valor descritivo escolhido.
    """
    while True:
        print(titulo)
        for key, descricao in opcoes.items():
            print(f"{key}. {descricao}")
        escolha = input("Digite a sua opção: ").strip()
        if escolha in opcoes:
            return opcoes[escolha]
        else:
            print("Opção inválida, tente novamente.\n")

def main():
    tabela_arquivo = "tabela_precos.json"
    combinacoes = carregar_tabela_precos(tabela_arquivo)

    # Coleta do nome do orçamento
    nome = input("Informe o nome do orçamento: ").strip()

    # Definição das opções para cada categoria  
    # (os textos abaixo devem bater exatamente com os cadastrados no JSON)
    opcoes_acabamento = {
        '1': "Verniz UV Total Frente",
        '2': "Laminação Fosca",
        '3': "Laminação Fosca c/ Verniz Localizado"
    }

    opcoes_papel = {
        '1': "Papel Couchê 250g",
        '2': "Papel Couchê 300g",
        '3': "Papel Supremo 300g",
        '4': "Papel Kraft 240g"
    }

    opcoes_impressao = {
        '1': "Impressão apenas frente",
        '2': "Impressão frente e verso"
    }

    opcoes_faca = {
        '1': "4,25x4,8cm",
        '2': "8,8x4,8cm",
        '3': "9,94x8,8cm"
    }
    
    # Obtenção das escolhas do usuário
    acabamento = obter_opcao("Informe a sua opção desejada (Acabamento):", opcoes_acabamento)
    print()
    papel = obter_opcao("Qual é o seu papel desejado?", opcoes_papel)
    print()
    impressao = obter_opcao("Escolha o tipo de impressão:", opcoes_impressao)
    print()
    faca = obter_opcao("Qual é a sua faca desejada?", opcoes_faca)
    print()
    
    # Exibe o resumo do orçamento
    print(f"\n*{nome}*")
    print(f"- {papel}")
    print(f"- {acabamento}")
    print(f"- {impressao}")
    print()
    
    # Procura pela combinação na tabela de preços usando todos os campos
    combinacao_encontrada = encontrar_combinacao(combinacoes, acabamento, papel, faca, impressao)

    if combinacao_encontrada:
        for quantidade, preco in combinacao_encontrada["precos"].items():
            # Extrai a parte numérica para calcular o preço por unidade
            quantidade_numerica = int(''.join(filter(str.isdigit, quantidade)))
            preco_unitario = preco / quantidade_numerica

             # Formata os valores monetários: apenas os números convertidos para string com duas casas e vírgula.
            preco_total_str = f"R${preco}".replace('.', ',')
            preco_unit_str = f"R${preco_unitario:.2f}".replace('.', ',')

            # Exibe a quantidade sem nenhum caractere extra.
            print(f"{quantidade} {preco_total_str} ({preco_unit_str}/un.)")
    else:
        print("\nNão existe uma tabela de preços cadastrada para essa combinação.")
        resposta = input("Deseja cadastrar uma nova tabela de preços para essa combinação? (s/n): ").lower().strip()
        if resposta == 's':
            nova_tabela = {}
            while True:
                quantidade = input("Informe a quantidade (ex.: 200unid): ").strip()
                preco_str = input("Informe o preço total: ").strip()
                try:
                    preco = float(preco_str)
                except ValueError:
                    print("Preço inválido, tente novamente.\n")
                    continue
                # Converte para inteiro se não houver parte decimal
                if preco.is_integer():
                    preco = int(preco)

                nova_tabela[quantidade] = preco
                mais = input("Deseja adicionar mais uma opção? (s/n): ").lower().strip()
                if mais != 's':
                    break
            nova_combinacao = {
                "acabamento": acabamento,
                "papel": papel,
                "faca": faca,
                "impressao": impressao,
                "precos": nova_tabela
            }
            combinacoes.append(nova_combinacao)
            salvar_tabela_precos(tabela_arquivo, combinacoes)
            print("Nova tabela de preços cadastrada com sucesso!")

if __name__ == "__main__":
    main()
