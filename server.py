import socket
import threading
import os
import queue

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

        # Colocar a mensagem na fila
        message_queue.put(response)

    with clients_lock:
        clients.remove(client_socket)
        client_socket.close()

def process_message_queue():
    while True:
        # Pegar a mensagem da fila
        message = message_queue.get()

        # Encaminhar a mensagem para todos os clientes conectados
        with clients_lock:
            for client in clients:
                client.send(message.encode())

        message_queue.task_done()

def main():
    server_ip = 'localhost'
    server_port = 24883

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)

    print(f"Servidor iniciado em {server_ip}:{server_port}")

    try:
        processing_thread = threading.Thread(target=process_message_queue)
        processing_thread.daemon = True
        processing_thread.start()

        while True:
            client_socket, addr = server_socket.accept()
            print("Cliente conectado:", addr[0], ":", addr[1])

            with clients_lock:
                clients.append(client_socket)

            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_handler.start()

    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    clients = []
    clients_lock = threading.Lock()
    message_queue = queue.Queue()
    main()
