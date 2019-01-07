#!/usr/bin/env python3
import chess
import chess.polyglot
import time

from cpython cimport array
import array

piece_types_no_king = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
piece_types = piece_types_no_king + [chess.KING]

# PAWNS
cdef array.array cpawns = array.array('i', [ 0,  0,  0,  0,  0,  0,  0,  0,
                            50, 50, 50, 50, 50, 50, 50, 50,
                            10, 10, 20, 30, 30, 20, 10, 10,
                             5,  5, 10, 25, 25, 10,  5,  5,
                             0,  0,  0, 20, 20,  0,  0,  0,
                             5, -5,-10,  0,  0,-10, -5,  5,
                             5, 10, 10,-20,-20, 10, 10,  5,
                             0,  0,  0,  0,  0,  0,  0,  0])

cdef int[:] pawns = cpawns
pawns_black = pawns[::-1]

# KNIGHTS
cdef array.array cknights = array.array('i', [-50,-40,-30,-30,-30,-30,-40,-50,
                                            -40,-20,  0,  0,  0,  0,-20,-40,
                                            -30,  0, 10, 15, 15, 10,  0,-30,
                                            -30,  5, 15, 20, 20, 15,  5,-30,
                                            -30,  0, 15, 20, 20, 15,  0,-30,
                                            -30,  5, 10, 15, 15, 10,  5,-30,
                                            -40,-20,  0,  5,  5,  0,-20,-40,
                                            -50,-40,-30,-30,-30,-30,-40,-50,])

cdef int[:] knights = cknights
knights_black = knights[::-1]

# BISHOPS
cdef array.array cbishops = array.array('i', [-20,-10,-10,-10,-10,-10,-10,-20,
                                            -10,  0,  0,  0,  0,  0,  0,-10,
                                            -10,  0,  5, 10, 10,  5,  0,-10,
                                            -10,  5,  5, 10, 10,  5,  5,-10,
                                            -10,  0, 10, 10, 10, 10,  0,-10,
                                            -10, 10, 10, 10, 10, 10, 10,-10,
                                            -10,  5,  0,  0,  0,  0,  5,-10,
                                            -20,-10,-10,-10,-10,-10,-10,-20,])

cdef int[:] bishops = cbishops
bishops_black = bishops[::-1]

# ROOKS
cdef array.array crooks = array.array('i', [  0,  0,  0,  0,  0,  0,  0,  0,
                                          5, 10, 10, 10, 10, 10, 10,  5,
                                         -5,  0,  0,  0,  0,  0,  0, -5,
                                         -5,  0,  0,  0,  0,  0,  0, -5,
                                         -5,  0,  0,  0,  0,  0,  0, -5,
                                         -5,  0,  0,  0,  0,  0,  0, -5,
                                         -5,  0,  0,  0,  0,  0,  0, -5,
                                          0,  0,  0,  5,  5,  0,  0,  0])
cdef int[:] rooks = crooks
rooks_black = rooks[::-1]

# QUEENS
cdef array.array cqueens = array.array('i', [-20,-10,-10, -5, -5,-10,-10,-20,
                                            -10,  0,  0,  0,  0,  0,  0,-10,
                                            -10,  0,  5,  5,  5,  5,  0,-10,
                                             -5,  0,  5,  5,  5,  5,  0, -5,
                                              0,  0,  5,  5,  5,  5,  0, -5,
                                            -10,  5,  5,  5,  5,  5,  0,-10,
                                            -10,  0,  5,  0,  0,  0,  0,-10,
                                            -20,-10,-10, -5, -5,-10,-10,-20])

cdef int[:] queens = cqueens
queens_black = queens[::-1]

# KINGS
cdef array.array cking_middle_game = array.array('i', [-30,-40,-40,-50,-50,-40,-40,-30,
                                                        -30,-40,-40,-50,-50,-40,-40,-30,
                                                        -30,-40,-40,-50,-50,-40,-40,-30,
                                                        -30,-40,-40,-50,-50,-40,-40,-30,
                                                        -20,-30,-30,-40,-40,-30,-30,-20,
                                                        -10,-20,-20,-20,-20,-20,-20,-10,
                                                         20, 20,  0,  0,  0,  0, 20, 20,
                                                         20, 30, 10,  0,  0, 10, 30, 20])

cdef int[:] king_middle_game = cking_middle_game
king_middle_game_black = king_middle_game[::-1]

cdef array.array cking_end_game = array.array('i', [-50,-40,-30,-20,-20,-30,-40,-50,
                                                    -30,-20,-10,  0,  0,-10,-20,-30,
                                                    -30,-10, 20, 30, 30, 20,-10,-30,
                                                    -30,-10, 30, 40, 40, 30,-10,-30,
                                                    -30,-10, 30, 40, 40, 30,-10,-30,
                                                    -30,-10, 20, 30, 30, 20,-10,-30,
                                                    -30,-30,  0,  0,  0,  0,-30,-30,
                                                    -50,-30,-30,-30,-30,-30,-30,-50])

cdef int[:] king_end_game = cking_end_game
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
    cache = {}
    def put(self, board, val):
        h = chess.polyglot.zobrist_hash(board)


    def get(self, board):
        h = chess.polyglot.zobrist_hash(board)
        return self.cache.get(h, None)


