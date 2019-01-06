#!/usr/bin/env python3

import chess
import time

piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
piece_val = {chess.PAWN:100,
             chess.KNIGHT: 300,
             chess.BISHOP: 310,
             chess.ROOK: 500,
             chess.QUEEN: 950,
             chess.KING: 0}

attack_square_val = {chess.PAWN:1,
             chess.KNIGHT: 4,
             chess.BISHOP: 2,
             chess.ROOK: 2,
             chess.QUEEN: 2,
             chess.KING: 0}

class LRUCache:
    cache = {}
    def put(self, board, val):
        bb = (board.pawns) | \
             (board.knights << 64) | \
             (board.bishops << 128) | \
             (board.rooks << 192) | \
             (board.queens << 256) | \
             (board.kings << 318)
        self.cache[bb] = val

    def get(self, board):
        bb = (board.pawns) | \
             (board.knights << 64) | \
             (board.bishops << 128) | \
             (board.rooks << 192) | \
             (board.queens << 256) | \
             (board.kings << 318)
        return self.cache.get(bb, None)




class AlphaBetaSearch:
    nodes = 0
    def __init__(self):
        self.cache = LRUCache()

    def minimax(self, board, depth, is_white):
        self.nodes = 0
        val, move = self.alpha_beta_search(board, depth, -float('inf'), float('inf'), is_white)
        return val/100.0, move

    def alpha_beta_search(self, board, depth, alpha, beta, maximizing_player):
        legal_moves = list(board.legal_moves)
        self.nodes += 1
        if depth == 0 or len(legal_moves) == 0:
            return self.eval_func(board), None
        if board.is_game_over():
            if board.is_checkmate():
                if board.result == '1-0':
                    return float('inf'), None
                if board.result == '0-1':
                    return -float('inf'), None

            return self.eval_func(board), None

        legal_moves = sorted(legal_moves, key=board.is_capture, reverse=True)
        if depth < 2:
            legal_moves = legal_moves[:5]
        best_move = None
        # opponent's node
        if not maximizing_player: #not board.turn == side_to_move:
            v_min = float('inf')
            for move in legal_moves:
                board.push(move)
                temp_min, _ = self.alpha_beta_search(board, depth-1, alpha, beta, not maximizing_player)

                if temp_min < v_min:
                    v_min = temp_min
                    best_move = move

                beta = min(beta, v_min)
                board.pop()
                if alpha >= beta:
                    break
            return beta, best_move
        else:
            v_max = -float('inf')
            for move in legal_moves:
                board.push(move)
                temp_max, _ = self.alpha_beta_search(board, depth-1, alpha, beta, not maximizing_player)

                if temp_max > v_max:
                    v_max = temp_max
                    best_move = move

                alpha = max(alpha, temp_max)
                board.pop()
                if alpha >= beta:
                    break
            return alpha, best_move

    def eval_func(self, board):
        # val = self.cache.get(board)
        # if val is not None:
        #     return val

        v = 0
        mobility = 0
        #eval_moves = 0

        for piece_type in piece_types:
            v += len(board.pieces(piece_type, chess.WHITE)) * piece_val[piece_type]
            for square in board.pieces(piece_type, chess.WHITE):
                mobility += len(board.attacks(square))
            #    v += piece_val[piece_type]

        for piece_type in piece_types:
            v -= len(board.pieces(piece_type, chess.BLACK)) * piece_val[piece_type]
            for square in board.pieces(piece_type, chess.BLACK):
                mobility -= len(board.attacks(square))

            #    v -= piece_val[piece_type]

        # bak = board.turn
        #
        # board.turn = chess.WHITE
        # eval_moves += board.legal_moves.count()
        # board.turn = chess.BLACK
        # eval_moves -= board.legal_moves.count()
        #
        # board.turn = bak

        v += mobility
        #v += eval_moves
        return v


if __name__ == '__main__':
    board = chess.Board()

    ab = AlphaBetaSearch()
    for depth in range(9):
        s = time.time()
        val, move = ab.minimax(board, depth, board.turn)
        e = time.time()
        delta = e-s
        print(val, move, ab.nodes, delta, ab.nodes/(delta))
