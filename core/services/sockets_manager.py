import socket
import threading


class SocketsManager:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server = None
        self.clients = []

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Socket server started on {self.host}:{self.port}")

        thread = threading.Thread(target=self.accept_clients)
        thread.start()

    def accept_clients(self):
        while True:
            client_socket, client_address = self.server.accept()
            print(f"Connection from {client_address}")
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                print(f"Received message: {message}")
                # Handle message
            except ConnectionResetError:
                break
        client_socket.close()

    def broadcast(self, message):
        for client in self.clients:
            client.sendall(message.encode())

    def stop(self):
        if self.server:
            self.server.close()
        for client in self.clients:
            client.close()
