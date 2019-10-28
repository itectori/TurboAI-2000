import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import os
import sys
import numpy as np
import MCTS.mcts

class AI:
    def __init__(self, rdn):
        self.rdn = rdn

    def set_game(self, game_module):
        self.game = game_module

    def play(self, state):
        # TODO: call MCTS play
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

def train(game_name, game_module, config, name):
    # TODO: Use config to create rdn structure
    ### tmp ###
    model = Sequential()
    model.add(Dense(32, input_shape=(19,), activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(32, activation='sigmoid'))
    model.add(Dense(9, activation='softmax'))
    model.compile(optimizer='rmsprop',
            loss='categorical_crossentropy',
            metrics=['accuracy'])
    ai = AI(model)
    ### end tmp ###

    ai.set_game(game_module)
    MCTS.mcts.train(ai, game_module, config)
    if not os.path.isdir("ais/" + game_name):
        os.makedirs("ais/" + game_name)
    model.save("ais/" + game_name + "/" + name)

