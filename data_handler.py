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
