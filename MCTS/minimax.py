import random
import time
import copy


__nb_iter = None

def evaluate(game):
    score = 0
    for _ in range(__nb_iter):
        game_copy = copy.deepcopy(game)
        turn = 0
        while not game_copy.end():
            moves = game_copy.get_all_moves()
            m = moves[random.randint(0, len(moves) - 1)]
            game_copy.play(m)
            turn += 1
        if game_copy.end() == 3:
            score += 0
        elif turn % 2 == 1:
            score += 1
        else:
            score -= 1
    return score / __nb_iter

def pv_search(game, depth, pv, pline, a = -2, b = 2):
    if not pv:
        return minmax(game, depth, pline, a, b)
    end = game.end()
    if end:
        pline[:] = []
        return 0 if end == 3 else -1
    if depth <= 0:
        pline[:] = []
        return evaluate(game)

    line = []
    game_copy = copy.deepcopy(game)
    value = -pv_search(game_copy.play(pv[0]), depth - 1, pv[1:], line, -b, -a)
    if value >= b:
        return b
    if value > a:
        a = value
        pline[:] = [pv[0]] + line

    for m in game_copy.get_all_moves():
        if m == pv[0]:
            continue
        game_copy = copy.deepcopy(game)
        value = -minmax(game_copy.play(m), depth - 1, line, -b, -a)
        if value >= b:
            return b
        if value > a:
            a = value
            pline[:] = [m] + line
    return a


def minmax(game, depth, pline, a = -2, b = 2):
    end = game.end()
    if end:
        pline[:] = []
        return 0 if end == 3 else -1
    if depth <= 0:
        pline[:] = []
        return evaluate(game)
    value = -1
    line = []
    for m in game.get_all_moves():
        game_copy = copy.deepcopy(game)
        value = -minmax(game_copy.play(m), depth - 1, line, -b, -a)
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
    print(f" | Evaluation: {a / 2 + 0.5:.2f}", end="")
    print(f" | {pourcent:>3}% [{waiting}]    ", end="", flush=True)


def play(game, max_time=4, nb_iter=20):
    global __nb_iter
    __nb_iter = nb_iter
    move = None
    moves = game.get_all_moves()
    depth = 0
    pv = []
    start_time = time.time()
    while time.time() < start_time + max_time:
        depth += 1
        a = -2
        line = []
        if pv:
            game_copy = copy.deepcopy(game)
            a = -pv_search(game_copy.play(move), depth - 1, pv[1:], line, b = -a)
            pv[:] = [move] + line
        for m in moves:
            if pv and m == pv[0]:
                continue
            game_copy = copy.deepcopy(game)
            val = -minmax(game_copy.play(m), depth - 1, line, b = -a)
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
