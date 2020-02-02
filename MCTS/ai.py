import keras
from keras.layers import Input, Dense
from keras.models import load_model, Model
import os
import sys
import numpy as np
import json
from shutil import copyfile
import MCTS.minimax
#from MCTS.mcts import MCTS as Tree
from MCTS.coach import Coach
from MCTS.mcts2 import Tree
import keras.backend as K
import random
import copy

class AI:
    def __init__(self, rdn, game, config, player):
        self.rdn = rdn
        self.game = copy.deepcopy(game)
        self.config = config
        if self.config["algo"] == "MCTS":
            self.mcts = Tree(self.config["c_puct"], self.config["tau"])
        self.board = copy.deepcopy(game)

    def reset(self):
        if self.config["algo"] == "MCTS":
            self.mcts = Tree(self.config["c_puct"], self.config["tau"])
        self.board = copy.deepcopy(self.game)

    def notify_move(self, move):
        if self.config["algo"] == "MCTS":
            self.board = self.mcts.move_to_children(self.board, move)
        else:
            self.board = self.board.play(move)

    def predict(self, board):
        pred = self.rdn.predict([[board.encode_input()]])
        pi = pred[0][0]
        eval_ = pred[1][0][0]
        return pi, eval_

    def play(self, verbose=True):
        if self.config["algo"] == "minimax":
            return MCTS.minimax.play(self.board,
                                        start_depth=self.config["start_depth"],
                                        max_depth=self.config["max_depth"],
                                        max_time=self.config["max_time"],
                                        nb_iter_eval=self.config["nb_iter_eval"],
                                        verbose=verbose)

        if self.config["algo"] == "random":
            return random.choice(self.board.get_all_moves())

        return self.mcts.play_best_move(self.board,
                                self,
                                self.config["play_simulation"],
                                verbose=verbose)

    
    def play_for_eval(self, verbose=True):
        if self.config["algo"] == "minimax":
            return MCTS.minimax.play(self.board,
                                        start_depth=self.config["start_depth"],
                                        max_depth=self.config["max_depth"],
                                        max_time=self.config["max_time"],
                                        nb_iter_eval=self.config["nb_iter_eval"],
                                        verbose=verbose)

        if self.config["algo"] == "random":
            return random.choice(self.board.get_all_moves())

        return self.mcts.play(self.board,
                                self,
                                self.config["play_simulation"],
                                verbose=verbose)
        
def load_config(config):
    with open(config) as config_file:
        return json.load(config_file)


def load_from(game_name, ai, game_module, player):
    path = "ais/" + game_name + "/" + ai
    if not os.path.exists(path + "_config.json"):
        print(ai, "does not exist")
        sys.exit(1)
    if os.path.exists(path):
        return AI(load_model(path,  custom_objects={"loss_eval": loss_eval, "loss_p": loss_p}), game_module, load_config(path + "_config.json"), player)
    return AI(None, game_module, load_config(path + "_config.json"), player)


def save(model, game_name, name, config):
    path = "ais/" + game_name
    if not os.path.isdir(path):
        os.makedirs(path)
    copyfile(config, path + "/" + name + "_config.json")
    if model:
        model.save(path + "/" + name)


def loss_eval(y_true, y_pred):
    return K.sum(K.square(y_pred - y_true))

def loss_p(y_true, y_pred):
    return -K.dot(y_true, K.transpose(K.log(y_pred)))

def train(game_name, game_module, config, name):
    config_json = load_config(config)
    if config_json["algo"] != "MCTS":
        save(None, game_name, name, config)
        return

    input_layer = Input(shape=(len(game_module.encode_input()),))
    layer = input_layer
    for l in config_json["nn"]["hidden_layers"]:
        layer = Dense(l["size"], activation=l["activation"])(layer)
    p = Dense(config_json["nn"]["policy_size"], activation='softmax', name='p')(layer)
    eval_ = Dense(1, activation='tanh', name='eval')(layer)
    model = Model(inputs=[input_layer], outputs=[p, eval_])

    model.compile(optimizer=config_json["nn"]["optimizer"], \
            loss={"p": loss_p, "eval": loss_eval}, \
                  metrics=['accuracy'],
                  loss_weights=[1., 1.])

    ai_1 = AI(model, game_module, config_json, 1)
    #ai_2 = AI(model, game_module, config_json, 2)

    '''
    X = [[game_module.encode_input()]]
    Y = [[[0, 0, 0, 0, 1, 0, 0, 0, 0]],[-1]]
    print(model.predict(X))
    model.fit(X, Y, epochs=500, verbose=0)
    print(model.predict(X))'''
    
    '''
    X = [[game_module.encode_input(), game_module.encode_input()]]
    Y = [[[0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0]],[-1, -1]]
    print(model.predict(X))
    model.fit(X, Y, epochs=500, verbose=0)
    print(model.predict(X))'''


    coach = Coach(ai_1)
    coach.learn()

    #TODO train neural network
    #MCTS.mcts.train(ai, game_module, config_json)
    save(model, game_name, name, config)
