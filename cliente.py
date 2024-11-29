import grpc
import sorteio_pb2
import sorteio_pb2_grpc
import random

# Função para solicitar os números sorteados ao servidor
def solicitar_bingo(stub):
    # Gera uma nova cartela com 5 números aleatórios
    cartela = random.sample(range(1, 100), 5)
    print(f"\nSua nova cartela: {cartela}")
    print("Aguardando números sorteados...\n")

    # Solicita os números sorteados ao servidor
    response_stream = stub.IniciarSorteio(sorteio_pb2.Empty())

    # Processa os números recebidos em tempo real
    for numero_sorteado in response_stream:
        print(f"Número sorteado: {numero_sorteado.numero}")

        if numero_sorteado.numero in cartela:
            print(f"-> Bingo! O número {numero_sorteado.numero} está na sua cartela!")

    print("\nSorteio encerrado!\n")

# Função principal para interagir com o cliente
def main():
    # Conecta ao servidor gRPC
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = sorteio_pb2_grpc.SorteioServiceStub(channel)

        while True:
            # Inicia um novo bingo
            solicitar_bingo(stub)

            # Pergunta ao cliente se deseja outro bingo
            opcao = input("Deseja iniciar outro bingo? (s/n): ").strip().lower()
            if opcao != 's':
                print("Obrigado por jogar! Até a próxima!")
                break

if __name__ == '__main__':
    main()
