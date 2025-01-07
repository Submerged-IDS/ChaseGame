import time

class GameState:
    def __init__(self):
        self.current_round = 1
        self.it_player = 3
        self.scores = {
            3: 0,
            4: 0
        }
        self.start_time = 0

    def startRound(self):
        print(f"Starting Round {self.current_round}: Player {self.it_player} is it!")
        self.start_time = time.time()

    def endRound(self):
        if self.it_player == 3:
            other_player = 4
        else:
            other_player = 3
        
        survival_time = time.time() - self.start_time
        self.scores[other_player] += survival_time

        if self.current_round >= 6:
            return self.gameOver()
        else:
            self.switchRoles()
            return False
        
    def switchRoles(self):
        if self.it_player == 3:
            self.it_player = 4
        else:
            self.it_player = 3

        self.current_round += 1
        self.startRound()
        
    def gameOver(self):
        print("Game Over!")
        winner = max(self.scores, key=self.scores.get)
        print(f"Player {winner} wins")
        return True



