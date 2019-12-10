import numpy as np

class Connect4:
    def __init__(self):
        self.player = 1
        self.grid = np.array([[0] * 6 for _ in range(7)])
        self.last_move = -1

    def get_all_moves(self):
        return np.where(self.grid.T[0] == 0)[0]

    def print_state(self):
        value = np.array(["   ", " X ", " O "])
        print()
        for i in range(6):
            print(*value[self.grid.T[i]], sep="|")
        print("|".join(["---"] * 7))
        print(end=" ")
        print(*range(7), sep=" | ")
        print()

    def play(self, action):
        self.grid[action][np.where(self.grid[action] == 0)[0][-1]] = self.player
        self.player -= 3
        self.player *= -1
        self.last_move = action
        return self

    def _check(self, x, y, dx, dy):
        c = 0
        grid = self.grid
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

    def end(self):
        if self.last_move == -1:
            return 0
        last_player = -(self.player - 3)
        x = self.last_move
        y = np.where(self.grid[x] == last_player)[0][0]
        if self._check(x, y, 0, 1) + self._check(x, y, 0, -1) >= 3:
            return last_player
        if self._check(x, y, 1, 0) + self._check(x, y, -1, 0) >= 3:
            return last_player
        if self._check(x, y, 1, 1) + self._check(x, y, -1, -1) >= 3:
            return last_player
        if self._check(x, y, -1, 1) + self._check(x, y, 1, -1) >= 3:
            return last_player
        if len(self.get_all_moves()) == 0:
            return 3
        return 0

    def encode_input(self):
        rdn_input = [0, 0]
        rdn_input[self.player - 1] = 1
        p1 = (self.grid.flatten() == 1).astype(np.int)
        p2 = (self.grid.flatten() == 2).astype(np.int)
        for e in zip(p1, p2):
            rdn_input += e
        return np.array(rdn_input)

