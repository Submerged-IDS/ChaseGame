import socket
import threading
import pickle
import pygame

from Constants import GRID_WIDTH, GRID_HEIGHT
from MapRenderer import MapRenderer

class Client:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.maze = None
        
    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")

            self.receiveMaze()

            send_thread = threading.Thread(target=self.sendMessages)
            receive_thread = threading.Thread(target=self.receiveMessages)
            send_thread.start()
            receive_thread.start()

            if self.maze:
                self.renderMap()

            send_thread.join()
            receive_thread.join()

        except ConnectionError:
            print("Connection failed.")
        finally:
            self.disconnect()

    def receiveMaze(self):
        try:
            serialised_maze = self.client_socket.recv(4096)
            self.maze = pickle.loads(serialised_maze)
            print("Maze received from server.")
        except Exception as e:
            print(f"Error receiving maze: {e}")

    def renderMap(self):
        pygame.init()
        screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
        pygame.display.set_caption("Chase Game")
        clock = pygame.time.Clock()
        renderer = MapRenderer(screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            renderer.drawMap(self.maze)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

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
    




