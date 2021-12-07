import numpy as np
from collections import defaultdict
from tictactoeboard import *


class MCTSNode(object):  # Class for MCTS search nodes
    # Define following attributes: number of visits, nodes, states, parents, and children
    def __init__(self, state: TicTacToeState, parent=None):
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self.state = state
        self.parent = parent
        self.children = []

    @property
    def untried_actions(self):  # Untried moves
        # hasattr() is used to determine if the object has its corresponding attributes
        if not hasattr(self, '_untried_actions'):
            self._untried_actions = self.state.actions_legal()
        return self._untried_actions

    @property
    def q(self):    # Value used for updates
        wins = self._results[self.parent.state.next_to_move]
        loses = self._results[-1 * self.parent.state.next_to_move]
        return wins - loses

    @property
    def n(self):    # Number of visits
        return self._number_of_visits

    def expand(self):   # Expend
        action = self.untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MCTSNode(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def terminal_node(self):    # Determine if it's leaf node
        return self.state.game_over()

    def rollout(self):  # Rollout
        current_rollout_state = self.state
        while not current_rollout_state.game_over():
            possible_moves = current_rollout_state.actions_legal()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result

    def backpropagate(self, result):    # Backpropagation
        self._number_of_visits += 1.
        self._results[result] += 1.
        # Use the final value that rollout gets
        # to update every node's T and N values in the path
        if self.parent:
            self.parent.backpropagate(result)

    def fully_expanded(self):   # Determine if it's fully expanded
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):  # Return the best child node
        choices_weights = []
        for c in self.children:
            choices_weights.append(
                (c.q / (c.n)) + c_param * np.sqrt((2 * np.log(self.n) / (c.n))))

        # Return the biggest index values in a numpy array
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):   # Rollout policy
        return possible_moves[np.random.randint(len(possible_moves))]
