#!/usr/bin/env python3

import chess


class AlphaBetaSearch:
    def __init__(self, side_to_move):
        self.eval_func = eval_func
        self.side_to_move = side_to_move

    def minimax(self, oard, depth=2):
        return self.alpha_beta_search(board, depth, -float('inf'), float('inf'))

    def alpha_beta_search(self, board, depth=2, alpha, beta):
        if board.is_game_over() or depth == 0:
            return eval_func(board)

        # opponent's node
        if not board.turn == side_to_move:
            for move in board.legal_moves():
                board.push(move)
                beta = min(beta, self.alpha_beta_search(board, depth-1, alpha, beta))
                board.pop(move)
                if alpha >= beta:
                    break
            return beta
        else:
            for move in board.legal_moves():
                board.push(move)
                alpha = max(alpha, self.alpha_beta_search(board, depth-1, alpha, beta))
                board.pop(move)
                if alpha >= beta:
                    break
            return alpha


    def eval_func(self, board):
        for piece in board.pieces():
            print(piece)

