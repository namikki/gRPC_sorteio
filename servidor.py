import time
import grpc
from concurrent import futures
import sorteio_pb2
import sorteio_pb2_grpc
import sqlite3
import random


class SorteioService(sorteio_pb2_grpc.SorteioServiceServicer):
    def __init__(self):
        # Conecta ao banco de dados SQLite e cria a tabela
        self.conn = sqlite3.connect('sorteio.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        # Cria a tabela para armazenar os números sorteados
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS numeros_sorteados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero INTEGER NOT NULL
                )
            """)

    def IniciarSorteio(self, request, context):
        # Gera 10 números aleatórios
        numeros_sorteados = random.sample(range(1, 100), 10)

        # Armazena os números no banco de dados
        with self.conn:
            self.conn.executemany(
                "INSERT INTO numeros_sorteados (numero) VALUES (?)",
                [(numero,) for numero in numeros_sorteados]
            )

        # Envia os números para o cliente com um delay de 2 segundos
        for numero in numeros_sorteados:
            time.sleep(2)
            yield sorteio_pb2.NumeroSorteado(numero=numero)

def serve():
    # Configuração do servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sorteio_pb2_grpc.add_SorteioServiceServicer_to_server(SorteioService(), server)
    print("Servidor gRPC iniciado na porta 50051...")
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
