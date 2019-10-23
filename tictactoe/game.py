import numpy as np

def init():
    return np.array([1, np.array([0] * 9)])

def get_all_moves(state):
    return np.where(state[1] == 0)[0]

def print_state(state):
    value = np.array(["   ", " X ", " O "])
    print()
    print(*value[state[1][:3]], sep="|")
    print("---|---|---")
    print(*value[state[1][3:6]], sep="|")
    print("---|---|---")
    print(*value[state[1][6:]], sep="|")
    print()

def play(state, action):
    state[1][action] = state[0]
    state[0] -= 3
    state[0] *= -1
    return state

def end(state):
    wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6))
    p1 = np.where(state[1] == 1)
    for w in wins:
        if False not in np.isin(w, p1):
            return 1
    p2 = np.where(state[1] == 2)
    for w in wins:
        if False not in np.isin(w, p2):
            return 2
    if 0 not in state[1]:
        return 3
    return 0

def interactive_mode():
    state = init()
    while not end(state):
        print_state(state)
        move = -1
        while move == -1:
            choice = -1
            try:
                choice = int(input(f"Select a move to play {get_all_moves(state)}:"))
                if choice in get_all_moves(state):
                    move = choice
                else:
                    print("Your choice is not a valid move")
            except:
                print("Please provide a valid number")
        play(state, move)
    print_state(state)
    print(("", "Player 1 wins!", "Player 2 wins!", "Draw")[end(state)])

if __name__ == "__main__":
    interactive_mode()
