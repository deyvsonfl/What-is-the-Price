import sqlite3
import json

DATABASE_FILE = 'orcamento.db'

def conectar():
    """Retorna uma conexão com o banco de dados SQLite."""
    return sqlite3.connect(DATABASE_FILE)

def criar_tabela():
    """Cria a tabela de combinações se ela não existir."""
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS combinacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acabamento TEXT NOT NULL,
            papel TEXT NOT NULL,
            faca TEXT NOT NULL,
            impressao TEXT NOT NULL,
            precos TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def inserir_combinacao(acabamento, papel, faca, impressao, precos):
    """
    Insere uma nova combinação no banco.
    O parâmetro `precos` é um dicionário que será convertido para JSON.
    """
    precos_str = json.dumps(precos)
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        INSERT INTO combinacoes (acabamento, papel, faca, impressao, precos)
        VALUES (?, ?, ?, ?, ?)
    """, (acabamento, papel, faca, impressao, precos_str))
    conn.commit()
    conn.close()

def buscar_combinacao(acabamento, papel, faca, impressao):
    """
    Busca uma combinação com os parâmetros informados.
    Retorna uma tupla (comb_id, precos) se encontrada ou (None, None).
    """
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        SELECT id, precos FROM combinacoes
        WHERE acabamento = ? AND papel = ? AND faca = ? AND impressao = ?
    """, (acabamento, papel, faca, impressao))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0], json.loads(row[1])
    return None, None

def atualizar_combinacao(comb_id, acabamento, papel, faca, impressao, precos):
    """Atualiza uma combinação existente com o ID fornecido."""
    precos_str = json.dumps(precos)
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        UPDATE combinacoes
        SET acabamento = ?, papel = ?, faca = ?, impressao = ?, precos = ?
        WHERE id = ?
    """, (acabamento, papel, faca, impressao, precos_str, comb_id))
    conn.commit()
    conn.close()

def excluir_combinacao(comb_id):
    """Exclui a combinação com o ID fornecido."""
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM combinacoes WHERE id = ?", (comb_id,))
    conn.commit()
    conn.close()

def listar_combinacoes():
    """
    Retorna uma lista de todas as combinações cadastradas.
    Cada item é uma tupla: (id, acabamento, papel, faca, impressao, precos)
    """
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id, acabamento, papel, faca, impressao, precos FROM combinacoes")
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    criar_tabela()
    print("Tabela criada com sucesso!")
