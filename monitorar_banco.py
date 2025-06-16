import sqlite3
import time
import os
import datetime

def monitorar_banco():
    print("=== MONITOR DE BANCO DE DADOS INICIADO ===")
    print("Este script monitorará alterações na tabela de clientes.")
    print("Pressione Ctrl+C para encerrar.\n")
    
    # Registros conhecidos
    registros_conhecidos = {}
    
    try:
        while True:
            # Conectar ao banco de dados
            conn = sqlite3.connect('banco.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Buscar todos os clientes
            cursor.execute("SELECT id, nome, telefone, email, endereco FROM clientes")
            clientes = cursor.fetchall()
            
            # Converter para dicionário para facilitar comparação
            clientes_atuais = {cliente['id']: dict(cliente) for cliente in clientes}
            
            # Verificar novos registros ou alterações
            for id, cliente in clientes_atuais.items():
                if id not in registros_conhecidos:
                    # Novo cliente
                    print(f"\n[{datetime.datetime.now()}] NOVO CLIENTE ADICIONADO:")
                    print(f"ID: {cliente['id']}")
                    print(f"Nome: {cliente['nome']}")
                    print(f"Telefone: {cliente['telefone']}")
                    print(f"Email: {cliente['email']}")
                    print(f"Endereço: {cliente['endereco']}")
                    print("=" * 50)
                elif registros_conhecidos[id] != cliente:
                    # Cliente alterado
                    print(f"\n[{datetime.datetime.now()}] CLIENTE ALTERADO (ID: {id}):")
                    for campo in ['nome', 'telefone', 'email', 'endereco']:
                        if registros_conhecidos[id][campo] != cliente[campo]:
                            print(f"{campo.capitalize()}: {registros_conhecidos[id][campo]} -> {cliente[campo]}")
                    print("=" * 50)
            
            # Verificar registros removidos
            for id in list(registros_conhecidos.keys()):
                if id not in clientes_atuais:
                    print(f"\n[{datetime.datetime.now()}] CLIENTE REMOVIDO:")
                    print(f"ID: {id}")
                    print(f"Nome: {registros_conhecidos[id]['nome']}")
                    print("=" * 50)
            
            # Atualizar registros conhecidos
            registros_conhecidos = clientes_atuais
            
            # Fechar a conexão
            conn.close()
            
            # Aguardar antes da próxima verificação
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado pelo usuário.")

if __name__ == "__main__":
    monitorar_banco()
