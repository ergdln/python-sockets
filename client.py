import socket
import os
import threading 

def send_file(connection, server_addr, filename):
    connection.sendto("FILE".encode('utf-8'), server_addr)
    connection.sendto(filename.encode('utf-8'), server_addr)

    with open(filename, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            connection.sendto(data, server_addr)

    print("Arquivo enviado para o servidor.")


def receive_messages(connection):
    while True:
        data, addr = connection.recvfrom(1024)
        if not data:
            break
        print("Mensagem recebida do servidor:", data.decode('utf-8'))


def main():
    server_ip = 'localhost'
    server_port = 24883
    server_addr = (server_ip, server_port)  # Tupla com o endereço do servidor

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Iniciar a thread de recebimento de mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    while True:
        message = input("Digite uma mensagem ou o caminho do arquivo para enviar (ou 'sair' para encerrar): ")

        if message.lower() == "sair":
            break

        if os.path.isfile(message):
            send_file(client_socket, server_addr, message)
        else:
            client_socket.sendto(message.encode('utf-8'), server_addr)

    client_socket.close()


if __name__ == "__main__":
    main()
