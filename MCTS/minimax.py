import random
import time

__nb_iter = None

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

def pv_search(game, state, depth, pv, pline, a = -2, b = 2):
    if not pv:
        return minmax(game, state, depth, pline, a, b)
    end = game.end(state)
    if end:
        pline[:] = []
        return 0 if end == 3 else -1
    if depth <= 0:
        pline[:] = []
        return evaluate(game, state)

    line = []
    value = -pv_search(game, game.play(state, pv[0]), depth - 1, pv[1:], line, -b, -a)
    if value >= b:
        return b
    if value > a:
        a = value
        pline[:] = [pv[0]] + line

    for m in game.get_all_moves(state):
        if m == pv[0]:
            continue
        value = -minmax(game, game.play(state, m), depth - 1, line, -b, -a)
        if value >= b:
            return b
        if value > a:
            a = value
            pline[:] = [m] + line
    return a


def minmax(game, state, depth, pline, a = -2, b = 2):
    end = game.end(state)
    if end:
        pline[:] = []
        return 0 if end == 3 else -1
    if depth <= 0:
        pline[:] = []
        return evaluate(game, state)
    value = -1
    line = []
    for m in game.get_all_moves(state):
        value = -minmax(game, game.play(state, m), depth - 1, line, -b, -a)
        if value >= b:
            return b
        if value > a:
            a = value
            pline[:] = [m] + line
    return a

def log_info(depth, move, a, pourcent):
    waiting = "#" * (pourcent // 10) + ".........."
    waiting = waiting[:10]
    print(f"\rDepth: {depth:>2}", end="")
    print(f" | Best move: {move}", end="")
    print(f" | Confidence: {a / 2 + 0.5:.2f}", end="")
    print(f" | {pourcent:>3}% [{waiting}]    ", end="", flush=True)


def play(game, state, max_time=4, nb_iter=20):
    global __nb_iter
    __nb_iter = nb_iter
    move = None
    moves = game.get_all_moves(state)
    depth = 0
    pv = []
    start_time = time.time()
    while time.time() < start_time + max_time:
        depth += 1
        a = -2
        line = []
        if pv:
            a = -pv_search(game, game.play(state, move), depth - 1, pv[1:], line, b = -a)
            pv[:] = [move] + line
        for m in moves:
            if pv and m == pv[0]:
                continue
            val = -minmax(game, game.play(state, m), depth - 1, line, b = -a)
            if val > a:
                a = val
                move = m
                pv[:] = [m] + line
            approx = 0.8 * (time.time() - start_time) / max_time
            pourcent = min(100, int(100 * approx))
            log_info(depth, move, a, pourcent)
        if depth >= 99:
            break
    log_info(depth, move, a, 100)
    print()
    print(f"Time: {time.time() - start_time:.1f} seconds")
    print(f"Principal variation: {pv}")
    return move
