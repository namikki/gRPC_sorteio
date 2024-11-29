# Criando um Sorteador usando servidor gRPC

### Estrutura do projeto
```
gRCP_sorteio/
├── cliente.proto
├── servidor.py
├── sorteio_pb2_grpc.py
├── sorteio_pb2.py
├── sorteio.proto
└── README.md
```

### Como testar
Siga os passos abaixo para compilar o arquivo .proto e executar o servidor e cliente.

### Instale os pacotes do gRPC e Protobuf para Python

Certifique-se de que você instalou as bibliotecas Python necessárias:
````bash
pip install grpcio grpcio-tools
````

### Compile o arquivo .proto
Use o comando ``python -m grpc_tools.protoc`` para compilar o arquivo ``.proto`` e gerar os arquivos Python.
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. sorteio.proto
```
**Explicação dos parâmetros:**

``-I.``: Define o diretório onde o arquivo ``.proto`` está localizado.

``--python_out=.``: Gera as classes de mensagens ``(sorteio_pb2.py)``.

``--grpc_python_out=.``: Gera as classes do serviço gRPC ``(sorteio_pb2_grpc.py)``.

### Rode o Servidor e Cliente
```bash
python servidor.py
python cliente.py
```
