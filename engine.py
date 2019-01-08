#!/usr/bin/env pypy3

import chess
import chess.polyglot
import time
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

piece_types_no_king = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
piece_types = piece_types_no_king + [chess.KING]

piece_attack_units = {chess.KNIGHT: 2, chess.BISHOP: 2, chess.QUEEN: 5, chess.ROOK: 3, chess.PAWN: 1, chess.KING:0}
king_safety = [
    0,  0,   1,   2,   3,   5,   7,   9,  12,  15,
  18,  22,  26,  30,  35,  39,  44,  50,  56,  62,
  68,  75,  82,  85,  89,  97, 105, 113, 122, 131,
 140, 150, 169, 180, 191, 202, 213, 225, 237, 248,
 260, 272, 283, 295, 307, 319, 330, 342, 354, 366,
 377, 389, 401, 412, 424, 436, 448, 459, 471, 483,
 494, 500, 500, 500, 500, 500, 500, 500, 500, 500,
 500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
 500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
 500, 500, 500, 500, 500, 500, 500, 500, 500, 500
]

pawns = [ 0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
         5,  5, 10, 25, 25, 10,  5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5, -5,-10,  0,  0,-10, -5,  5,
         5, 10, 10,-20,-20, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0]
pawns_black = pawns[::-1]

knights = [-50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50,]


knights_black = knights[::-1]

bishops = [-20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20,]

bishops_black = bishops[::-1]

rooks = [  0,  0,  0,  0,  0,  0,  0,  0,
          5, 10, 10, 10, 10, 10, 10,  5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
          0,  0,  0,  5,  5,  0,  0,  0]

rooks_black = rooks[::-1]

queens = [-20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20]


queens_black = queens[::-1]

king_middle_game = [-30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -20,-30,-30,-40,-40,-30,-30,-20,
                    -10,-20,-20,-20,-20,-20,-20,-10,
                     20, 20,  0,  0,  0,  0, 20, 20,
                     20, 30, 10,  0,  0, 10, 30, 20]

king_middle_game_black = king_middle_game[::-1]

king_end_game = [-50,-40,-30,-20,-20,-30,-40,-50,
                -30,-20,-10,  0,  0,-10,-20,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-30,  0,  0,  0,  0,-30,-30,
                -50,-30,-30,-30,-30,-30,-30,-50]

king_end_game_black = king_end_game[::-1]

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

class TTable:
    def __init__(self):
        self.cache = {}

    def put(self, board, val, depth, move, pv, FLAG):
        h = chess.polyglot.zobrist_hash(board)
        self.cache[h] = (val, depth, move, pv, FLAG)

    def get(self, board):
        h = chess.polyglot.zobrist_hash(board)
        return self.cache.get(h, None)


color_multiplier = [-1, 1]

EXACT = 1
LOWERBOUND = 2
UPPERBOUND = 2

