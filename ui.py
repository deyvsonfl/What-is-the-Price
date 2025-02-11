import tkinter as tk
from tkinter import ttk, messagebox
import json
from db_handler import (
    criar_tabela,
    inserir_combinacao,
    buscar_combinacao,
    listar_combinacoes,
    atualizar_combinacao,
    excluir_combinacao,
)
from config_handler import load_config

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Orçamento com Banco de Dados")
        self.configure(padx=10, pady=10)
        criar_tabela()  # Garante que a tabela existe
        self.opcoes_acabamento = [
            "Verniz UV Total Frente",
            "Laminação Fosca",
            "Laminação Fosca c/ Verniz Localizado",
            "Laminação Fosca c/ Hot Stamping",
        ]
        self.opcoes_papel = [
            "Papel Couchê 250g",
            "Papel Couchê 300g",
            "Papel Supremo 300g",
            "Papel Kraft 240g",
        ]
        self.opcoes_impressao = ["Impressão apenas frente", "Impressão frente e verso"]
        self.opcoes_faca = ["4,25x4,8cm", "8,8x4,8cm", "9,94x8,8cm"]
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Nome do orçamento:").grid(row=0, column=0, sticky="w")
        self.nome_entry = tk.Entry(self, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Acabamento:").grid(row=1, column=0, sticky="w")
        self.acabamento_cb = ttk.Combobox(
            self, values=self.opcoes_acabamento, state="readonly", width=37
        )
        self.acabamento_cb.grid(row=1, column=1, padx=5, pady=5)
        self.acabamento_cb.current(0)

        tk.Label(self, text="Papel:").grid(row=2, column=0, sticky="w")
        self.papel_cb = ttk.Combobox(
            self, values=self.opcoes_papel, state="readonly", width=37
        )
        self.papel_cb.grid(row=2, column=1, padx=5, pady=5)
        self.papel_cb.current(0)

        tk.Label(self, text="Impressão:").grid(row=3, column=0, sticky="w")
        self.impressao_cb = ttk.Combobox(
            self, values=self.opcoes_impressao, state="readonly", width=37
        )
        self.impressao_cb.grid(row=3, column=1, padx=5, pady=5)
        self.impressao_cb.current(0)

        tk.Label(self, text="Faca:").grid(row=4, column=0, sticky="w")
        self.faca_cb = ttk.Combobox(
            self, values=self.opcoes_faca, state="readonly", width=37
        )
        self.faca_cb.grid(row=4, column=1, padx=5, pady=5)
        self.faca_cb.current(0)

        tk.Label(self, text="Número de Furos:").grid(row=5, column=0, sticky="w")
        self.furos_entry = tk.Entry(self, width=10)
        self.furos_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.furos_entry.insert(0, "2")

        tk.Label(self, text="Número de Cortes:").grid(row=6, column=0, sticky="w")
        self.cortes_entry = tk.Entry(self, width=10)
        self.cortes_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        self.cortes_entry.insert(0, "2")

        tk.Label(self, text="Número de Vincos:").grid(row=7, column=0, sticky="w")
        self.vincos_entry = tk.Entry(self, width=10)
        self.vincos_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        self.vincos_entry.insert(0, "2")

        self.consulta_btn = tk.Button(
            self, text="Consultar Preços", command=self.consultar_precos, width=40
        )
        self.consulta_btn.grid(row=8, column=0, columnspan=2, pady=5)

        self.cadastro_btn = tk.Button(
            self,
            text="Cadastrar Nova Combinação",
            command=self.abrir_cadastro,
            width=40,
        )
        self.cadastro_btn.grid(row=9, column=0, columnspan=2, pady=5)

        self.gerenciar_btn = tk.Button(
            self, text="Gerenciar Combinações", command=self.abrir_gerenciar, width=40
        )
        self.gerenciar_btn.grid(row=10, column=0, columnspan=2, pady=5)

        self.config_av_btn = tk.Button(
            self, text="Configurações Avançadas", command=self.abrir_config_avancada, width=40
        )
        self.config_av_btn.grid(row=11, column=0, columnspan=2, pady=5)

        self.result_text = tk.Text(self, width=50, height=10)
        self.result_text.grid(row=12, column=0, columnspan=2, padx=5, pady=5)

    def consultar_precos(self):
        nome = self.nome_entry.get().strip()
        acabamento = self.acabamento_cb.get()
        papel = self.papel_cb.get()
        impressao = self.impressao_cb.get()
        faca = self.faca_cb.get()
        try:
            n_furos = int(self.furos_entry.get())
        except ValueError:
            n_furos = 2
        try:
            n_cortes = int(self.cortes_entry.get())
        except ValueError:
            n_cortes = 2
        try:
            n_vincos = int(self.vincos_entry.get())
        except ValueError:
            n_vincos = 2

        # Carrega as configurações avançadas
        config = load_config()
        extra_furos = max(n_furos - 2, 0) * config.get("custo_furo_adicional", 5.00)
        extra_cortes = max(n_cortes - 2, 0) * config.get("custo_corte_adicional", 6.00)
        extra_vincos = max(n_vincos - 2, 0) * config.get("custo_vinco_adicional", 6.00)
        extra_total = extra_furos + extra_cortes + extra_vincos

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"*{nome}*\n")
        self.result_text.insert(tk.END, f"- {papel}\n")
        self.result_text.insert(tk.END, f"- {acabamento}\n")
        self.result_text.insert(tk.END, f"- {impressao}\n\n")

        comb_id, precos = buscar_combinacao(acabamento, papel, faca, impressao)
        if precos:
            self.result_text.insert(tk.END, "--- Tabela de Preços ---\n")
            for quantidade, preco in precos.items():
                quantidade_numerica = int("".join(filter(str.isdigit, quantidade)))
                final_price = preco + extra_total
                preco_unitario = final_price / quantidade_numerica
                preco_total_str = f"R${final_price:.2f}".replace(".", ",")
                preco_unit_str = f"R${preco_unitario:.2f}".replace(".", ",")
                self.result_text.insert(
                    tk.END, f"{quantidade} {preco_total_str} ({preco_unit_str}/un.)\n"
                )
        else:
            self.result_text.insert(
                tk.END, "\nCombinação não encontrada no banco de dados."
            )
            messagebox.showinfo(
                "Informação",
                "Combinação não encontrada.\nConsidere cadastrar uma nova combinação.",
            )

    def abrir_cadastro(self, modo_edicao=False, comb_id=None):
        cadastro_win = tk.Toplevel(self)
        cadastro_win.title("Editar Combinação" if modo_edicao else "Cadastro de Nova Combinação")
        cadastro_win.configure(padx=10, pady=10)

        tk.Label(cadastro_win, text="Acabamento:").grid(row=0, column=0, sticky="w")
        acabamento_entry = ttk.Combobox(cadastro_win, values=self.opcoes_acabamento, state="readonly", width=30)
        acabamento_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(cadastro_win, text="Papel:").grid(row=1, column=0, sticky="w")
        papel_entry = ttk.Combobox(cadastro_win, values=self.opcoes_papel, state="readonly", width=30)
        papel_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(cadastro_win, text="Impressão:").grid(row=2, column=0, sticky="w")
        impressao_entry = ttk.Combobox(cadastro_win, values=self.opcoes_impressao, state="readonly", width=30)
        impressao_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(cadastro_win, text="Faca:").grid(row=3, column=0, sticky="w")
        faca_entry = ttk.Combobox(cadastro_win, values=self.opcoes_faca, state="readonly", width=30)
        faca_entry.grid(row=3, column=1, padx=5, pady=5)

        precos_dict = {}
        if modo_edicao and comb_id is not None:
            from db_handler import conectar
            import sqlite3
            conn = conectar()
            c = conn.cursor()
            c.execute("SELECT acabamento, papel, faca, impressao, precos FROM combinacoes WHERE id = ?", (comb_id,))
            row = c.fetchone()
            conn.close()
            if row:
                acabamento_entry.set(row[0])
                papel_entry.set(row[1])
                impressao_entry.set(row[3])
                faca_entry.set(row[2])
                precos_dict = json.loads(row[4])
        else:
            acabamento_entry.current(0)
            papel_entry.current(0)
            impressao_entry.current(0)
            faca_entry.current(0)

        tk.Label(cadastro_win, text="Preços (Quantidade: Preço Total):").grid(row=4, column=0, columnspan=2, pady=(10, 0))
        precos_frame = tk.Frame(cadastro_win)
        precos_frame.grid(row=5, column=0, columnspan=2, pady=5)
        preco_rows = []

        def adicionar_linha(default_quantidade="", default_preco=""):
            row = len(preco_rows)
            quantidade_entry = tk.Entry(precos_frame, width=12)
            quantidade_entry.grid(row=row, column=0, padx=5, pady=2)
            quantidade_entry.insert(0, default_quantidade)
            preco_entry = tk.Entry(precos_frame, width=12)
            preco_entry.grid(row=row, column=1, padx=5, pady=2)
            preco_entry.insert(0, default_preco)
            btn_remove = None
            if row > 0:
                btn_remove = tk.Button(precos_frame, text="Remover")
                btn_remove.grid(row=row, column=2, padx=5, pady=2)
                btn_remove.config(
                    command=lambda q=quantidade_entry, p=preco_entry, b=btn_remove: remover_linha((q, p, b))
                )
            preco_rows.append((quantidade_entry, preco_entry, btn_remove))

        def remover_linha(item):
            if item in preco_rows:
                item[0].destroy()
                item[1].destroy()
                if item[2]:
                    item[2].destroy()
                preco_rows.remove(item)
                for idx, (q_entry, p_entry, btn) in enumerate(preco_rows):
                    q_entry.grid_configure(row=idx)
                    p_entry.grid_configure(row=idx)
                    if btn:
                        btn.grid_configure(row=idx)

        btn_add_linha = tk.Button(cadastro_win, text="Adicionar Linha", command=adicionar_linha)
        btn_add_linha.grid(row=6, column=0, columnspan=2, pady=5)
        if modo_edicao and comb_id is not None and precos_dict:
            for quantidade, preco in precos_dict.items():
                adicionar_linha(quantidade, str(preco))
        else:
            adicionar_linha()

        def salvar_combinacao():
            novo_acabamento = acabamento_entry.get()
            novo_papel = papel_entry.get()
            nova_impressao = impressao_entry.get()
            nova_faca = faca_entry.get()
            nova_tabela = {}
            for quantidade_entry, preco_entry, _ in preco_rows:
                quantidade = quantidade_entry.get().strip()
                preco_str = preco_entry.get().strip()
                if not quantidade or not preco_str:
                    continue
                try:
                    preco_valor = float(preco_str)
                except ValueError:
                    messagebox.showerror("Erro", f"Preço inválido para {quantidade}.")
                    return
                if preco_valor.is_integer():
                    preco_valor = int(preco_valor)
                nova_tabela[quantidade] = preco_valor
            if not nova_tabela:
                messagebox.showerror("Erro", "Cadastre pelo menos uma linha de preço.")
                return
            from db_handler import inserir_combinacao, atualizar_combinacao
            if modo_edicao and comb_id is not None:
                atualizar_combinacao(
                    comb_id,
                    novo_acabamento,
                    novo_papel,
                    nova_faca,
                    nova_impressao,
                    nova_tabela,
                )
            else:
                inserir_combinacao(novo_acabamento, novo_papel, nova_faca, nova_impressao, nova_tabela)
            messagebox.showinfo("Sucesso", "Combinação salva com sucesso!")
            cadastro_win.destroy()

        btn_salvar = tk.Button(cadastro_win, text="Salvar", command=salvar_combinacao, width=30)
        btn_salvar.grid(row=7, column=0, columnspan=2, pady=10)

    def abrir_gerenciar(self):
        gerenciar_win = tk.Toplevel(self)
        gerenciar_win.title("Gerenciar Combinações")
        gerenciar_win.configure(padx=10, pady=10)
        tree = ttk.Treeview(
            gerenciar_win,
            columns=("acabamento", "papel", "faca", "impressao"),
            show="headings",
            height=10,
        )
        tree.heading("acabamento", text="Acabamento")
        tree.heading("papel", text="Papel")
        tree.heading("faca", text="Faca")
        tree.heading("impressao", text="Impressão")
        tree.column("acabamento", width=150)
        tree.column("papel", width=150)
        tree.column("faca", width=100)
        tree.column("impressao", width=150)
        tree.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        id_para_comb = {}
        comb_list = listar_combinacoes()
        for comb in comb_list:
            comb_id = comb[0]
            values = (comb[1], comb[2], comb[3], comb[4])
            item_id = tree.insert("", "end", values=values)
            id_para_comb[item_id] = comb_id

        def editar_selecionado():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Atenção", "Selecione uma combinação para editar.")
                return
            comb_id = id_para_comb.get(selected[0])
            self.abrir_cadastro(modo_edicao=True, comb_id=comb_id)
            gerenciar_win.destroy()

        def excluir_selecionado():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Atenção", "Selecione uma combinação para excluir.")
                return
            comb_id = id_para_comb.get(selected[0])
            if messagebox.askyesno("Confirmação", "Deseja realmente excluir essa combinação?"):
                excluir_combinacao(comb_id)
                messagebox.showinfo("Sucesso", "Combinação excluída com sucesso!")
                gerenciar_win.destroy()

        btn_editar = tk.Button(gerenciar_win, text="Editar", command=editar_selecionado, width=20)
        btn_editar.grid(row=1, column=0, padx=5, pady=5)
        btn_excluir = tk.Button(gerenciar_win, text="Excluir", command=excluir_selecionado, width=20)
        btn_excluir.grid(row=1, column=1, padx=5, pady=5)

    def abrir_config_avancada(self):
        from config_ui import AdvancedConfigUI
        config_win = AdvancedConfigUI(self)
        self.wait_window(config_win)


if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()
