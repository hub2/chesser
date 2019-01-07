#!/usr/bin/env python3

import chess
import chess.polyglot
import time

piece_types_no_king = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
piece_types = piece_types_no_king + [chess.KING]

pawns = [ 0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
         5,  5, 10, 25, 25, 10,  5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5, -5,-10,  0,  0,-10, -5,  5,
         5, 10, 10,-20,-20, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0]

knights = [-50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50,]

bishops = [-20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20,]
rooks = [  0,  0,  0,  0,  0,  0,  0,  0,
          5, 10, 10, 10, 10, 10, 10,  5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
          0,  0,  0,  5,  5,  0,  0,  0]

queen = [-20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20]

king_middle_game = [-30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -20,-30,-30,-40,-40,-30,-30,-20,
                    -10,-20,-20,-20,-20,-20,-20,-10,
                     20, 20,  0,  0,  0,  0, 20, 20,
                     20, 30, 10,  0,  0, 10, 30, 20]

king_end_game = [-50,-40,-30,-20,-20,-30,-40,-50,
                -30,-20,-10,  0,  0,-10,-20,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-30,  0,  0,  0,  0,-30,-30,
                -50,-30,-30,-30,-30,-30,-30,-50]

piece_val = {chess.PAWN:100,
             chess.KNIGHT: 320,
             chess.BISHOP: 330,
             chess.ROOK: 500,
             chess.QUEEN: 900,
             chess.KING: 0}

attack_square_val = {chess.PAWN:1,
             chess.KNIGHT: 4,
             chess.BISHOP: 2,
             chess.ROOK: 2,
             chess.QUEEN: 2,
             chess.KING: 0}

MINVALUE = -1000000
MAXVALUE = 1000000

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
        self.pieces = board.pieces
        self.attacks = board.attacks
        self.is_capture = board.is_capture

        if len(board.pieces(chess.QUEEN, chess.BLACK)) + len(board.pieces(chess.QUEEN, chess.WHITE)) == 0:
            self.is_endgame = True
        else:
            self.is_endgame = False

        val, move = self.alpha_beta_search(board, depth, MINVALUE, MAXVALUE, is_white)

        return val/100.0, move

    def alpha_beta_search(self, board, depth, alpha, beta, maximizing_player):
        legal_moves = list(board.legal_moves)
        self.nodes += 1
        if depth == 0 or len(legal_moves) == 0:
            return self.eval_func(board), None
        if board.is_game_over():
            if board.is_checkmate():
                if board.result == '1-0':
                    return MAXVALUE, None
                if board.result == '0-1':
                    return MINVALUE, None

            return self.eval_func(board), None

        legal_moves = sorted(legal_moves, key=self.is_capture, reverse=True)
        if depth < 2:
            legal_moves = legal_moves[:5]
        best_move = None
        # opponent's node
        if not maximizing_player: #not board.turn == side_to_move:
            v_min = MAXVALUE
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
            v_max = MINVALUE
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
        for piece_type in piece_types_no_king:
            pieces_set = self.pieces(piece_type, chess.WHITE)
            pieces_count = 0
            for square in pieces_set:
                mobility += self.attacks(square).__len__()
                pieces_count += 1

            v += pieces_count * piece_val[piece_type]
            #    v += piece_val[piece_type]

        for piece_type in piece_types_no_king:
            pieces_set = self.pieces(piece_type, chess.BLACK)
            pieces_count = 0
            for square in pieces_set:
                mobility -= self.attacks(square).__len__()
                pieces_count += 1
            v -= pieces_count * piece_val[piece_type]

            #    v -= piece_val[piece_type]
        # MOBILITY
        v += mobility

        white_king = board.king(chess.WHITE)
        file = white_king & 7
        rank = white_king >> 3
        file ^= (file - 4) >> 8
        rank ^= (rank - 4) >> 8
        manhattan_dist_w = 2 << ((file + rank) & 7)


        black_king = board.king(chess.BLACK)

        file = black_king & 7
        rank = black_king >> 3
        file ^= (file - 4) >> 8
        rank ^= (rank - 4) >> 8
        manhattan_dist_b = 2 << ((file + rank) & 7)

        # KING
        if not self.is_endgame:
            v += manhattan_dist_w
            v -= manhattan_dist_b
        else:
            v -= manhattan_dist_w
            v += manhattan_dist_b


        # bak = board.turn
        #
        # board.turn = chess.WHITE
        # eval_moves += board.legal_moves.count()
        # board.turn = chess.BLACK
        # eval_moves -= board.legal_moves.count()
        #
        # board.turn = bak

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
