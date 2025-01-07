import socket
import threading
import pickle

from Constants import ROWS, COLUMNS, BLUE, RED
from MazeGenerator import MazeGenerator
from Player import Player
from GameState import GameState  # Step 1: Import GameState

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
        self.maze = None
        self.players = {}
        self.game_state = GameState()  # Step 2: Initialize GameState

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print(f"Server started on {self.host}:{self.port}")
        self.generateMaze()

    def generateMaze(self):
        maze_gen = MazeGenerator()
        self.maze = maze_gen.generateMaze()
        print("Maze Generated")

    def acceptClients(self):
        try:
            self.server_socket.settimeout(1)
            while len(self.clients) < self.max_clients:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Client {client_address} connected.")

                    if len(self.clients) == 0:
                        player_1 = Player(3, 2, 2, BLUE, self.maze)
                        self.players[client_socket] = player_1
                    elif len(self.clients) == 1:
                        player_2 = Player(4, ROWS-3, COLUMNS-3, RED, self.maze)
                        self.players[client_socket] = player_2

                    self.clients.append(client_socket)
                    self.sendMaze(client_socket)
                    self.broadcastPlayerPositions()

                    client_thread = threading.Thread(target=self.handleClients, args=(client_socket, client_address))
                    self.client_threads.append(client_thread)
                    client_thread.start()
                except socket.timeout:
                    pass

            print("No longer accepting clients.")
            self.game_state.startRound()  # Step 3: Start the game round
        except KeyboardInterrupt:
            print("Server shutting down...")
            self.stop()

    def sendMaze(self, client_socket):
        try:
            serialised_maze = pickle.dumps(self.maze)
            client_socket.sendall(serialised_maze)
            print(f"Maze sent to client {client_socket}")
        except Exception as e:
            print(f"Error sending maze to client {e}")

    def broadcastPlayerPositions(self):
        with self.lock:
            positions = {player.player_id: (player.x, player.y) for player in self.players.values()}
            serialised_positions = pickle.dumps(positions)
            for client in self.clients:
                client.sendall(serialised_positions)

    def handleClients(self, client_socket, client_address):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if message.lower() == 'exit':
                    print(f"Client {client_address} disconnected.")
                    break

                if message.startswith("Move"):
                    _, direction = message.split()
                    direction = int(direction)
                    player = self.players[client_socket]
                    player.move(direction)
                    self.broadcastPlayerPositions()

                    if player.checkTag(self.players.values()):
                        self.game_state.endRound()  # Step 4: End the round if a player is tagged
                        if self.game_state.current_round > 6:
                            self.broadcast("Game Over", client_socket)
                            self.stop()
                            break
                        else:
                            self.game_state.startRound()

                print(f"Message from {client_address}: {message}")

        except ConnectionError:
            print(f"Client {client_address} disconnected.")

        finally:
            with self.lock:
                client_socket.close()
                self.clients.remove(client_socket)
                del self.players[client_socket]

    def broadcast(self, message, sender_socket):
        with self.lock:
            for client in self.clients:
                if client != sender_socket:
                    client.send(message.encode('utf-8'))

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