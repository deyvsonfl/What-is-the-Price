import tkinter as tk
from tkinter import messagebox
import config_handler

class AdvancedConfigUI(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Configuração Avançada")
        self.configure(padx=10, pady=10)
        self.config_data = config_handler.load_config()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Custo Furo Adicional (R$):").grid(row=0, column=0, sticky="w")
        self.furo_entry = tk.Entry(self, width=10)
        self.furo_entry.grid(row=0, column=1, padx=5, pady=5)
        self.furo_entry.insert(0, str(self.config_data.get("custo_furo_adicional", 5.00)))

        tk.Label(self, text="Custo Corte Adicional (R$):").grid(row=1, column=0, sticky="w")
        self.corte_entry = tk.Entry(self, width=10)
        self.corte_entry.grid(row=1, column=1, padx=5, pady=5)
        self.corte_entry.insert(0, str(self.config_data.get("custo_corte_adicional", 6.00)))

        tk.Label(self, text="Custo Vinco Adicional (R$):").grid(row=2, column=0, sticky="w")
        self.vinco_entry = tk.Entry(self, width=10)
        self.vinco_entry.grid(row=2, column=1, padx=5, pady=5)
        self.vinco_entry.insert(0, str(self.config_data.get("custo_vinco_adicional", 6.00)))

        btn_save = tk.Button(self, text="Salvar Configurações", command=self.save_config)
        btn_save.grid(row=3, column=0, columnspan=2, pady=10)

    def save_config(self):
        try:
            custo_furo = float(self.furo_entry.get())
            custo_corte = float(self.corte_entry.get())
            custo_vinco = float(self.vinco_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
            return

        self.config_data["custo_furo_adicional"] = custo_furo
        self.config_data["custo_corte_adicional"] = custo_corte
        self.config_data["custo_vinco_adicional"] = custo_vinco
        config_handler.save_config(self.config_data)
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        self.destroy()
