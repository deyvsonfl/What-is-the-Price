import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

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

class BudgetApp(tk.Tk):
    def __init__(self, tabela_arquivo):
        super().__init__()
        self.title("Sistema de Orçamento")
        self.tabela_arquivo = tabela_arquivo
        self.combinacoes = carregar_tabela_precos(tabela_arquivo)
        self.configure(padx=10, pady=10)
        self.create_widgets()
    
    def create_widgets(self):
        # Linha 0: Nome do orçamento
        tk.Label(self, text="Nome do orçamento:").grid(row=0, column=0, sticky="w")
        self.nome_entry = tk.Entry(self, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        # Linha 1: Opção Acabamento
        tk.Label(self, text="Acabamento:").grid(row=1, column=0, sticky="w")
        self.opcoes_acabamento = [
            "Verniz UV Total Frente",
            "Laminação Fosca",
            "Laminação Fosca c/ Verniz Localizado"
        ]
        self.acabamento_cb = ttk.Combobox(self, values=self.opcoes_acabamento, state="readonly", width=37)
        self.acabamento_cb.grid(row=1, column=1, padx=5, pady=5)
        self.acabamento_cb.current(0)

        # Linha 2: Opção Papel
        tk.Label(self, text="Papel:").grid(row=2, column=0, sticky="w")
        self.opcoes_papel = [
            "Papel Couchê 250g",
            "Papel Couchê 300g",
            "Papel Supremo 300g",
            "Papel Kraft 240g"
        ]
        self.papel_cb = ttk.Combobox(self, values=self.opcoes_papel, state="readonly", width=37)
        self.papel_cb.grid(row=2, column=1, padx=5, pady=5)
        self.papel_cb.current(0)

        # Linha 3: Opção Impressão
        tk.Label(self, text="Impressão:").grid(row=3, column=0, sticky="w")
        self.opcoes_impressao = [
            "Impressão apenas frente",
            "Impressão frente e verso"
        ]
        self.impressao_cb = ttk.Combobox(self, values=self.opcoes_impressao, state="readonly", width=37)
        self.impressao_cb.grid(row=3, column=1, padx=5, pady=5)
        self.impressao_cb.current(0)

        # Linha 4: Opção Faca
        tk.Label(self, text="Faca:").grid(row=4, column=0, sticky="w")
        self.opcoes_faca = [
            "4,25x4,8cm",
            "8,8x4,8cm",
            "9,94x8,8cm"
        ]
        self.faca_cb = ttk.Combobox(self, values=self.opcoes_faca, state="readonly", width=37)
        self.faca_cb.grid(row=4, column=1, padx=5, pady=5)
        self.faca_cb.current(0)

        # Linha 5: Botão de Consulta
        self.consulta_btn = tk.Button(self, text="Consultar Preços", command=self.consultar_precos, width=40)
        self.consulta_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # Linha 6: Área de Resultados
        self.result_text = tk.Text(self, width=50, height=10)
        self.result_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
    
    def consultar_precos(self):
        # Recupera os valores das entradas
        nome = self.nome_entry.get().strip()
        acabamento = self.acabamento_cb.get()
        papel = self.papel_cb.get()
        impressao = self.impressao_cb.get()
        faca = self.faca_cb.get()

        # Limpa a área de resultados
        self.result_text.delete(1.0, tk.END)

        # Exibe o resumo do orçamento
        self.result_text.insert(tk.END, f"*{nome}*\n")
        self.result_text.insert(tk.END, f"- {papel}\n")
        self.result_text.insert(tk.END, f"- {acabamento}\n")
        self.result_text.insert(tk.END, f"- {impressao}\n\n")

        # Procura a combinação na tabela
        combinacao_encontrada = encontrar_combinacao(self.combinacoes, acabamento, papel, faca, impressao)
        if combinacao_encontrada:
            for quantidade, preco in combinacao_encontrada["precos"].items():
                # Extrai os dígitos para calcular o preço por unidade
                quantidade_numerica = int(''.join(filter(str.isdigit, quantidade)))
                preco_unitario = preco / quantidade_numerica

                # Formata os valores monetários (apenas o preço, não a quantidade)
                preco_total_str = f"R${preco:.2f}".replace('.', ',')
                preco_unit_str = f"R${preco_unitario:.2f}".replace('.', ',')

                # Exibe a linha de preço sem ":" após a quantidade
                self.result_text.insert(tk.END, f"{quantidade} {preco_total_str} ({preco_unit_str}/un.)\n")
        else:
            self.result_text.insert(tk.END, "\nNão existe uma tabela de preços cadastrada para essa combinação.")
            messagebox.showinfo("Informação", "Combinação não encontrada.\nConsidere cadastrar uma nova tabela de preços.")

if __name__ == "__main__":
    tabela_arquivo = "tabela_precos.json"
    app = BudgetApp(tabela_arquivo)
    app.mainloop()
