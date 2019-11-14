import numpy as np

class TicTacToeBoard:

    def __init__(self, board=np.array([0] * 9)):
        self.board = board

    def get_all_moves(self):
        moves = np.where(self.board == 0)[0]
        if moves.size==0 and not self.end():
            return np.array([])
        return moves

    def apply_move(self, move, player):
        self.board[move] = player
    
    def end(self):
        wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6))
        p1 = np.where(self.board == 1)
        for w in wins:
            if np.all(np.isin(w, p1)):
                return 1
        p2 = np.where(self.board == 2)
        for w in wins:
            if np.all(np.isin(w, p2)):
                return 2
        if 0 not in self.board:
            return 3
        return 0


    def print_state(self):
        value = np.array(["   ", " X ", " O "])
        print()
        print(*value[self.board[:3]], sep="|")
        print("---|---|---")
        print(*value[self.board[3:6]], sep="|")
        print("---|---|---")
        print(*value[self.board[6:]], sep="|")
        print()

