import socket
import threading

class Server:
    
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.client_threads = []
        self.max_clients = 2
        self.ready = False
        self.lock = threading.Lock()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print(f"Server started on {self.host}:{self.port}")

    def acceptClients(self):
        try:
            self.server_socket.settimeout(1)
            while len(self.clients) < self.max_clients:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    self.clients.append(client_socket)
                    print(f"Client {client_address} connected.")

                    client_thread = threading.Thread(target=self.handleClients, args=(client_socket, client_address))
                    self.client_threads.append(client_thread)
                    client_thread.start()
                except socket.timeout:
                    pass

            print("No longer accepting clients.")
        except KeyboardInterrupt:
            print("Server shutting down...")
            self.stop()
    
    def handleClients(self, client_socket, client_address):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if message.lower() == 'exit':
                    print(f"Client {client_address} disconnected.")
                    break
                print(f"Message from {client_address}: {message}")
                client_socket.send(f"Server recieved: {message}".encode('utf-8'))

        except ConnectionError:
            print(f"Client {client_address} disconnected.")

        finally:
            with self.lock:
                client_socket.close()
            self.clients.remove(client_socket)

    def stop(self):
        print("Shutting down server...")
        for client in self.clients:
            client.close()
        for thread in self.client_threads:
            thread.join()
        self.server_socket.close()
        print("Server shut down successfully.")

if __name__ == '__main__':
    try:
        server = Server(host='127.0.0.1', port=8080)
        server.start()
        server.acceptClients()
    except KeyboardInterrupt:
        server.stop()



