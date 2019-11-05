import numpy as np

class State:
    def __init__(self, player, grid):
        self.player = player
        self.grid = grid

def init():
    return State(1, np.array([0] * 9))

def get_all_moves(state):
    return np.where(state.grid == 0)[0]

def print_state(state):
    value = np.array(["   ", " X ", " O "])
    print()
    print(*value[state.grid[:3]], sep="|")
    print("---|---|---")
    print(*value[state.grid[3:6]], sep="|")
    print("---|---|---")
    print(*value[state.grid[6:]], sep="|")
    print()

def play(state, action):
    state.grid[action] = state.player
    state.player -= 3
    state.player *= -1
    return state

def end(state):
    wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6))
    p1 = np.where(state.grid == 1)
    for w in wins:
        if np.all(np.isin(w, p1)):
            return 1
    p2 = np.where(state.grid == 2)
    for w in wins:
        if np.all(np.isin(w, p2)):
            return 2
    if 0 not in state.grid:
        return 3
    return 0

def encode_input(state):
    rdn_input = [state.player]
    p1 = (state.grid == 1).astype(np.int)
    p2 = (state.grid == 2).astype(np.int)
    for e in zip(p1, p2):
        rdn_input += e
    return np.array(rdn_input)

