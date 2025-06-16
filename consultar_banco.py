import sqlite3
import sys

def executar_consulta(sql):
    """Executa uma consulta SQL e exibe os resultados"""
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Executar a consulta
        cursor.execute(sql)
        resultados = cursor.fetchall()
        
        # Exibir os resultados
        if not resultados:
            print("Nenhum resultado encontrado.")
            return
        
        # Obter nomes das colunas
        colunas = [description[0] for description in cursor.description]
        
        # Imprimir cabeçalho
        print("\n" + "-" * 80)
        print(" | ".join(colunas))
        print("-" * 80)
        
        # Imprimir linhas
        for linha in resultados:
            valores = [str(linha[coluna]) for coluna in colunas]
            print(" | ".join(valores))
        
        print("-" * 80)
        print(f"Total de registros: {len(resultados)}")
        
    except sqlite3.Error as e:
        print(f"Erro ao executar consulta: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Verificar se foi fornecida uma consulta
    if len(sys.argv) > 1:
        consulta = " ".join(sys.argv[1:])
    else:
        # Consulta padrão
        consulta = "SELECT * FROM clientes ORDER BY id DESC"
    
    print(f"Executando consulta: {consulta}")
    executar_consulta(consulta)