color_multiplier = [-1, 1]

class AlphaBetaSearch:
    nodes = 0
    def __init__(self):
        self.transposition_table = TTable()
        self.last_pv = None

    def minimax(self, board, max_depth, is_white):
        self.max_depth = max_depth
        self.nodes = 0
        self.pieces = board.pieces
        self.attacks = board.attacks
        self.is_capture = board.is_capture

        if len(board.pieces(chess.QUEEN, chess.BLACK)) + len(board.pieces(chess.QUEEN, chess.WHITE)) == 0:
            self.is_endgame = True
        else:
            self.is_endgame = False

        val, move, tpv = self.alpha_beta_search(board, 0, MINVALUE, MAXVALUE, is_white)
        self.last_pv = tpv[::-1]
        print(" ".join([x.uci() for x in tpv[::-1]]))

        return val/100.0, move

    def alpha_beta_search(self, board, depth, alpha, beta, maximizing_player):
        color = color_multiplier[board.turn]

        legal_moves = list(board.legal_moves)
        self.nodes += 1

        if depth >= self.max_depth or len(legal_moves) == 0:
            return self.eval_func(board, color), None, []
        if board.is_game_over():
            if board.is_checkmate():
                if board.result == '1-0':
                    return MAXVALUE, None
                if board.result == '0-1':
                    return MINVALUE, None

            return self.eval_func(board, color), None, []

        legal_moves = sorted(legal_moves, key=self.is_capture, reverse=True)
        #if depth > 6:
        #    legal_moves = legal_moves[:2]
        #if depth > 5:
        #    legal_moves = legal_moves[:5]

        best_move = None

        v_max = MINVALUE
        for move in legal_moves:
            board.push(move)
            v, _, ttpv = self.alpha_beta_search(board, depth+1, -beta, -alpha, not maximizing_player)
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

        cdef int v = 0
        #eval_moves = 0
        #for piece_type in piece_types_no_king:
        #    pieces_set = self.pieces(piece_type, chess.WHITE)
        #    pieces_count = 0
        #    for square in pieces_set:
        #        v += self.attacks(square).__len__()
        #        pieces_count += 1

        #    v += pieces_count * piece_val[piece_type]
        #    #    v += piece_val[piece_type]

        #for piece_type in piece_types_no_king:
        #    pieces_set = self.pieces(piece_type, chess.BLACK)
        #    pieces_count = 0
        #    for square in pieces_set:
        #        v -= self.attacks(square).__len__()
        #        pieces_count += 1
        #    v -= pieces_count * piece_val[piece_type]

        #    #    v -= piece_val[piece_type]

        cdef int i
        cdef unsigned long long white_bishops = (board.bishops & board.occupied_co[1])
        for i in range(64):
            if (white_bishops & 1):
                v += bishops[i]
            white_bishops = white_bishops >> i

        cdef unsigned long long black_bishops = (board.bishops & board.occupied_co[0])
        for i in range(64):
            if (black_bishops & 1):
                v -= bishops_black[i]
            black_bishops = black_bishops >> i

        cdef unsigned long long white_queens = (board.queens & board.occupied_co[1])
        for i in range(64):
            if (white_queens & 1):
                v += queens[i]
            white_queens = white_queens >> i

        cdef unsigned long long black_queens = (board.queens & board.occupied_co[0])
        for i in range(64):
            if (black_queens & 1):
                v -= queens_black[i]
            black_queens = black_queens >> i

        cdef unsigned long long white_knights = (board.knights & board.occupied_co[1])
        for i in range(64):
            if (white_knights & 1):
                v += knights[i]
            white_knights = white_knights >> i

        cdef unsigned long long black_knights = (board.knights & board.occupied_co[0])
        for i in range(64):
            if (black_knights & 1):
                v -= knights_black[i]
            black_knights = black_knights >> i

        cdef unsigned long long white_pawns = (board.pawns & board.occupied_co[1])
        for i in range(64):
            if (white_pawns & 1):
                v += pawns[i]
            white_pawns = white_pawns >> i

        cdef unsigned long long black_pawns = (board.pawns & board.occupied_co[0])
        for i in range(64):
            if (black_pawns & 1):
                v -= pawns_black[i]
            black_pawns = black_pawns >> i

        cdef unsigned long long white_king = (board.kings & board.occupied_co[1])
        cdef unsigned long long black_king = (board.kings & board.occupied_co[0])
        # KING
        if self.is_endgame:
            for i in range(64):
                if (white_king & 1):
                    v += king_end_game[i]
                white_king = white_king >> i

            for i in range(64):
                if (black_king & 1):
                    v -= king_end_game_black[i]
                black_king = black_king >> i

        else:
            for i in range(64):
                if (white_king & 1):
                    v += king_middle_game[i]
                white_king = white_king >> i

            for i in range(64):
                if (black_king & 1):
                    v -= king_middle_game_black[i]
                black_king = black_king >> i

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


board = chess.Board()

ab = AlphaBetaSearch()
for depth in range(1, 9):
    s = time.time()
    val, move = ab.minimax(board, depth, board.turn)
    e = time.time()
    delta = e-s
    print(val, move, ab.nodes, delta, ab.nodes/(delta))
