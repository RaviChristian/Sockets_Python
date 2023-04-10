import socket
import json

# Define o endereço IP e porta do servidor
HOST = 'localhost'
PORT = 8000

# Cria o socket do cliente
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta com o servidor
s.connect((HOST, PORT))

# Função para enviar uma mensagem ao servidor
def send_msg(msg):
    # Converte a mensagem em JSON
    json_msg = json.dumps(msg)
    # Envia a mensagem ao servidor
    s.sendall(json_msg.encode())
    # Recebe a resposta do servidor
    data = s.recv(1024).decode()
    # Converte a resposta de JSON para um dicionário Python
    msg = json.loads(data)
    # Retorna a resposta do servidor
    return msg

# Loop principal do cliente
while True:
    # Pede ao usuário que digite uma opção
    op = input("\nDigite 1 para adicionar um novo cliente\n2 para listar os clientes cadastrados\n3 para alterar informaçoes de um usuário ")

    if op == '1':
        # Pede ao usuário que digite o nome, email e senha
        nome = input("Digite o nome do cliente: ")
        email = input("Digite o email do cliente: ")
        senha = input("Digite a senha do cliente: ")
        # Cria um dicionário com os dados do cliente
        dados = {'nome': nome, 'email': email, 'senha': senha}
        # Envia uma mensagem POST ao servidor com os dados do cliente
        msg = {'tipo': 'POST', 'dados': dados}
        # Envia a mensagem e imprime a resposta do servidor
        httpResponse = send_msg(msg)
        print('\n',httpResponse,'\n')
        print(httpResponse['msg'],'\n')

    elif op == '2':
        # Envia uma mensagem GET ao servidor para obter os dados dos clientes
        httpRequest = {'tipo': 'GET'}
        # Envia a mensagem e imprime a resposta do servidor
        httpResponse = send_msg(httpRequest)
        dados = httpResponse['dados']
        if len(dados) == 0:
            print('\n "HTTP Response: "',httpResponse,'\n')
            print("Nenhum cliente cadastrado.\n")
        else:
            print('\n "HTTP Response: "',httpResponse,'\n')
            print("Clientes cadastrados:\n")
            for cliente in dados:
                print(f"Nome: {cliente['nome']}, Email: {cliente['email']}, Senha: {cliente['senha']}")

    elif op == '3':
        id = input("Digite o id do usuário que deseja alterar: ")
        nome = input("Digite o nome do cliente: ")
        email = input("Digite o email do cliente: ")
        senha = input("Digite a senha do cliente: ")

        dados = {'id':id, 'nome': nome, 'email': email, 'senha': senha}
        httpRequest = {'tipo':'PUT','dados' : dados}

        httpResponse = send_msg(httpRequest)
        print('\n',httpResponse,'\n')
        print(httpResponse['msg'],'\n')

    else:
        msg = {'tipo': 'Bad Request'}
        httpResponse = send_msg(msg)
        print('\n "HTTP Response: "',httpResponse,'\n')
        print("Opção inválida.\n")
