import sys
from games.tictactoe.game import TicTacToe
from games.connect4.game import Connect4
from games.wesnuts.game import Wesnuts
import numpy as np
import MCTS.ai
import random

from MCTS.validation import score

class Command:
    def __init__(self, name, args, desc, func):
        self.name = name
        self.args = args
        self.desc = desc
        self.func = func

def get_game(game):
    games = {
            "connect4": Connect4(),
            "tictactoe": TicTacToe(),
            "wesnuts": Wesnuts(),
            }
    if game not in games:
        print("Unknown game:", game)
        sys.exit(1)
    return games[game]

def play_game(game, p1, p2):
    turn = 0
    while not game.end():
        game.print_state()
        move = -1
        player = (p1, p2)[turn % 2]
        if player:
            move = player.play()
        while move == -1:
            choice = -2
            exit = 1
            try:
                choice = input(f"Select a move to play {game.get_all_moves()}:")
                exit = 0
                choice = int(choice)
            except:
                if exit:
                    sys.exit(0)
                print("Please provide a valid number")
                continue
            if choice in game.get_all_moves():
                move = choice
            else:
                print("Your choice is not a valid move")
        if p1: p1.notify_move(move)
        if p2: p2.notify_move(move)
        state = game.play(move)
        turn += 1
    game.print_state()
    print(("", "Player 1 wins!", "Player 2 wins!", "Draw")[game.end()])

def train(game, config, ai):
    game_module = get_game(game)
    MCTS.ai.train(game, game_module, config, ai)

def play_humans(game):
    game_module = get_game(game)
    play_game(game_module, None, None)

def play_human_vs_ai(game, human_side, ai):
    game_module = get_game(game)
    if human_side != "1" and human_side != "2":
        print("'human_side' must be either 1 or 2")
        sys.exit(1)
    ai_model = MCTS.ai.load_from(game, ai, game_module, 3 - int(human_side))
    if human_side == "1":
        play_game(game_module, None, ai_model)
    else:
        play_game(game_module, ai_model, None)

def play_ais(game, ai_1, ai_2, nb_game):
    game_module = get_game(game)
    ai_1_model = MCTS.ai.load_from(game, ai_1, game_module, 1)
    ai_2_model = MCTS.ai.load_from(game, ai_2, game_module, 2)
    if int(nb_game) == 1:
        play_game(game_module, ai_1_model, ai_2_model)
    else:
        score(game_module, ai_1_model, ai_2_model, int(nb_game))

commands = [
        Command("train", ["<game>", "<config>", "<ai>"],
            "Train the ai to play the given game", train),
        Command("play_humans", ["<game>"],
            "Start a game between 2 humans", play_humans),
        Command("play_human_vs_ai", ["<game>", "<human_side>", "<ai>"],
            "Start a game against the given ai", play_human_vs_ai),
        Command("play_ais", ["<game>", "<ai_1>", "<ai_2>", "<nb>"],
            "Start 'nb' game(s) between 2 ais", play_ais)
        ]


def help():
    print("Usage: python3", sys.argv[0], "<command> [args...]")
    print("Here is the list of the available commands and their arguments:")
    for c in commands:
        print(f" * {c.name}".ljust(21), f"{' '.join(c.args)}".ljust(30), "|", c.desc)

if __name__ == "__main__":
    #random.seed(10)
    #np.random.seed(seed=0)
    if len(sys.argv) < 2:
        help()
    else:
        for c in commands:
            if c.name == sys.argv[1] and len(c.args) == len(sys.argv) - 2:
                c.func(*sys.argv[2:])
                sys.exit(0)
        help()
        sys.exit(1)
