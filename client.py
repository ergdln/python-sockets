import socket
import os
import threading

def send_file(connection, filename):
    connection.send("FILE".encode('utf-8'))
    connection.send(filename.encode('utf-8'))

    with open(filename, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            connection.send(data)

    print("Arquivo enviado para o servidor.")

def receive_messages(connection):
    while True:
        data = connection.recv(1024)
        if not data:
            break

        message = data.decode()

        if message == "FILE":
            filename = connection.recv(1024).decode()
            receive_file(connection, filename)
        else:
            print("Mensagem recebida do servidor:", message)

def receive_file(connection, filename):
    print(f"Recebendo arquivo '{filename}' do servidor")

    with open(filename, 'wb') as file:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            file.write(data)

    print(f"Arquivo '{filename}' recebido do servidor")

def main():
    server_ip = 'localhost'
    server_port = 24883

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Iniciar a thread de recebimento de mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        message = input("Digite uma mensagem ou o caminho do arquivo para enviar (ou 'sair' para encerrar): ")

        if message.lower() == "sair":
            break

        if os.path.isfile(message):
            send_file(client_socket, message)
        else:
            client_socket.send(message.encode())

    client_socket.close()

if __name__ == "__main__":
    main()