class AlphaBetaSearch:
    nodes = 0
    def __init__(self):
        self.last_pv = None

    def search(self, board, depth):
        self.transposition_table = TTable()
        for i in range(1, depth+1):
            s = time.time()
            val, move = self.minimax(board, i, board.turn)
            e = time.time()
            usedtime = (e-s)*1000

            print('info depth {} score {} time {} nodes {}'.format(i, val, int(usedtime), self.nodes))
            eprint('info depth {} score {} time {} nodes {}'.format(i, val, int(usedtime), self.nodes))
        return val, move

    def minimax(self, board, depth, is_white):
        self.nodes = 0
        self.pieces = board.pieces
        self.attacks = board.attacks
        self.is_capture = board.is_capture

        if len(board.pieces(chess.QUEEN, chess.BLACK)) + len(board.pieces(chess.QUEEN, chess.WHITE)) == 0:
            self.is_endgame = True
        else:
            self.is_endgame = False

        val, move, tpv = self.alpha_beta_search(board, depth, MINVALUE, MAXVALUE, is_white)
        self.last_pv = tpv[::-1]
        eprint(" ".join([x.uci() for x in tpv[::-1]]))

        color = color_multiplier[board.turn]

        return color * val/100.0, move

    def alpha_beta_search(self, board, depth, alpha, beta, maximizing_player):
        alpha_orig = alpha
        probe = self.transposition_table.get(board)
        if probe is not None:
            if probe[1] >= depth:
                if probe[4] == EXACT:
                    return probe[0], probe[2], probe[3]
                elif probe[4] == LOWERBOUND:
                    alpha = max(alpha, probe[0])
                elif probe[4] == UPPERBOUND:
                    beta = min(beta, probe[0])
            if alpha >= beta:
                return probe[0], probe[2], probe[3]

        color = color_multiplier[board.turn]

        legal_moves = list(board.legal_moves)
        self.nodes += 1

        if depth == 0 or len(legal_moves) == 0:
            val = self.eval_func(board, color)
            return val, None, []

        legal_moves = sorted(legal_moves, key=self.is_capture, reverse=True)

        best_move = None

        v_max = MINVALUE
        for move in legal_moves:
            board.push(move)
            v, _, ttpv = self.alpha_beta_search(board, depth-1, -beta, -alpha, not maximizing_player)
            v = -v
            v = max(alpha, v)
            alpha = max(alpha, v)

            if v > v_max:
                v_max = v
                best_move = move
                tpv = ttpv + [best_move]

            board.pop()
            if alpha >= beta:
                break

        flag = EXACT
        if v_max <= alpha_orig:
            flag = UPPERBOUND
        elif v_max >= beta:
            flag = LOWERBOUND

        self.transposition_table.put(board, v_max, depth, best_move, tpv, flag)
        return v_max, best_move, tpv


        # opponent's node
        #if not maximizing_player: #not board.turn == side_to_move:
        #    v_min = MAXVALUE
        #    for move in legal_moves:
        #        board.push(move)
        #        temp_min, _ = self.alpha_beta_search(board, depth+1, alpha, beta, not maximizing_player)

        #        if temp_min < v_min:
        #            v_min = temp_min
        #            best_move = move

        #        beta = min(beta, v_min)
        #        board.pop()
        #        if alpha >= beta:
        #            break
        #    return beta, best_move
        #else:
        #    v_max = MINVALUE
        #    for move in legal_moves:
        #        board.push(move)
        #        temp_max, _ = self.alpha_beta_search(board, depth+1, alpha, beta, not maximizing_player)

        #        if temp_max > v_max:
        #            v_max = temp_max
        #            best_move = move

        #        alpha = max(alpha, temp_max)
        #        board.pop()
        #        if alpha >= beta:
        #            break
        #    return alpha, best_move

    def eval_func(self, board, color):
        # val = self.cache.get(board)
        # if val is not None:
        #     return val

        if board.is_game_over():
            if board.is_checkmate():
                if board.result == '1-0':
                    return MAXVALUE * color
                if board.result == '0-1':
                    return MINVALUE * color
        v = 0
        #eval_moves = 0
        for piece_type in piece_types_no_king:
            pieces_set = self.pieces(piece_type, chess.WHITE)
            pieces_count = 0
            for square in pieces_set:
                v += self.attacks(square).__len__()
                pieces_count += 1

            v += pieces_count * piece_val[piece_type]
            #    v += piece_val[piece_type]

        for piece_type in piece_types_no_king:
            pieces_set = self.pieces(piece_type, chess.BLACK)
            pieces_count = 0
            for square in pieces_set:
                v -= self.attacks(square).__len__()
                pieces_count += 1
            v -= pieces_count * piece_val[piece_type]

            #    v -= piece_val[piece_type]

        for bishop in board.pieces(chess.BISHOP, chess.WHITE):
            v += bishops[bishop]

        for bishop in board.pieces(chess.BISHOP, chess.BLACK):
            v -= bishops_black[bishop]

        for queen in board.pieces(chess.QUEEN, chess.WHITE):
            v += queens[queen]

        for queen in board.pieces(chess.QUEEN, chess.BLACK):
            v -= queens_black[queen]

        for knight in board.pieces(chess.KNIGHT, chess.WHITE):
            v += knights[knight]

        for knight in board.pieces(chess.KNIGHT, chess.BLACK):
            v -= knights_black[knight]

        for pawn in board.pieces(chess.PAWN, chess.WHITE):
            v += pawns[pawn]

        for pawn in board.pieces(chess.PAWN, chess.BLACK):
            v -= pawns_black[pawn]

        white_king = board.king(chess.WHITE)
        black_king = board.king(chess.BLACK)

        # KING
        if self.is_endgame:
            v += king_end_game[white_king]
            v -= king_end_game_black[black_king]
        else:
            v += king_middle_game[white_king]
            v -= king_middle_game_black[black_king]

        # WHITE SAFETY
        attk_units = 0
        for neighbouring_square in board.attacks(white_king):
            for attacked_square in board.attackers(chess.BLACK, neighbouring_square):
                attk_units += piece_attack_units[board.piece_type_at(attacked_square)]
        v -= king_safety[attk_units]

        # BLACK SAFETY
        attk_units = 0
        for neighbouring_square in board.attacks(black_king):
            for attacked_square in board.attackers(chess.WHITE, neighbouring_square):
                attk_units += piece_attack_units[board.piece_type_at(attacked_square)]
        v += king_safety[attk_units]

        # bak = board.turn
        #
        # board.turn = chess.WHITE
        # eval_moves += board.legal_moves.count()
        # board.turn = chess.BLACK
        # eval_moves -= board.legal_moves.count()
        #
        # board.turn = bak

        v *= color

        return v

if __name__ == '__main__':
    board = chess.Board()

    ab = AlphaBetaSearch()
    ab.search(board, 8)

