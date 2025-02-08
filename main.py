from ui import BudgetApp

if __name__ == "__main__":
    tabela_arquivo = "tabela_precos.json"
    app = BudgetApp(tabela_arquivo)
    app.mainloop()
