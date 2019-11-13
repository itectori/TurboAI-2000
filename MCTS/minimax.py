__nb_iter = 30

def evaluate(game, state, player):
    return 0.5

def minmax(game, state, player, depth, a = -1, b = 1):
    end = game.end(state)
    if end:
        return 0 if end == 3 else -1
    if depth <= 0:
        return evaluate(game, state, player)
    value = -1
    for m in game.get_all_moves(state):
        value = max(value, -minmax(game, game.play(state, m), -player, depth - 1, -b, -a))
        a = max(a, value)
        if a >= b:
            break
    return value

def play(game, state, player, depth=8, nb_iter=30):
    move = None
    a = -2
    __nb_iter = nb_iter
    moves = game.get_all_moves(state)
    waiting = ""
    print(f"\r[{waiting:<{len(moves)}}] {100*len(waiting)//len(moves)}%", end="")
    for m in moves:
        val = -minmax(game, game.play(state, m), -player, depth - 1, b = -a)
        if val > a:
            a = val
            move = m
        waiting += "#"
        print(f"\r[{waiting:<{len(moves)}}] {100*len(waiting)//len(moves)}%", end="")
    print()
    print(f"Confidence: {a/2 + 0.5}")
    return move
