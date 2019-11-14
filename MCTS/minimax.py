import random

__nb_iter = 20

def evaluate(game, state):
    score = 0
    for _ in range(__nb_iter):
        copy_state = state
        turn = 0
        while not game.end(copy_state):
            moves = game.get_all_moves(copy_state)
            m = moves[random.randint(0, len(moves) - 1)]
            copy_state = game.play(copy_state, m)
            turn += 1
        if game.end(copy_state) == 3:
            score += 0
        elif turn % 2 == 1:
            score += 1
        else:
            score -= 1
    return score / __nb_iter

def minmax(game, state, depth, a = -1, b = 1):
    end = game.end(state)
    if end:
        return 0 if end == 3 else -1
    if depth <= 0:
        return evaluate(game, state)
    value = -1
    for m in game.get_all_moves(state):
        value = max(value, -minmax(game, game.play(state, m), depth - 1, -b, -a))
        a = max(a, value)
        if a >= b:
            break
    return value

def play(game, state, depth=4, nb_iter=30):
    move = None
    a = -2
    __nb_iter = nb_iter
    moves = game.get_all_moves(state)
    waiting = ""
    print(f"\r[{waiting:<{len(moves)}}] {100*len(waiting)//len(moves)}%", end="")
    for m in moves:
        val = -minmax(game, game.play(state, m), depth - 1, b = -a)
        if val > a:
            a = val
            move = m
        waiting += "#"
        print(f"\r[{waiting:<{len(moves)}}] {100*len(waiting)//len(moves)}%", end="")
    print()
    print(f"Confidence: {a/2 + 0.5}")
    return move
