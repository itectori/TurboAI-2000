import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import os
import sys
import numpy as np
import MCTS.mcts
import json
from shutil import copyfile


class AI:
    def __init__(self, rdn, config):
        self.rdn = rdn
        self.config = config

    def set_game(self, game_module):
        self.game = game_module

    def play(self, state):
        # TODO: call MCTS play
        valid = self.game.get_all_moves(state)
        y = self.rdn.predict(np.array([self.game.encode_input(state)]))[0]
        for c in reversed(np.argsort(y)):
            if c in valid:
                return c

def load_config(config):
    with open(config) as config_file:
        return json.load(config_file)


def load_from(game_name, ai):
    path = "ais/" + game_name + "/" + ai
    if os.path.isdir(path):
        print(ai, "does not exist")
        sys.exit(1)
    return AI(load_model(path), load_config(path + "_config.json"))

def train(game_name, game_module, config, name):
    config_json = load_config(config)
    model = Sequential()
    for l in config_json["layers"]:
        exec(f'model.add(Dense({l["out"]}, \
                input_shape=({l["in"]},), \
                activation=\'{l["activation"]}\'))')

    model.compile(optimizer='adam', \
            loss='categorical_crossentropy', \
            metrics=['accuracy'])
    ai = AI(model, config_json)

    ai.set_game(game_module)
    MCTS.mcts.train(ai, game_module, config_json)
    path = "ais/" + game_name
    if not os.path.isdir(path):
        os.makedirs(path)
    copyfile(config, path + "/" + name + "_config.json")
    model.save(path + "/" + name)
