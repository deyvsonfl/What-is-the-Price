from ui import BudgetApp

if __name__ == "__main__":
    app = BudgetApp()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("Aplicação interrompida pelo usuário.")
