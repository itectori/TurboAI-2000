import copy
import math

class Tree:

    def __init__(self):
        self.visited = set()
        self.children = {}
        self.P = {}
        self.N = {}
        self.Q = {}

    def move_to_children(self, board, best_move):
        if board in self.children and self.children[board][best_move] is not None:
            return self.children[board][best_move]
        board_copy = copy.deepcopy(board)
        board_copy.play(best_move)
        return board_copy


    def select_next_board(self, board):
        max_u = -float("inf")
        best_move = -1
        for m in board.get_all_moves():
            u = self.Q[board][m] + 0.1 * self.P[board][m] * math.sqrt(sum(self.N[board])) / (1. + self.N[board][m])
            if u > max_u:
                max_u = u
                best_move = m
        return self.move_to_children(board, best_move), best_move

    def search(self, board, ai):
        end = board.end()
        if end == 3:
            return 0.
        if end:
            return 1.

        if board not in self.visited:
            self.visited.add(board)
            p, v = ai.predict(board)
            self.children[board] = [None] * len(p)
            self.N[board] = [0.] * len(p)
            self.Q[board] = [0.] * len(p)
            self.P[board] = p
            return -v

        next_board, best_move = self.select_next_board(board)
        v = self.search(next_board, ai)
        if next_board not in self.children[board]:
            self.children[board][best_move] = next_board

        self.Q[board][best_move] = (self.N[board][best_move] * self.Q[board][best_move] + v) / (self.N[board][best_move] + 1.)
        self.N[board][best_move] += 1
        return -v

    def pi(self, board):
        s = sum(self.N[board])
        return [n / s for n in self.N[board]]
