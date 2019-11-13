import numpy as np

class State:
    def __init__(self, player, grid, last_move):
        self.player = player
        self.grid = grid
        self.last_move = last_move

def init():
    return State(1, np.array([[0] * 6 for _ in range(7)]), -1)

def get_all_moves(state):
    return np.where(state.grid.T[0] == 0)[0]

def print_state(state):
    value = np.array(["   ", " X ", " O "])
    print()
    for i in range(6):
        print(*value[state.grid.T[i]], sep="|")
    print("|".join(["---"] * 7))
    print(end=" ")
    print(*range(7), sep=" | ")
    print()

def play(state, action):
    state = State(state.player, np.copy(state.grid), state.last_move)
    state.grid[action][np.where(state.grid[action] == 0)[0][-1]] = state.player
    state.player -= 3
    state.player *= -1
    state.last_move = action
    return state

def _check(state, x, y, dx, dy):
    c = 0
    grid = state.grid
    first = grid[x, y]
    x += dx
    y += dy
    while 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
        if grid[x, y] != first:
            return c
        c += 1
        x += dx
        y += dy
    return c

def end(state):
    if state.last_move == -1:
        return 0
    last_player = -(state.player - 3)
    x = state.last_move
    y = np.where(state.grid[x] == last_player)[0][0]
    if _check(state, x, y, 0, 1) + _check(state, x, y, 0, -1) >= 3:
        return last_player
    if _check(state, x, y, 1, 0) + _check(state, x, y, -1, 0) >= 3:
        return last_player
    if _check(state, x, y, 1, 1) + _check(state, x, y, -1, -1) >= 3:
        return last_player
    if _check(state, x, y, -1, 1) + _check(state, x, y, 1, -1) >= 3:
        return last_player
    if len(get_all_moves(state)) == 0:
        return 3
    return 0

def encode_input(state):
    rdn_input = [state.player]
    p1 = (state.grid.flatten() == 1).astype(np.int)
    p2 = (state.grid.flatten() == 2).astype(np.int)
    for e in zip(p1, p2):
        rdn_input += e
    return np.array(rdn_input)

