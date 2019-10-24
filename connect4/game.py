import numpy as np
import sys

class Game:
    def init(self):
        return np.array([1, np.array([[0] * 6 for _ in range(7)]), -1])

    def get_all_moves(self, state):
        return np.where(state[1].T[0] == 0)[0]

    def print_state(self, state):
        value = np.array(["   ", " X ", " O "])
        print()
        for i in range(6):
            print(*value[state[1].T[i]], sep="|")
        print("|".join(["---"] * 7))
        print(end=" ")
        print(*range(7), sep=" | ")
        print()

    def play(self, state, action):
        state[1][action][np.where(state[1][action] == 0)[0][-1]] = state[0]
        state[0] -= 3
        state[0] *= -1
        state[2] = action
        return state

    def _check(self, state, x, y, dx, dy):
        c = 0
        grid = state[1]
        first = grid[x, y]
        x += dx
        y += dy
        while 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
            if grid[x, y] != first:
                return c
            c += 1
            x += dx
            y += dy
        return c

    def end(self, state):
        if state[2] == -1:
            return 0
        last_player = -(state[0] - 3)
        x = state[2]
        y = np.where(state[1][x] == last_player)[0][0]
        if self._check(state, x, y, 0, 1) + self._check(state, x, y, 0, -1) >= 3:
            return last_player
        if self._check(state, x, y, 1, 0) + self._check(state, x, y, -1, 0) >= 3:
            return last_player
        if self._check(state, x, y, 1, 1) + self._check(state, x, y, -1, -1) >= 3:
            return last_player
        if self._check(state, x, y, -1, 1) + self._check(state, x, y, 1, -1) >= 3:
            return last_player
        if len(self.get_all_moves(state)) == 0:
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

