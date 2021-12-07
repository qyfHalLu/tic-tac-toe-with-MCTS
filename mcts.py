from mctsnodes import MCTSNode


class MCTS:  # Monte Carlo tree search (MCTS)
    def __init__(self, node: MCTSNode):
        self.root = node

    # Get the best action after chosen number of loops
    def best_action(self, simulations_times):
        for _ in range(0, simulations_times):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.root.best_child(c_param=0.)

    def tree_policy(self):  # MCTS policy
        current_node = self.root
        while not current_node.terminal_node():
            if not current_node.fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
