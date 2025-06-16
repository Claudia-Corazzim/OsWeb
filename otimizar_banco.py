import sqlite3

def otimizar_banco():
    """Adiciona índices ao banco de dados para melhorar o desempenho"""
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    
    # Índice para cliente_id em ordens_servico
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cliente_id ON ordens_servico (cliente_id)')
    
    # Índice para nome em clientes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cliente_nome ON clientes (nome)')
    
    # Índice para nome em pecas
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_peca_nome ON pecas (nome)')
    
    conn.commit()
    conn.close()
    print("Banco de dados otimizado com sucesso!")

if __name__ == "__main__":
    otimizar_banco()
