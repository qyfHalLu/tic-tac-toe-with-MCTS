import numpy as np
from mctsnodes import *
from mcts import MCTS
from tictactoeboard import TicTacToeState
import random

mt = 0
rt = 0
tt = 0
at = 0
rside = -1


def init():  # Initialization
    state = np.zeros((3, 3))  # Initialize board (3*3)
    state[0, 1] = -1
    state[1, 1] = 1
    state[1, 0] = 1
    state[1, 2] = -1
    initial_board_state = TicTacToeState(state=state, next_to_move=1)
    root = MCTSNode(state=initial_board_state, parent=None)
    mcts = MCTS(root)
    best_node = mcts.best_action(500)
    new_state = best_node.state
    new_board = new_state.board
    return new_state, new_board


def graphics(board):  # Display board
    for i in range(3):
        print("")
        print("{0:3}".format(i).center(8)+"|", end='')
        for j in range(3):
            if new_board[i][j] == 0:
                print('_'.center(8), end='')
            if new_board[i][j] == 1:
                print('X'.center(8), end='')
            if new_board[i][j] == -1:
                print('O'.center(8), end='')
    print("")
    print("______________________________")


def agent_random(board):  # Ramdom player, random moves
    ri = random.randint(0, 2)
    rj = random.randint(0, 2)
    while board[ri][rj] != 0:
        ri = random.randint(0, 2)
        rj = random.randint(0, 2)
    return ri, rj


def get_action(state):  # Get random player's move and update to the board
    try:  # Then determine if the move is legal
        x, y = agent_random(state.board)
        move = TicTacToeMove(x, y, rside)
    except Exception as e:
        move = -1
    if move == -1 or not state.move_legal(move):
        print("invalid move")
        move = get_action(state)
    return move


def judge(state):  # Determine win/lose
    global mt, rt, tt, at
    if state.game_over():
        if state.game_result == 1.0:
            print("MCTS Win!")
            mt += 1
            at += 1
        if state.game_result == 0.0:
            print("Tie!")
            tt += 1
            at += 1
        if state.game_result == -1.0:
            print("Random Agent Win!")
            rt += 1
            at += 1
        return 1
    else:
        return -1


for i in range(0, 100):  # Play 100 games
    print(at + 1, 'game :')
    while True:
        new_state, n_board = init()
        move1 = get_action(new_state)
        new_state = new_state.move(move1)
        new_board = new_state.board

        board_state = TicTacToeState(state=new_board, next_to_move=1)
        root = MCTSNode(state=board_state, parent=None)
        mcts = MCTS(root)
        # Return best moves after 500 simulations
        best_node = mcts.best_action(500)
        new_state = best_node.state
        new_board = new_state.board
        if judge(new_state) == 1:
            graphics(new_board)
            break
        elif judge(new_state) == -1:
            continue

print('Total Games Played: ', at)
print('MCTS Win Rate: ', float(mt/at)*100, '%')
print('Tie Rate: ', float(tt/at)*100, '%')
print('Random Agent Win Rate: ', float(rt/at)*100, '%')
