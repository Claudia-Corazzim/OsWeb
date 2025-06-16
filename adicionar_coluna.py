import sqlite3

def adicionar_coluna_valor_instalado():
    """Adiciona a coluna valor_instalado à tabela pecas"""
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    
    try:
        # Verificar se a coluna já existe
        cursor.execute("PRAGMA table_info(pecas)")
        colunas = [col[1] for col in cursor.fetchall()]
        
        if 'valor_instalado' not in colunas:
            # Adicionar a coluna
            cursor.execute("ALTER TABLE pecas ADD COLUMN valor_instalado REAL")
            conn.commit()
            print("Coluna valor_instalado adicionada com sucesso!")
        else:
            print("A coluna valor_instalado já existe na tabela pecas.")
    except Exception as e:
        print(f"Erro ao adicionar coluna: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    adicionar_coluna_valor_instalado()
