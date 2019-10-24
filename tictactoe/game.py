import numpy as np
import sys

class Game:
    def init(self):
        return np.array([1, np.array([0] * 9)])

    def get_all_moves(self, state):
        return np.where(state[1] == 0)[0]

    def print_state(self, state):
        value = np.array(["   ", " X ", " O "])
        print()
        print(*value[state[1][:3]], sep="|")
        print("---|---|---")
        print(*value[state[1][3:6]], sep="|")
        print("---|---|---")
        print(*value[state[1][6:]], sep="|")
        print()

    def play(self, state, action):
        state[1][action] = state[0]
        state[0] -= 3
        state[0] *= -1
        return state

    def end(self, state):
        wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6))
        p1 = np.where(state[1] == 1)
        for w in wins:
            if False not in np.isin(w, p1):
                return 1
        p2 = np.where(state[1] == 2)
        for w in wins:
            if False not in np.isin(w, p2):
                return 2
        if 0 not in state[1]:
            return 3
        return 0

    def interactive_mode(self, p1, p2):
        state = self.init()
        turn = 0
        while not self.end(state):
            self.print_state(state)
            move = -1
            if (p1, p2)[turn % 2]:
                move = self.get_all_moves(state) #TODO call ai function
            while move == -1:
                choice = -2
                try:
                    choice = int(input(f"Select a move to play {self.get_all_moves(state)} (-1 to quit):"))
                except:
                    print("Please provide a valid number")
                    continue
                if choice == -1:
                    sys.exit(0)
                if choice in self.get_all_moves(state):
                    move = choice
                else:
                    print("Your choice is not a valid move")
            self.play(state, move)
            turn += 1
        self.print_state(state)
        print(("", "Player 1 wins!", "Player 2 wins!", "Draw")[self.end(state)])

if __name__ == "__main__":
    Game().interactive_mode(None, None)
