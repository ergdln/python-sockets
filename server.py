import socket
import threading
import os

def receive_file(connection, addr, filename):
    print(f"Recebendo arquivo '{filename}' de {addr[0]}:{addr[1]}")

    with open(filename, 'wb') as file:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            file.write(data)

    print(f"Arquivo '{filename}' recebido e armazenado.")

def handle_client(client_socket, addr):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        message = data.decode()

        if message == "FILE":
            filename = client_socket.recv(1024).decode()
            receive_file(client_socket, addr, filename)
            response = "Arquivo recebido com sucesso!"
        else:
            response = "Mensagem recebida: " + message

        print("Recebido de", addr[0], ":", response)

        # Encaminhar a mensagem para todos os clientes conectados
        for client in clients:
            if client != client_socket:
                client.send(response.encode())

    client_socket.close()

def main():
    server_ip = 'localhost'
    server_port = 24883

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)

    print(f"Servidor iniciado em {server_ip}:{server_port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print("Cliente conectado:", addr[0], ":", addr[1])

            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_handler.start()
            clients.append(client_socket)

    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    clients = []
    main()
