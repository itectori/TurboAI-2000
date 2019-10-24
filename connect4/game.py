import numpy as np
import sys

def init():
    return np.array([1, np.array([[0] * 6 for _ in range(7)]), -1])

def get_all_moves(state):
    return np.where(state[1].T[0] == 0)[0]

def print_state(state):
    value = np.array(["   ", " X ", " O "])
    print()
    for i in range(6):
        print(*value[state[1].T[i]], sep="|")
    print("|".join(["---"] * 7))
    print(end=" ")
    print(*range(7), sep=" | ")
    print()

def play(state, action):
    state[1][action][np.where(state[1][action] == 0)[0][-1]] = state[0]
    state[0] -= 3
    state[0] *= -1
    state[2] = action
    return state

def _check(state, x, y, dx, dy):
    c = 0
    grid = state[1]
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
    if state[2] == -1:
        return 0
    last_player = -(state[0] - 3)
    x = state[2]
    y = np.where(state[1][x] == last_player)[0][0]
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

def interactive_mode():
    state = init()
    while not end(state):
        print_state(state)
        move = -1
        while move == -1:
            choice = -2
            try:
                choice = int(input(f"Select a move to play {get_all_moves(state)} (-1 to quit):"))
            except:
                print("Please provide a valid number")
                continue
            if choice == -1:
                sys.exit(0)
            if choice in get_all_moves(state):
                move = choice
            else:
                print("Your choice is not a valid move")
        play(state, move)
    print_state(state)
    print(("", "Player 1 wins!", "Player 2 wins!", "Draw")[end(state)])

if __name__ == "__main__":
    interactive_mode()

