import grpc
import sorteio_pb2
import sorteio_pb2_grpc

def main():
    channel = grpc.insecure_channel("localhost:50051")
    stub = sorteio_pb2_grpc.SorteioServiceStub(channel)

    # Solicitar número inicial
    numero_inicial = stub.SolicitarNumero(sorteio_pb2.Empty()).numero
    print(f"Seu número inicial: {numero_inicial}")

    tentativas = 5
    while tentativas > 0:
        response = stub.SolicitarNumeros(sorteio_pb2.SolicitarRequest(
            numero_cliente=numero_inicial,
            tentativas_restantes=tentativas
        ))
        print(f"Números sorteados: {response.numeros_sorteados}")
        if response.numero_encontrado:
            print("Parabéns! Seu número foi sorteado!")
            break
        tentativas -= 1
        print(f"Tentativas restantes: {tentativas}")
    
    if tentativas == 0:
        print("Seu número não foi sorteado nas tentativas permitidas.")
        opcao = input("Deseja tentar novamente com um novo número? (s/n): ")
        if opcao.lower() == "s":
            stub.ReiniciarOuEncerrar(sorteio_pb2.OpcaoRequest(reiniciar=True))
            main()
        else:
            stub.ReiniciarOuEncerrar(sorteio_pb2.OpcaoRequest(reiniciar=False))
            print("Encerrando o sorteio. Até logo!")

if __name__ == "__main__":
    main()
