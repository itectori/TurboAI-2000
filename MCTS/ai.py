import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import os
import sys
import numpy as np
import json
from shutil import copyfile
import MCTS.minimax
from MCTS.mcts import MCTS as Tree

class AI:
    def __init__(self, rdn, game, config, player):
        self.rdn = rdn
        self.game = game
        self.config = config
        self.mcts = Tree(player)

    def play(self, state):
        if self.config["minimax"]:
            return MCTS.minimax.play(state)
        
        return self.mcts.find_next_move(state, 1000)
        
        
def load_config(config):
    with open(config) as config_file:
        return json.load(config_file)


def load_from(game_name, ai, game_module, player):
    path = "ais/" + game_name + "/" + ai
    if not os.path.exists(path + "_config.json"):
        print(ai, "does not exist")
        sys.exit(1)
    if os.path.exists(path):
        return AI(load_model(path), game_module, load_config(path + "_config.json"), player)
    return AI(None, game_module, load_config(path + "_config.json"), player)


def save(model, game_name, name, config):
    path = "ais/" + game_name
    if not os.path.isdir(path):
        os.makedirs(path)
    copyfile(config, path + "/" + name + "_config.json")
    if model:
        model.save(path + "/" + name)


def train(game_name, game_module, config, name):
    config_json = load_config(config)
    if config_json["minimax"]:
        save(None, game_name, name, config)
        return

    model = Sequential()
    for l in config_json["layers"]:
        exec(f'model.add(Dense({l["out"]}, \
                input_shape=({l["in"]},), \
                activation=\'{l["activation"]}\'))')
    model.compile(optimizer='adam', \
                  loss='categorical_crossentropy', \
                  metrics=['accuracy'])

    ai_1 = AI(model, game_module, config_json, 1)
    ai_2 = AI(model, game_module, config_json, 2)
    #TODO train neural network
    #MCTS.mcts.train(ai, game_module, config_json)
    save(None, game_name, name, config) # FIXME: model = None
