import keras
from keras.models import load_model
import os
import sys
import numpy as np

class AI:
    def __init__(self, rdn):
        self.rdn = rdn

    def set_game(self, game):
        self.game = game

    def play(self, state):
        # TODO: call MCTS
        valid = self.game.get_all_moves(state)
        y = self.rdn.predict(np.array([self.game.encode_input(state)]))[0]
        for c in reversed(np.argsort(y)):
            if c in valid:
                return c

def load_from(game_name, ai):
    path = "ais/" + game_name + "/" + ai
    if os.path.isdir(path):
        print(ai, "does not exist")
        sys.exit(1)
    return AI(load_model(path))

