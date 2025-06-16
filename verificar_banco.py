import sqlite3
import os

def verificar_banco():
    # Confirmar que estamos no diretório correto
    print(f"Diretório atual: {os.getcwd()}")
    
    # Verificar se o arquivo do banco existe
    if not os.path.exists('banco.db'):
        print("Arquivo do banco de dados 'banco.db' não encontrado!")
        return
    
    # Conectar ao banco de dados
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Verificar a estrutura da tabela clientes
    print("\n=== ESTRUTURA DA TABELA CLIENTES ===")
    try:
        cursor.execute("PRAGMA table_info(clientes)")
        colunas = cursor.fetchall()
        for coluna in colunas:
            print(f"Coluna: {coluna['name']}, Tipo: {coluna['type']}")
    except sqlite3.Error as e:
        print(f"Erro ao verificar estrutura da tabela: {e}")
    
    # Listar os clientes e seus endereços
    print("\n=== DADOS DOS CLIENTES ===")
    try:
        cursor.execute("SELECT id, nome, telefone, email, endereco FROM clientes")
        clientes = cursor.fetchall()
        
        if not clientes:
            print("Nenhum cliente encontrado na base de dados.")
        else:
            for cliente in clientes:
                print(f"\nID: {cliente['id']}")
                print(f"Nome: {cliente['nome']}")
                print(f"Telefone: {cliente['telefone']}")
                print(f"Email: {cliente['email']}")
                print(f"Endereço: {cliente['endereco']}")
    except sqlite3.Error as e:
        print(f"Erro ao consultar clientes: {e}")
    
    # Fechar a conexão
    conn.close()

if __name__ == "__main__":
    verificar_banco()
