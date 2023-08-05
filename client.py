import socket
import os

def send_file(connection, filename):
    connection.send("FILE".encode())
    connection.send(filename.encode())

    with open(filename, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            connection.send(data)

    print("Arquivo enviado para o servidor.")

def main():
    server_ip = 'localhost'
    server_port = 24883

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        message = input("Digite uma mensagem ou o caminho do arquivo para enviar (ou 'sair' para encerrar): ")

        if message.lower() == "sair":
            break

        if os.path.isfile(message):
            send_file(client_socket, message)
        else:
            client_socket.send(message.encode())

        data = client_socket.recv(1024)
        print("Resposta do servidor:", data.decode())

    client_socket.close()

if __name__ == "__main__":
    main()
