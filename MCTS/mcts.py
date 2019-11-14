# https://web.stanford.edu/~surag/posts/alphazero.html
# https://www.baeldung.com/java-monte-carlo-tree-search

from MCTS.tree import Node
import random

class MCTS:
    def __init__(self, player):
        self.player = player

    def find_next_move(self, state, nb_iter):
        root = Node(state, self.player, None, None)
        for i in range(nb_iter):
            promising = root.select_promising_node()
            promising.expand()

            if promising.children:
                explore = random.choice(promising.children)
            else:
                explore = promising
            
            result = explore.simulate_playout()
            explore.back_prop(result)


        winner_node = root.get_child_max_score()
        return winner_node.move_parent

   

# if __name__ == "__main__":
#     tictactoe = TicTacToe()
#     mcts = MCTS()
#     test = mcts.find_next_move(tictactoe.board, 1)
#     tictactoe.play(test, 1)
#     tictactoe.print_state()
#     #print(test)