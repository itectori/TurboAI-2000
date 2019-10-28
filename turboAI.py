import sys
import games.connect4.game as connect4
import games.tictactoe.game as tictactoe
import numpy as np
import MCTS.ai

class Command:
    def __init__(self, name, args, desc, func):
        self.name = name
        self.args = args
        self.desc = desc
        self.func = func

def get_game(game):
    games = {
            "connect4": connect4,
            "tictactoe": tictactoe
            }
    if game not in games:
        print("Unknown game:", game)
        sys.exit(1)
    return games[game]

def play_game(game, p1, p2):
    state = game.init()
    turn = 0
    while not game.end(state):
        game.print_state(state)
        move = -1
        player = (p1, p2)[turn % 2]
        if player:
            move = player.play(state)
        while move == -1:
            choice = -2
            try:
                choice = int(input(f"Select a move to play {game.get_all_moves(state)} (-1 to quit):"))
            except:
                print("Please provide a valid number")
                continue
            if choice == -1:
                sys.exit(0)
            if choice in game.get_all_moves(state):
                move = choice
            else:
                print("Your choice is not a valid move")
        game.play(state, move)
        turn += 1
    game.print_state(state)
    print(("", "Player 1 wins!", "Player 2 wins!", "Draw")[game.end(state)])

def learn(game, config, ai):
    game_module = get_game(game)

def play_humans(game):
    game_module = get_game(game)
    play_game(game_module, None, None)

def play_human_vs_ai(game, human_side, ai):
    game_module = get_game(game)
    if human_side != "1" and human_side != "2":
        print("'human_side' must be either 1 or 2")
        sys.exit(1)
    ai_model = MCTS.ai.load_from(game, ai)
    ai_model.set_game(game_module)
    if human_side == "1":
        play_game(game_module, None, ai_model)
    else:
        play_game(game_module, ai_model, None)

def play_ais(game, ai_1, ai_2):
    game_module = get_game(game)
    ai_1_model = MCTS.ai.load_from(game, ai_1)
    ai_2_model = MCTS.ai.load_from(game, ai_2)
    ai_1_model.set_game(game_module)
    ai_2_model.set_game(game_module)
    play_game(game_module, ai_1_model, ai_2_model)

commands = [
        Command("learn", ["<game>", "<config>", "<ai>"],
            "Train the ai to play the given game", learn),
        Command("play_humans", ["<game>"],
            "Start a game between 2 humans", play_humans),
        Command("play_human_vs_ai", ["<game>", "<human_side>", "<ai>"],
            "Start a game against the given ai", play_human_vs_ai),
        Command("play_ais", ["<game>", "<ai_1>", "<ai_2>"],
            "Start a game between 2 ais", play_ais)
        ]


def help():
    print("Usage: python3", sys.argv[0], "<command> [args...]")
    print("Here is the list of the available commands and their arguments:")
    for c in commands:
        print(f" * {c.name}".ljust(21), f"{' '.join(c.args)}".ljust(30), "|", c.desc)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        help()
    else:
        for c in commands:
            if c.name == sys.argv[1] and len(c.args) == len(sys.argv) - 2:
                c.func(*sys.argv[2:])
                sys.exit(0)
        help()
        sys.exit(1)
