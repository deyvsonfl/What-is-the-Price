import tkinter as tk
from tkinter import ttk, messagebox
from data_handler import carregar_tabela_precos, salvar_tabela_precos, encontrar_combinacao

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

        # Linha 1: Acabamento
        tk.Label(self, text="Acabamento:").grid(row=1, column=0, sticky="w")
        self.opcoes_acabamento = [
            "Verniz UV Total Frente",
            "Laminação Fosca",
            "Laminação Fosca c/ Verniz Localizado"
        ]
        self.acabamento_cb = ttk.Combobox(self, values=self.opcoes_acabamento, state="readonly", width=37)
        self.acabamento_cb.grid(row=1, column=1, padx=5, pady=5)
        self.acabamento_cb.current(0)

        # Linha 2: Papel
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

        # Linha 3: Impressão
        tk.Label(self, text="Impressão:").grid(row=3, column=0, sticky="w")
        self.opcoes_impressao = [
            "Impressão apenas frente",
            "Impressão frente e verso"
        ]
        self.impressao_cb = ttk.Combobox(self, values=self.opcoes_impressao, state="readonly", width=37)
        self.impressao_cb.grid(row=3, column=1, padx=5, pady=5)
        self.impressao_cb.current(0)

        # Linha 4: Faca
        tk.Label(self, text="Faca:").grid(row=4, column=0, sticky="w")
        self.opcoes_faca = [
            "4,25x4,8cm",
            "8,8x4,8cm",
            "9,94x8,8cm"
        ]
        self.faca_cb = ttk.Combobox(self, values=self.opcoes_faca, state="readonly", width=37)
        self.faca_cb.grid(row=4, column=1, padx=5, pady=5)
        self.faca_cb.current(0)

        # Linha 5: Botão Consultar Preços
        self.consulta_btn = tk.Button(self, text="Consultar Preços", command=self.consultar_precos, width=40)
        self.consulta_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # Linha 6: Botão Cadastrar Nova Combinação
        self.cadastro_btn = tk.Button(self, text="Cadastrar Nova Combinação", command=self.abrir_cadastro_nova_combinacao, width=40)
        self.cadastro_btn.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Linha 7: Botão Gerenciar Combinações (Editar/Excluir)
        self.gerenciar_btn = tk.Button(self, text="Gerenciar Combinações", command=self.abrir_gerenciar_combinacoes, width=40)
        self.gerenciar_btn.grid(row=7, column=0, columnspan=2, pady=5)

        # Linha 8: Área de Resultados
        self.result_text = tk.Text(self, width=50, height=10)
        self.result_text.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
    
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
            self.result_text.insert(tk.END, "--- Tabela de Preços ---\n")
            for quantidade, preco in combinacao_encontrada["precos"].items():
                quantidade_numerica = int(''.join(filter(str.isdigit, quantidade)))
                preco_unitario = preco / quantidade_numerica
                preco_total_str = f"R${preco}"
                preco_unit_str = f"R${preco_unitario:.2f}".replace('.', ',')
                self.result_text.insert(tk.END, f"{quantidade} {preco_total_str} ({preco_unit_str}/un.)\n")
        else:
            self.result_text.insert(tk.END, "\nNão existe uma tabela de preços cadastrada para essa combinação.")
            messagebox.showinfo("Informação", "Combinação não encontrada.\nConsidere cadastrar uma nova tabela de preços.")

    def abrir_cadastro_nova_combinacao(self, modo_edicao=False, comb_index=None):
        """
        Se modo_edicao=True, preenche os campos com os dados da combinação em comb_index para edição.
        Caso contrário, funciona como cadastro de nova combinação.
        """
        cadastro_win = tk.Toplevel(self)
        titulo = "Editar Combinação" if modo_edicao else "Cadastro de Nova Combinação"
        cadastro_win.title(titulo)
        cadastro_win.configure(padx=10, pady=10)
        
        # Campos para os parâmetros
        tk.Label(cadastro_win, text="Acabamento:").grid(row=0, column=0, sticky="w")
        acabamento_cb = ttk.Combobox(cadastro_win, values=self.opcoes_acabamento, state="readonly", width=30)
        acabamento_cb.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(cadastro_win, text="Papel:").grid(row=1, column=0, sticky="w")
        papel_cb = ttk.Combobox(cadastro_win, values=self.opcoes_papel, state="readonly", width=30)
        papel_cb.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(cadastro_win, text="Impressão:").grid(row=2, column=0, sticky="w")
        impressao_cb = ttk.Combobox(cadastro_win, values=self.opcoes_impressao, state="readonly", width=30)
        impressao_cb.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(cadastro_win, text="Faca:").grid(row=3, column=0, sticky="w")
        faca_cb = ttk.Combobox(cadastro_win, values=self.opcoes_faca, state="readonly", width=30)
        faca_cb.grid(row=3, column=1, padx=5, pady=5)
        
        # Define valores padrão se estiver em modo de edição
        if modo_edicao and comb_index is not None:
            comb = self.combinacoes[comb_index]
            acabamento_cb.set(comb.get("acabamento"))
            papel_cb.set(comb.get("papel"))
            impressao_cb.set(comb.get("impressao"))
            faca_cb.set(comb.get("faca"))
        else:
            acabamento_cb.current(0)
            papel_cb.current(0)
            impressao_cb.current(0)
            faca_cb.current(0)
        
        # Área para cadastro de preços (quantidade e preço)
        tk.Label(cadastro_win, text="Preços (Quantidade e Preço Total):").grid(row=4, column=0, columnspan=2, pady=(10,0))
        
        precos_frame = tk.Frame(cadastro_win)
        precos_frame.grid(row=5, column=0, columnspan=2, pady=5)
        preco_rows = []
        
        def adicionar_linha():
            row = len(preco_rows)
            quantidade_entry = tk.Entry(precos_frame, width=12)
            quantidade_entry.grid(row=row, column=0, padx=5, pady=2)
            preco_entry = tk.Entry(precos_frame, width=12)
            preco_entry.grid(row=row, column=1, padx=5, pady=2)
            preco_rows.append((quantidade_entry, preco_entry))
        
        btn_add_linha = tk.Button(cadastro_win, text="Adicionar Linha", command=adicionar_linha)
        btn_add_linha.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Se estiver editando, preenche as linhas de preços
        if modo_edicao and comb_index is not None:
            comb = self.combinacoes[comb_index]
            for quantidade, preco in comb.get("precos", {}).items():
                row = len(preco_rows)
                quantidade_entry = tk.Entry(precos_frame, width=12)
                quantidade_entry.insert(0, quantidade)
                quantidade_entry.grid(row=row, column=0, padx=5, pady=2)
                preco_entry = tk.Entry(precos_frame, width=12)
                preco_entry.insert(0, str(preco))
                preco_entry.grid(row=row, column=1, padx=5, pady=2)
                preco_rows.append((quantidade_entry, preco_entry))
        else:
            adicionar_linha()
        
        def salvar_combinacao():
            novo_acabamento = acabamento_cb.get()
            novo_papel = papel_cb.get()
            nova_impressao = impressao_cb.get()
            nova_faca = faca_cb.get()
            nova_tabela = {}
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
            if modo_edicao and comb_index is not None:
                self.combinacoes[comb_index] = nova_combinacao
            else:
                self.combinacoes.append(nova_combinacao)
            salvar_tabela_precos(self.tabela_arquivo, self.combinacoes)
            messagebox.showinfo("Sucesso", "Tabela de preços cadastrada com sucesso!")
            cadastro_win.destroy()
        
        btn_salvar = tk.Button(cadastro_win, text="Salvar", command=salvar_combinacao, width=30)
        btn_salvar.grid(row=7, column=0, columnspan=2, pady=10)
    
    def abrir_gerenciar_combinacoes(self):
        gerenciar_win = tk.Toplevel(self)
        gerenciar_win.title("Gerenciar Combinações")
        gerenciar_win.configure(padx=10, pady=10)
        
        # Treeview para listar combinações
        colunas = ("acabamento", "papel", "faca", "impressao")
        tree = ttk.Treeview(gerenciar_win, columns=colunas, show="headings", height=8)
        for col in colunas:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=130)
        tree.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        # Mapeia o id do item para o índice na lista de combinações
        id_para_indice = {}
        for idx, comb in enumerate(self.combinacoes):
            item_id = tree.insert("", "end", values=(comb.get("acabamento"), comb.get("papel"), comb.get("faca"), comb.get("impressao")))
            id_para_indice[item_id] = idx
        
        def editar_selecionado():
            item_id = tree.selection()
            if not item_id:
                messagebox.showwarning("Atenção", "Selecione uma combinação para editar.")
                return
            idx = id_para_indice.get(item_id[0])
            self.abrir_cadastro_nova_combinacao(modo_edicao=True, comb_index=idx)
            gerenciar_win.destroy()
        
        def excluir_selecionado():
            item_id = tree.selection()
            if not item_id:
                messagebox.showwarning("Atenção", "Selecione uma combinação para excluir.")
                return
            idx = id_para_indice.get(item_id[0])
            resposta = messagebox.askyesno("Confirmação", "Deseja realmente excluir essa combinação?")
            if resposta:
                del self.combinacoes[idx]
                salvar_tabela_precos(self.tabela_arquivo, self.combinacoes)
                messagebox.showinfo("Sucesso", "Combinação excluída com sucesso!")
                gerenciar_win.destroy()
        
        btn_editar = tk.Button(gerenciar_win, text="Editar", command=editar_selecionado, width=20)
        btn_editar.grid(row=1, column=0, padx=5, pady=5)
        
        btn_excluir = tk.Button(gerenciar_win, text="Excluir", command=excluir_selecionado, width=20)
        btn_excluir.grid(row=1, column=1, padx=5, pady=5)

