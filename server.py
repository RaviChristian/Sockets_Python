import socket
import threading
import json

# Define o endereço IP e porta do servidor
HOST = 'localhost'
PORT = 8000

# Cria o socket do servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket com o endereço IP e porta definidos
s.bind((HOST, PORT))

# Define o tamanho máximo da fila de conexões pendentes
s.listen()

# Array para armazenar os dados
dados = []
id = 0

# Função para lidar com um cliente
def handle_client(conn):
    global id
    while True:
        # Recebe os dados do cliente
        data = conn.recv(1024).decode()
        if not data:
            break

        # Converte a mensagem JSON recebida em um dicionário Python
        httpRequest = json.loads(data)
        print("HTTP Request: ",httpRequest)
        
        # Verifica o tipo de mensagem
        if httpRequest['tipo'] == 'POST':
            # Adiciona os dados recebidos ao array
            httpRequest['dados']['id'] = id
            id += 1
            dados.append(httpRequest['dados'])
            # Envia uma mensagem de confirmação com código de status HTTP 201
            httpResponse = {'status': '201 OK', 'content-type': 'text/plain', 'msg': 'Dados adicionados com sucesso.'}
            conn.sendall(json.dumps(httpResponse).encode())


        elif httpRequest['tipo'] == 'GET':
            # Envia os dados armazenados no array
            if len(dados) == 0:
                # Envia uma mensagem de erro com código de status HTTP 404
                httpResponse = {'status': '404 Not Found', 'content-type': 'text/plain', 'msg': 'Nenhum cliente cadastrado.','dados':dados}
                conn.sendall(json.dumps(httpResponse).encode())
            else:
                # Envia uma mensagem de sucesso com código de status HTTP 200
                httpResponse = {'status': '200 OK', 'content-type': 'application/json', 'dados':dados}
                conn.sendall(json.dumps(httpResponse).encode())


        elif httpRequest['tipo'] == 'PUT':
            id_Request = httpRequest['dados']['id']

            if httpRequest['dados']['id'] == '' or httpRequest['dados']['nome'] == '' or httpRequest['dados']['email'] == '' or httpRequest['dados']['senha'] == '':
                httpResponse = {'status': '400 Bad Request', 'content-type': 'text/plain', 'msg': 'Campo inválido.'}
                conn.sendall(json.dumps(httpResponse).encode())
            id_exists = False
            for user in dados:
                if int(user['id']) == int(id_Request):
                    id_exists = True

            if id_exists == True:
                for user in dados:
                    if int(user['id']) == int(id_Request):
                        user['nome'] = httpRequest['dados']['nome']
                        user['email'] = httpRequest['dados']['email']
                        user['senha'] = httpRequest['dados']['senha']
                httpResponse =  {'status': '200 OK', 'content-type': 'application/json', 'dados': user, 'msg': 'Dados alterados com sucesso.'}
                conn.sendall(json.dumps(httpResponse).encode())

            else:
                httpResponse = {'status': '404 Not Found', 'content-type': 'text/plain', 'msg': 'Nenhum cliente com esse id cadastrado.'}
                conn.sendall(json.dumps(httpResponse).encode())

        else:
            # Envia uma mensagem de erro com código de status HTTP 400
            httpResponse = {'status': '400 Bad Request', 'content-type': 'text/plain', 'msg': 'Opção inválida.'}
            conn.sendall(json.dumps(httpResponse).encode())

    # Fecha a conexão
    conn.close()


# Loop principal do servidor
while True:
    # Aceita a conexão do cliente
    conn, addr = s.accept()
    print(f"Cliente {addr} conectado.")

    # Inicia uma nova thread para lidar com o cliente
    t = threading.Thread(target=handle_client, args=(conn,))
    t.start()
