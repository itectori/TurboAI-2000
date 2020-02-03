import numpy as np

class TicTacToe:
    def __init__(self):
        self.grid = np.array([0] * 9)
        self.player = 1

    def get_all_moves(self):
        return np.where(self.grid == 0)[0]

    def print_state(self):
        value = np.array(["   ", " X ", " O "])
        print()
        print(*value[self.grid[:3]], sep="|")
        print("---|---|---")
        print(*value[self.grid[3:6]], sep="|")
        print("---|---|---")
        print(*value[self.grid[6:]], sep="|")
        print()

    def play(self, action):
        self.grid[action] = self.player
        self.player -= 3
        self.player *= -1
        return self

    def end(self):
        wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6))
        p1 = np.where(self.grid == 1)
        for w in wins:
            if np.all(np.isin(w, p1)):
                return 1
        p2 = np.where(self.grid == 2)
        for w in wins:
            if np.all(np.isin(w, p2)):
                return 2
        if 0 not in self.grid:
            return 3
        return 0

    def encode_input(self):
        '''        
        rdn_input = [0, 0]
        rdn_input[self.player - 1] = 1
        p1 = (self.grid == 1).astype(np.int)
        p2 = (self.grid == 2).astype(np.int)
        for e in zip(p1, p2):
            rdn_input += e
        return np.array(rdn_input)
        '''

        encoded = np.zeros([3,3,3]).astype(np.int)
        encoded[0,:,:] = (self.grid == 1).astype(np.int).reshape(3,3)
        encoded[1,:,:] = (self.grid == 2).astype(np.int).reshape(3,3)
        encoded[2,:,:] = self.player-1 # player to move
        
        return encoded