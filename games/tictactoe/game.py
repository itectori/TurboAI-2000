import numpy as np
import sys
from games.tictactoe.board import TicTacToeBoard

class TicTacToe:

    def __init__(self):
        self.board = TicTacToeBoard()
        self.turn_to = 1

    def play(self, move):
        self.board.apply_move(move, self.turn_to)
        self.turn_to = 3-self.turn_to

    def get_all_moves(self):
        return self.board.get_all_moves()

    def print_state(self):
        self.board.print_state()
    
    def end(self):
        return self.board.end()

