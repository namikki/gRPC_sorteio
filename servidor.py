from concurrent import futures
import grpc
import sorteio_pb2
import sorteio_pb2_grpc
import sqlite3
import random
import time

# Banco SQLite
DB_FILE = "sorteio.db"

# Função para configurar o banco de dados
def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS numeros (id INTEGER PRIMARY KEY, numero INTEGER)")
    conn.commit()
    conn.close()

# Função para gerar números aleatórios no banco
def generate_numbers():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Gera 100 números aleatórios para sorteio
    cursor.executemany("INSERT INTO numeros (numero) VALUES (?)", [(random.randint(1, 100),) for _ in range(100)])
    conn.commit()
    conn.close()

# Definindo o serviço de sorteio
class SorteioService(sorteio_pb2_grpc.SorteioServiceServicer):
    def IniciarSorteio(self, request, context):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT numero FROM numeros ORDER BY RANDOM() LIMIT 10")
        numeros_sorteados = [row[0] for row in cursor.fetchall()]
        conn.close()

        for numero in numeros_sorteados:
            # Envia os números sorteados um por um com delay
            yield sorteio_pb2.NumeroSorteado(numero=numero)
            time.sleep(2)  # Delay de 2 segundos

# Função para rodar o servidor gRPC
def serve():
    setup_database()
    generate_numbers()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sorteio_pb2_grpc.add_SorteioServiceServicer_to_server(SorteioService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Servidor iniciado na porta 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
