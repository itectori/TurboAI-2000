import time
import copy

def play(game, p1, p2):
    turn = 0
    while not game.end():
        move = -1
        if turn % 2 == 0:
            move = p1.play_for_eval(False)
        else:
            move = p2.play_for_eval(False)
        p1.notify_move(move)
        p2.notify_move(move)
        game.play(move)
        turn += 1
    return game.end()

def log_info(i, nb_game, res):
    p1 = p2 = draw = 0.
    if i != 0:
        p1 = res[0] / i
        p2 = res[1] / i
        draw = res[2] / i
    print(end=f"\rGame {i:>3} / {nb_game} | p1: {p1:.2f} | p2: {p2:.2f} | draw: {draw:.2f}",
          flush = True)


def score(game, p1, p2, nb_game):
    res = [0, 0, 0]
    start_time = time.time()
    for i in range(nb_game):
        log_info(i, nb_game, res)
        p1.reset()
        p2.reset()
        if i % 2 == 0:
            res[play(copy.deepcopy(game), p1, p2) - 1] += 1
        else:
            tmp = play(copy.deepcopy(game), p2, p1)
            if tmp == 3:
                res[2] += 1
            else:
                res[2 - tmp] += 1
    log_info(nb_game, nb_game, res)
    print()
    print(f"Time: {time.time() - start_time:.2f} seconds")
    return [n / nb_game for n in res]
