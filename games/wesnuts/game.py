import numpy as np
class Unit:
    def __init__(self, hp, attack, coords, side, char):
        self.hp = hp
        self.attack = attack
        self.coords = coords
        self.side = side
        self.char = char
    def play(self, action, game):
        if self.hp <= 0:
            return
        moved = 0
        if action == 0:
            moved = self.move(1, 0, game)
        elif action == 1:
            moved = self.move(0, 1, game)
        elif action == 2:
            moved = self.move(-1, 0, game)
        else:
            moved = self.move(0, -1, game)
        if moved != 0 and moved != 1:
            moved.hp = max(0, moved.hp - self.attack)

    def move(self, dx, dy, game):
        x = max(0, min(len(game.grid) - 1, self.coords[0] + dx))
        y = max(0, min(len(game.grid) - 1, self.coords[1] + dy))
        if game.grid[x, y] == None:
            game.grid[x, y] = self
            game.grid[self.coords] = None
            self.coords = (x, y)
            return 0 # moved
        if x == self.coords[0] and y == self.coords[1]:
            return 1 # can't move
        else:
            return game.grid[x, y] # attack

class Wesnuts:
    def __init__(self):
        self.grid = np.array([[None for _ in range(9)] for _ in range(9)])
        self.player = 1
        self.units = (
                Unit(3, 1, (3, 3), 1, "☺"),
                Unit(3, 1, (5, 3), 1, "☺"),
                Unit(3, 1, (3, 5), 2, "☻"),
                Unit(3, 1, (5, 5), 2, "☻"))
        for u in self.units:
            self.grid[u.coords] = u
        self.turn = 0

    def get_all_moves(self):
        return list(range(16))

    def print_state(self):
        print(f"Unit 1: {self.units[0].hp} hp")
        print(f"Unit 2: {self.units[1].hp} hp")
        print("┌─────────┐")
        for i in range(9):
            print("│", end="")
            for j in range(9):
                if self.grid[j, i] == None:
                    if i == j == 4:
                        print(end="+")
                    else:
                        print(end=" ")
                else:
                    print(end=self.grid[j, i].char)
            print("│")
        print("└─────────┘")
        print(f"Unit 3: {self.units[2].hp} hp")
        print(f"Unit 4: {self.units[3].hp} hp")
        print()

    def play(self, action):
        if self.player == 1:
            self.units[0].play(action % 4, self)
            self.units[1].play(action // 4, self)
        else:
            self.units[2].play(action % 4, self)
            self.units[3].play(action // 4, self)
        
        if self.grid[4, 4] and self.grid[4, 4].hp != 0:
            self.grid[4, 4].hp = min(3, self.grid[4, 4].hp + 1)

        self.player -= 3
        self.player *= -1
        self.turn += 1
        return self

    def end(self):
        total_p1 = self.units[0].hp + self.units[1].hp
        total_p2 = self.units[2].hp + self.units[3].hp
        if self.turn >= 20:
            total = total_p1 - total_p2
            if total == 0:
                return 3
            if total > 0:
                return 1
            return 2
        if total_p1 == 0:
            return 2
        if total_p2 == 0:
            return 1 
        return 0

    def encode_input(self):
        encoded = np.zeros([3,9,9]).astype(np.int)
        for i in range(9):
            for j in range(9):
                if self.grid[i, j]:
                    encoded[self.grid[i, j].side - 1, i, j] = self.grid[i, j].hp
        encoded[2,:,:] = self.player-1 # player to move
        return encoded
