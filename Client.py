import socket
import threading

class Client:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        
    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")

            send_thread = threading.Thread(target=self.sendMessages)
            receive_thread = threading.Thread(target=self.receiveMessages)
            send_thread.start()
            receive_thread.start()

            send_thread.join()
            receive_thread.join()

        except ConnectionError:
            print("Connection failed.")
        finally:
            self.disconnect()

    def sendMessages(self):
        while self.running:
            try:
                message = input("Enter message: ")
                self.client_socket.send(message.encode('utf-8'))
                if message.lower() == 'exit':
                    self.running = False
                    break
            except ConnectionError:
                print("Error sending message. Disconnected from server.")
                self.running = False
                break

    def receiveMessages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Server: {message}")
            except ConnectionError:
                print("Disconnected from server.")
                self.running = False
                break

    def disconnect(self):
        print("Disconnecting...")
        self.client_socket.close()
        print("Disconnect Successful.")

if __name__ == "__main__":
    client = Client(host='127.0.0.1', port=8080)
    client.connect()
    




