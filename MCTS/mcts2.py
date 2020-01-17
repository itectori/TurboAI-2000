import copy
import math
import time
import numpy as np

class Tree:

    def __init__(self, c_puct, tau):
        self.c_puct = c_puct
        self.tau = tau
        self.visited = set()
        self.children = {}
        self.P = {}
        self.N = {}
        self.Q = {}

    def log_info(self, best_move, evaluation, percent):
        percent = min(100, int(percent))
        waiting = '#' * (percent // 10) + ".........."
        print(end=f"Best move: {best_move} ")
        print(end=f"| Evaluation: {evaluation:.2f} ")
        print(end=f"| {percent:>3}% ")
        print(end=f"[{waiting[:10]}]\r")

    def play(self, board, ai, nb_iter, verbose=True):
        pi= self.get_proba(board, ai, nb_iter, verbose)
        #print(np.argmax(pi))
        return np.random.choice(range(len(pi)), p=pi)
    
    def get_proba(self, board, ai, nb_iter, verbose=True):
        assert nb_iter >= 2
        s = 0
        disp_i = max(1, nb_iter // 11)
        start_time = time.time()
        for i in range(nb_iter):
            s += self.search(board, ai)
            if verbose and i % disp_i == 0:
                self.log_info(np.argmax(self.pi(board)), (1 - s/(i+1))/2, 100 * i / nb_iter)
        pi = self.pi(board)
        if verbose:
            self.log_info(np.argmax(pi), (1 - s/nb_iter)/2, 100)
            print()
            print(f"Time: {time.time() - start_time:.1f} seconds")
            print(f"Pi: {[int(i * 100)/100 for i in pi]}")
        return pi

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
            u = self.Q[board][m] + self.c_puct * self.P[board][m] * math.sqrt(sum(self.N[board])) / (1. + self.N[board][m])
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
        s = sum(np.power(self.N[board], 1 / self.tau))
        if s == 0:
            return [0 for _ in self.N[board]]
        return [math.pow(n, 1 / self.tau) / s for n in self.N[board]]
