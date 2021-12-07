import numpy as np


class TicTacToeMove(object):    # Class for game moves
    def __init__(self, x_coordinate, y_coordinate, value):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value

    def __repr__(self):  # Print (instance name) = repr return data
        return "x:" + str(self.x_coordinate) + " y:" + str(self.y_coordinate) + " v:" + str(self.value)


class TicTacToeState(object):   # Class for game states
    x = 1
    o = -1

    # Determine if board size matches tic tac toe board
    def __init__(self, state, next_to_move=1):
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Please play on 2D square board")
        # Define some basic attributes
        self.board = state
        self.board_size = state.shape[0]
        self.next_to_move = next_to_move

    @property
    def game_result(self):   # Determine game result
        rowsum = np.sum(self.board, 0)
        colsum = np.sum(self.board, 1)
        diag_sum_tl = self.board.trace()
        diag_sum_tr = self.board[::-1].trace()

        if any(rowsum == self.board_size) or any(
                colsum == self.board_size) or diag_sum_tl == self.board_size or diag_sum_tr == self.board_size:
            return 1.
        elif any(rowsum == -self.board_size) or any(
                colsum == -self.board_size) or diag_sum_tl == -self.board_size or diag_sum_tr == -self.board_size:

            return -1.
        elif np.all(self.board != 0):
            return 0.
        else:
            return None

    def game_over(self):  # Geme over: return 1, not over: return 0
        return self.game_result != None

    def move_legal(self, move):  # Determine the player's move's location and validity
        if move.value != self.next_to_move:
            return False

        x_in_range = move.x_coordinate < self.board_size and move.x_coordinate >= 0
        if not x_in_range:
            return False

        y_in_range = move.y_coordinate < self.board_size and move.y_coordinate >= 0
        if not y_in_range:
            return False

        return self.board[move.x_coordinate, move.y_coordinate] == 0

    def move(self, move):   # Update the move's location in the board and update the new board states in the board's class
        if not self.move_legal(move):
            raise ValueError("move " + move + " on board " +
                             self.board + " is not legal")
        new_board = np.copy(self.board)
        new_board[move.x_coordinate, move.y_coordinate] = move.value
        next_to_move = TicTacToeState.o if self.next_to_move == TicTacToeState.x else TicTacToeState.x
        return TicTacToeState(new_board, next_to_move)

    def actions_legal(self):    # Determien if the move is legal
        indices = np.where(self.board == 0)
        return [TicTacToeMove(coords[0], coords[1], self.next_to_move) for coords in list(zip(indices[0], indices[1]))]
