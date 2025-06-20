def criar_tabelas():
    conn = get_db_connection()    
    
    # Verificar se é necessário atualizar a tabela de clientes
    try:
        # Verifica se as colunas email e endereco existem
        conn.execute('SELECT email, endereco FROM clientes LIMIT 1')
    except sqlite3.OperationalError:
        # Se não existir, cria uma nova tabela com as colunas
        conn.execute('DROP TABLE IF EXISTS clientes')
        conn.execute('''
            CREATE TABLE clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                endereco TEXT
            );
        ''')
    else:
        # Se já existir, não faz nada
        pass
        
    # Verificar se é necessário atualizar a tabela de ordens de serviço
    try:
        # Verifica se as colunas veiculo e placa existem
        conn.execute('SELECT veiculo, placa FROM ordens_servico LIMIT 1')
    except sqlite3.OperationalError:
        # Se não existir, cria uma nova tabela com as colunas
        conn.execute('DROP TABLE IF EXISTS ordens_servico')
        conn.execute('''
            CREATE TABLE ordens_servico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                data TEXT NOT NULL,
                veiculo TEXT,
                placa TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            );
        ''')
    else:
        # Se já existir, não faz nada
        pass
        
    # Verificar se é necessário atualizar a tabela de peças
    try:
        # Verifica se a coluna valor_instalado existe
        conn.execute('SELECT valor_instalado FROM pecas LIMIT 1')
    except sqlite3.OperationalError:
        # Se a coluna valor_instalado não existir, adiciona-a
        try:
            conn.execute('ALTER TABLE pecas ADD COLUMN valor_instalado REAL')
            print("Coluna valor_instalado adicionada com sucesso à tabela pecas")
        except sqlite3.OperationalError as e:
            # Se houver um erro na alteração, recria a tabela
            print(f"Erro ao adicionar coluna: {e}. Recriando tabela...")
            conn.execute('DROP TABLE IF EXISTS pecas')
            conn.execute('''
                CREATE TABLE pecas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    valor REAL,
                    valor_instalado REAL
                );
            ''')
            print("Tabela pecas recriada com sucesso!")
    else:
        # Se a coluna valor_instalado já existir, não faz nada
        pass

    conn.commit()
    conn.close()
