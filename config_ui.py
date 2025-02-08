import tkinter as tk
from tkinter import messagebox
import json
import os

CONFIG_FILE = "config.json"

def carregar_config(arquivo=CONFIG_FILE):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Configuração padrão
        return {
            "acabamento": ["Verniz UV Total Frente", "Laminação Fosca", "Laminação Fosca c/ Verniz Localizado"],
            "papel": ["Papel Couchê 250g", "Papel Couchê 300g", "Papel Supremo 300g", "Papel Kraft 240g"],
            "impressao": ["Impressão apenas frente", "Impressão frente e verso"],
            "faca": ["4,25x4,8cm", "8,8x4,8cm", "9,94x8,8cm"]
        }

def salvar_config(config, arquivo=CONFIG_FILE):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

class ConfigurationUI(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Configuração das Opções")
        self.configure(padx=10, pady=10)
        self.config_data = carregar_config()
        self.create_widgets()
    
    def create_widgets(self):
        self.frames = {}
        categories = ["acabamento", "papel", "impressao", "faca"]
        row = 0
        for cat in categories:
            frame = tk.LabelFrame(self, text=cat.capitalize(), padx=5, pady=5)
            frame.grid(row=row, column=0, padx=5, pady=5, sticky="nsew")
            self.frames[cat] = frame
            row += 1
        
        self.listboxes = {}
        for cat, frame in self.frames.items():
            lb = tk.Listbox(frame, width=40, height=4)
            lb.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
            for option in self.config_data.get(cat, []):
                lb.insert(tk.END, option)
            self.listboxes[cat] = lb
            
            entry = tk.Entry(frame, width=30)
            entry.grid(row=1, column=0, padx=5, pady=2)
            setattr(self, f"{cat}_entry", entry)
            
            btn_add = tk.Button(frame, text="Adicionar", command=lambda c=cat: self.adicionar_opcao(c))
            btn_add.grid(row=1, column=1, padx=5, pady=2)
            
            btn_remove = tk.Button(frame, text="Remover", command=lambda c=cat: self.remover_opcao(c))
            btn_remove.grid(row=2, column=0, columnspan=2, padx=5, pady=2)
        
        btn_save = tk.Button(self, text="Salvar Configurações", command=self.salvar_configuracoes, width=30)
        btn_save.grid(row=row, column=0, pady=10)
    
    def adicionar_opcao(self, categoria):
        entry = getattr(self, f"{categoria}_entry")
        nova_opcao = entry.get().strip()
        if nova_opcao:
            lb = self.listboxes[categoria]
            lb.insert(tk.END, nova_opcao)
            entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Digite uma opção válida.")
    
    def remover_opcao(self, categoria):
        lb = self.listboxes[categoria]
        selected = lb.curselection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma opção para remover.")
            return
        for index in reversed(selected):
            lb.delete(index)
    
    def salvar_configuracoes(self):
        nova_config = {}
        for cat, lb in self.listboxes.items():
            nova_config[cat] = list(lb.get(0, tk.END))
        salvar_config(nova_config)
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        self.destroy()
