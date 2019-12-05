import copy
from MCTS.uct import UCT
import numpy as np

class Node():
    def __init__(self, state, player, parent, move_parent):
        self.state = state
        self.move_parent = move_parent
        self.parent = parent
        self.children = []
        self.original_player = player
        self.player = player
        self.opponent = 3-player
        self.visit_count = 0
        self.win_score = 0
        self.expanded = False
    
    def apply_move(self, move):
        self.state.play(move)
        self.player = 3 - self.player
        self.opponent = 3 - self.opponent 

    def random_move(self):
        moves = self.state.get_all_moves()
        if moves.size == 0:
            return False
        move = np.random.choice(moves,1)[0]
        self.apply_move(move)
        return True

    def print(self):
        #self.state.print_state()
        print("counts", self.move_parent, self.visit_count, "winsc", self.win_score)
        #print("Node", self.move_parent, len(self.children))
        self.print_children()

    def print_children(self):
        for c in self.children:
            #print("move : ", c.move_parent)
            c.print()
        
    def add_child(self, state, player, move_parent):
        self.children.append(Node(state, player, self, move_parent))
    
    def expand(self):
        if self.expanded:
            return

        moves = self.state.get_all_moves()
        
        for move in moves:
            new_board = copy.deepcopy(self.state)
            new_board.play(move)
            self.add_child(new_board, self.opponent, move)
        
        self.expanded = True
    
    def simulate_playout(self):

        copy_node = copy.deepcopy(self)
        #self.state.print_state()
        if copy_node.state.end() == (3-self.player):
            self.win_score = -np.inf
            return (3-self.player)

        # if copy_node.state.end() == self.player:
        #     self.win_score = np.inf
        #     return self.player
        
        while copy_node.random_move() and not copy_node.state.end():
            continue
        
        #self.state.print_state()
        return copy_node.state.end()

    def back_prop(self, player):
        t_node = self
        while(t_node is not None):
            t_node.visit_count += 1

            #opponent and not a draw
            if t_node.original_player == player and player:
                t_node.win_score += 10
            
            # if t_node.original_player == player and player:
            #     t_node.win_score -= 10
            
            t_node = t_node.parent

    
    def get_child_max_score(self):
        return max(self.children, key=lambda n : n.win_score)

    def find_best_node(self):
        return max(self.children, key=lambda n : UCT(n.parent.visit_count, n.win_score, n.visit_count))

    def select_promising_node(self):
        node = self
        while node.children:
            node = node.find_best_node()
        return node


    # def pprint(self):
    #     print(self.data)
    #     for i in self.children:
    #         i.pprint()
