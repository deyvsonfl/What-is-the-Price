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
        # Nome do orçamento
        tk.Label(self, text="Nome do orçamento:").grid(row=0, column=0, sticky="w")
        self.nome_entry = tk.Entry(self, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        # Acabamento
        tk.Label(self, text="Acabamento:").grid(row=1, column=0, sticky="w")
        self.opcoes_acabamento = [
            "Verniz UV Total Frente",
            "Laminação Fosca",
            "Laminação Fosca c/ Verniz Localizado"
        ]
        self.acabamento_cb = ttk.Combobox(self, values=self.opcoes_acabamento, state="readonly", width=37)
        self.acabamento_cb.grid(row=1, column=1, padx=5, pady=5)
        self.acabamento_cb.current(0)

        # Papel
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

        # Impressão
        tk.Label(self, text="Impressão:").grid(row=3, column=0, sticky="w")
        self.opcoes_impressao = [
            "Impressão apenas frente",
            "Impressão frente e verso"
        ]
        self.impressao_cb = ttk.Combobox(self, values=self.opcoes_impressao, state="readonly", width=37)
        self.impressao_cb.grid(row=3, column=1, padx=5, pady=5)
        self.impressao_cb.current(0)

        # Faca
        tk.Label(self, text="Faca:").grid(row=4, column=0, sticky="w")
        self.opcoes_faca = [
            "4,25x4,8cm",
            "8,8x4,8cm",
            "9,94x8,8cm"
        ]
        self.faca_cb = ttk.Combobox(self, values=self.opcoes_faca, state="readonly", width=37)
        self.faca_cb.grid(row=4, column=1, padx=5, pady=5)
        self.faca_cb.current(0)

        # Botão Consultar Preços
        self.consulta_btn = tk.Button(self, text="Consultar Preços", command=self.consultar_precos, width=40)
        self.consulta_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # Botão Cadastrar Nova Combinação
        self.cadastro_btn = tk.Button(self, text="Cadastrar Nova Combinação", command=self.abrir_cadastro_nova_combinacao, width=40)
        self.cadastro_btn.grid(row=6, column=0, columnspan=2, pady=5)

        # Área de resultados
        self.result_text = tk.Text(self, width=50, height=10)
        self.result_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
    
    def consultar_precos(self):
        nome = self.nome_entry.get().strip()
        acabamento = self.acabamento_cb.get()
        papel = self.papel_cb.get()
        impressao = self.impressao_cb.get()
        faca = self.faca_cb.get()

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"*{nome}*\n")
        self.result_text.insert(tk.END, f"- {papel}\n")
        self.result_text.insert(tk.END, f"- {acabamento}\n")
        self.result_text.insert(tk.END, f"- {impressao}\n\n")

        combinacao_encontrada = encontrar_combinacao(self.combinacoes, acabamento, papel, faca, impressao)
        if combinacao_encontrada:
            for quantidade, preco in combinacao_encontrada["precos"].items():
                quantidade_numerica = int(''.join(filter(str.isdigit, quantidade)))
                preco_unitario = preco / quantidade_numerica
                preco_total_str = f"R${preco}"
                preco_unit_str = f"R${preco_unitario:.2f}".replace('.', ',')
                self.result_text.insert(tk.END, f"{quantidade} {preco_total_str} ({preco_unit_str}/un.)\n")
        else:
            self.result_text.insert(tk.END, "\nNão existe uma tabela de preços cadastrada para essa combinação.")
            messagebox.showinfo("Informação", "Combinação não encontrada.\nConsidere cadastrar uma nova tabela de preços.")

    def abrir_cadastro_nova_combinacao(self):
        # Cria uma nova janela para cadastro da nova combinação
        cadastro_win = tk.Toplevel(self)
        cadastro_win.title("Cadastro de Nova Combinação")
        cadastro_win.configure(padx=10, pady=10)
        
        # Campos para os parâmetros (utilizando Combobox para padronizar os valores)
        tk.Label(cadastro_win, text="Acabamento:").grid(row=0, column=0, sticky="w")
        acabamento_cb = ttk.Combobox(cadastro_win, values=self.opcoes_acabamento, state="readonly", width=30)
        acabamento_cb.grid(row=0, column=1, padx=5, pady=5)
        acabamento_cb.current(0)
        
        tk.Label(cadastro_win, text="Papel:").grid(row=1, column=0, sticky="w")
        papel_cb = ttk.Combobox(cadastro_win, values=self.opcoes_papel, state="readonly", width=30)
        papel_cb.grid(row=1, column=1, padx=5, pady=5)
        papel_cb.current(0)
        
        tk.Label(cadastro_win, text="Impressão:").grid(row=2, column=0, sticky="w")
        impressao_cb = ttk.Combobox(cadastro_win, values=self.opcoes_impressao, state="readonly", width=30)
        impressao_cb.grid(row=2, column=1, padx=5, pady=5)
        impressao_cb.current(0)
        
        tk.Label(cadastro_win, text="Faca:").grid(row=3, column=0, sticky="w")
        faca_cb = ttk.Combobox(cadastro_win, values=self.opcoes_faca, state="readonly", width=30)
        faca_cb.grid(row=3, column=1, padx=5, pady=5)
        faca_cb.current(0)
        
        # Área de cadastro de preços (quantidade e preço)
        tk.Label(cadastro_win, text="Preços (Quantidade e Preço Total):").grid(row=4, column=0, columnspan=2, pady=(10,0))
        
        # Frame para os campos dinâmicos de preços
        precos_frame = tk.Frame(cadastro_win)
        precos_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Lista para armazenar as linhas (cada linha será uma tupla de Entry widgets)
        preco_rows = []
        
        def adicionar_linha():
            row = len(preco_rows)
            # Entrada para quantidade
            quantidade_entry = tk.Entry(precos_frame, width=12)
            quantidade_entry.grid(row=row, column=0, padx=5, pady=2)
            # Entrada para preço
            preco_entry = tk.Entry(precos_frame, width=12)
            preco_entry.grid(row=row, column=1, padx=5, pady=2)
            preco_rows.append((quantidade_entry, preco_entry))
        
        # Botão para adicionar nova linha
        btn_add_linha = tk.Button(cadastro_win, text="Adicionar Linha", command=adicionar_linha)
        btn_add_linha.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Adiciona uma linha inicial
        adicionar_linha()
        
        def salvar_nova_combinacao():
            novo_acabamento = acabamento_cb.get()
            novo_papel = papel_cb.get()
            nova_impressao = impressao_cb.get()
            nova_faca = faca_cb.get()
            nova_tabela = {}
            # Percorre as linhas de preços cadastrados
            for quantidade_entry, preco_entry in preco_rows:
                quantidade = quantidade_entry.get().strip().replace('.', '')
                preco_str = preco_entry.get().strip()
                if not quantidade or not preco_str:
                    continue
                try:
                    preco_valor = float(preco_str)
                except ValueError:
                    messagebox.showerror("Erro", f"Preço inválido para a quantidade {quantidade}.")
                    return
                # Converte para inteiro se não houver parte decimal
                if preco_valor.is_integer():
                    preco_valor = int(preco_valor)
                nova_tabela[quantidade] = preco_valor
            if not nova_tabela:
                messagebox.showerror("Erro", "Cadastre pelo menos uma linha de preço.")
                return
            nova_combinacao = {
                "acabamento": novo_acabamento,
                "papel": novo_papel,
                "faca": nova_faca,
                "impressao": nova_impressao,
                "precos": nova_tabela
            }
            self.combinacoes.append(nova_combinacao)
            salvar_tabela_precos(self.tabela_arquivo, self.combinacoes)
            messagebox.showinfo("Sucesso", "Nova tabela de preços cadastrada com sucesso!")
            cadastro_win.destroy()
        
        # Botão para salvar a nova combinação
        btn_salvar = tk.Button(cadastro_win, text="Salvar Nova Combinação", command=salvar_nova_combinacao, width=30)
        btn_salvar.grid(row=7, column=0, columnspan=2, pady=10)
        
if __name__ == "__main__":
    tabela_arquivo = "tabela_precos.json"
    app = BudgetApp(tabela_arquivo)
    app.mainloop()
