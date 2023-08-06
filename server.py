import socket
import os

def receive_file(connection, addr, filename):
    print(f"Recebendo arquivo '{filename}' de {addr[0]}:{addr[1]}")

    with open(filename, 'wb') as file:
        while True:
            data, client_addr = connection.recvfrom(1024)
            if not data:
                break
            file.write(data)

    print(f"Arquivo '{filename}' recebido e armazenado.")
    print("Arquivo salvo em:", os.path.abspath(filename))
    print("Tamanho do arquivo:", os.path.getsize(filename))


def main():
    server_ip = 'localhost'
    server_port = 24883

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))

    print(f"Servidor iniciado em {server_ip}:{server_port}")

    clients = [] 

    try:
        while True:
            data, addr = server_socket.recvfrom(1024)
            message = data.decode('utf-8')

            if message == "FILE":
                filename, addr = server_socket.recvfrom(1024)
                filename = filename.decode('utf-8')
                receive_file(server_socket, addr, filename)
                response = "Arquivo recebido com sucesso!"
            else:
                response = "Mensagem recebida: " + message

            print("Recebido de", addr[0], ":", response)
  
            # Enviar resposta para o cliente
            server_socket.sendto(response.encode('utf-8'), addr)

    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
