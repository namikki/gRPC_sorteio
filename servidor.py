from concurrent import futures
import grpc
import sorteio_pb2
import sorteio_pb2_grpc
import sqlite3
import random

# Banco SQLite
DB_FILE = "sorteio.db"

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS numeros (id INTEGER PRIMARY KEY, numero INTEGER)")
    conn.commit()
    conn.close()

def generate_numbers():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Gera 100 números aleatórios para sorteio
    cursor.executemany("INSERT INTO numeros (numero) VALUES (?)", [(random.randint(1, 100),) for _ in range(100)])
    conn.commit()
    conn.close()

class SorteioService(sorteio_pb2_grpc.SorteioServiceServicer):
    def SolicitarNumero(self, request, context):
        numero = random.randint(1, 100)
        return sorteio_pb2.NumeroResponse(numero=numero)

    def SolicitarNumeros(self, request, context):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT numero FROM numeros ORDER BY RANDOM() LIMIT 5")
        numeros_sorteados = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        numero_encontrado = request.numero_cliente in numeros_sorteados
        return sorteio_pb2.SorteioResponse(numeros_sorteados=numeros_sorteados, numero_encontrado=numero_encontrado)

    def ReiniciarOuEncerrar(self, request, context):
        if request.reiniciar:
            return sorteio_pb2.RespostaFinal(mensagem="Novo sorteio iniciado!")
        else:
            return sorteio_pb2.RespostaFinal(mensagem="Sorteio encerrado. Obrigado por participar!")

def serve():
    setup_database()
    generate_numbers()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sorteio_pb2_grpc.add_SorteioServiceServicer_to_server(SorteioService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
