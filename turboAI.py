import sys
import connect4.game as connect4
import tictactoe.game as tictactoe

class Command:
    def __init__(self, name, args, desc, func):
        self.name = name
        self.args = args
        self.desc = desc
        self.func = func

def get_game(game):
    games = {
            "connect4": connect4.Game(),
            "tictactoe": tictactoe.Game()
            }
    if game not in games:
        print("Unknown game:", game)
        sys.exit(1)
    return games[game]

def learn(game, config, ai):
    game = get_game(game)

def play_humans(game):
    game = get_game(game)
    game.interactive_mode(None, None)

def play_human_vs_ai(game, human_side, ai):
    game = get_game(game)

def play_ais(game, ai_1, ai_2):
    game = get_game(game)

commands = [Command("learn", ["<game>", "<config>", "<ai>"],
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

if len(sys.argv) < 2:
    help()
else:
    for c in commands:
        if c.name == sys.argv[1] and len(c.args) == len(sys.argv) - 2:
            c.func(*sys.argv[2:])
            sys.exit(0)
    help()
