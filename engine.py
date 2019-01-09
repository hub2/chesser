#!/usr/bin/env pypy3

import chess
import chess.polyglot
import time
import sys
from heapq import heappush, heappop


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
        self.WHITE = chess.WHITE
        self.BLACK = chess.BLACK
        self.PAWN = chess.PAWN
        self.KNIGHT = chess.KNIGHT
        self.BISHOP = chess.BISHOP
        self.QUEEN = chess.QUEEN
        self.KING = chess.KING

    def search(self, board, depth):
        self.pieces_mask = board.pieces_mask
        #self.attacks = board.attacks
        self.is_capture = board.is_capture
        self.scan_forward = chess.scan_forward
        self.attacks_mask = board.attacks_mask
        self.attackers_mask = board.attackers_mask
        self.piece_type_at = board.piece_type_at
        self.transposition_table = TTable()
        for i in range(1, depth+1):
            s = time.time()
            val, move = self.minimax(board, i, board.turn)
            e = time.time()
            usedtime = (e-s)*1000

            print('info depth {} score {} time {} nodes {}'.format(i, val, int(usedtime), self.nodes))
            eprint('info depth {} score {} time {} nodes {}'.format(i, val, int(usedtime), self.nodes))
        return val, move

    def get_pieces(self, piece_type, color):
        return self.scan_forward(self.pieces_mask(piece_type, color))

    def get_attacks(self, square):
        return self.scan_forward(self.attacks_mask(square))

    def get_attackers(self, color, square):
        return self.scan_forward(self.attackers_mask(color, square))

    def minimax(self, board, depth, is_white):
        self.nodes = 0

        if len(board.pieces(chess.QUEEN, chess.BLACK)) + len(board.pieces(chess.QUEEN, chess.WHITE)) == 0:
            self.is_endgame = True
        else:
            self.is_endgame = False

        val, move, tpv = self.alpha_beta_search(board, depth, MINVALUE, MAXVALUE)
        self.last_pv = tpv[::-1]
        eprint(" ".join([x.uci() for x in tpv[::-1]]))

        color = color_multiplier[board.turn]
        return color*val/100.0, move

    def alpha_beta_search(self, board, depth, alpha, beta):
        alpha_orig = alpha
        probe = self.transposition_table.get(board)
        if probe is not None:
            if probe[1] >= depth:
                board.push(probe[2])
                if board.is_valid():
                    if probe[4] == EXACT:
                        board.pop()
                        return probe[0], probe[2], probe[3]
                    elif probe[4] == LOWERBOUND:
                        alpha = max(alpha, probe[0])
                    elif probe[4] == UPPERBOUND:
                        beta = min(beta, probe[0])
                board.pop()

                if alpha >= beta:
                    return probe[0], probe[2], probe[3]

        color = color_multiplier[board.turn]

        legal_moves = board.generate_legal_moves()
        self.nodes += 1

        if depth == 0 or len(legal_moves) == 0:
            val, move, pv = self.quiescent(board, alpha, beta, depth)
            return val, move, pv

        legal_moves = sorted(legal_moves, key=self.is_capture, reverse=True)

        best_move = None
        v_max = MINVALUE
        tpv = []
        for move in legal_moves:
            board.push(move)
            v, _, ttpv = self.alpha_beta_search(board, depth-1, -beta, -alpha)
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

        if board.is_checkmate():
            return MAXVALUE * color

        v = 0
        #eval_moves = 0
        # for piece_type in piece_types_no_king:
        #     pieces_set = self.pieces(piece_type, chess.WHITE)
        #     pieces_count = 0
        #     for square in pieces_set:
        #         v += self.attacks(square).__len__()
        #         pieces_count += 1
        #
        #     v += pieces_count * piece_val[piece_type]
        #     #    v += piece_val[piece_type]
        #
        # for piece_type in piece_types_no_king:
        #     pieces_set = self.pieces(piece_type, chess.BLACK)
        #     pieces_count = 0
        #     for square in pieces_set:
        #         v -= self.attacks(square).__len__()
        #         pieces_count += 1
        #     v -= pieces_count * piece_val[piece_type]

            #    v -= piece_val[piece_type]

        for bishop in self.get_pieces(self.BISHOP, self.WHITE):
            v += bishops[bishop]
            v += piece_val[self.BISHOP]

        for bishop in self.get_pieces(self.BISHOP, self.BLACK):
            v -= bishops_black[bishop]
            v -= piece_val[self.BISHOP]


        for queen in self.get_pieces(self.QUEEN, self.WHITE):
            v += queens[queen]
            v += piece_val[self.QUEEN]

        for queen in self.get_pieces(self.QUEEN, self.BLACK):
            v -= queens_black[queen]
            v -= piece_val[self.QUEEN]


        for knight in self.get_pieces(self.KNIGHT, self.WHITE):
            v += knights[knight]
            v += piece_val[self.KNIGHT]

        for knight in self.get_pieces(self.KNIGHT, self.BLACK):
            v -= knights_black[knight]
            v -= piece_val[self.KNIGHT]


        for pawn in self.get_pieces(self.PAWN, self.WHITE):
            v += pawns[pawn]
            v += piece_val[self.PAWN]

        for pawn in self.get_pieces(self.PAWN, self.BLACK):
            v -= pawns_black[pawn]
            v -= piece_val[self.PAWN]


        white_king = board.king(self.WHITE)
        black_king = board.king(self.BLACK)

        # KING
        if self.is_endgame:
            v += king_end_game[white_king]
            v -= king_end_game_black[black_king]
        else:
            v += king_middle_game[white_king]
            v -= king_middle_game_black[black_king]

        # WHITE SAFETY
        attk_units = 0
        for neighbouring_square in self.get_attacks(white_king):
            for attacked_square in self.get_attackers(chess.BLACK, neighbouring_square):
                attk_units += piece_attack_units[self.piece_type_at(attacked_square)]
        v -= king_safety[attk_units]

        # BLACK SAFETY
        attk_units = 0
        for neighbouring_square in self.get_attacks(black_king):
            for attacked_square in self.get_attackers(chess.WHITE, neighbouring_square):
                attk_units += piece_attack_units[self.piece_type_at(attacked_square)]
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

    def quiescent(self, board, alpha, beta, depth):
        isCheck = board.is_check()
        if not isCheck:
            v = self.eval_func(board, color_multiplier[board.turn])
            if v >= beta:
                return v, None, []
            if v > alpha:
                alpha = v

        heap = []
        amove = []
        move = None
        if isCheck:
            isMoveOnCheck = False
            king_mask = board.kings & board.occupied_co[board.turn]
            if king_mask:
                king = chess.msb(king_mask)
                blockers = board._slider_blockers(king)
                checkers = board.attackers_mask(not board.turn, king)
                if checkers:
                    for move in board._generate_evasions(king, checkers):
                        isMoveOnCheck = True
                        if board._is_safe(king, blockers, move):
                            heap.append((0, move))
            if not isMoveOnCheck:
                return -MAXVALUE + depth, None, []

        else:
            for move in board.generate_legal_captures():
                heappush(heap, (-self.getCaptureValue(board, move), move))

        while heap:
            self.nodes += 1

            v, move = heappop(heap)

            board.push(move)
            if not isCheck:
                if board.is_check():
                    board.pop()
                    continue

            val, _, mvs = self.quiescent(board, -beta, -alpha, depth - 1)
            val = -val

            board.pop()

            if val >= beta:
                return beta, move, mvs + [move]

            if val > alpha:
                alpha = val
                amove = mvs + [move]

        if amove:
            return alpha, move, amove

        else:
            return alpha, None, []

    # TODO: optimize and get better undestanding of.
    # TODO: handle promotions
    def getCaptureValue(self, board, move):
        tsq = move.to_square
        fsq = move.from_square
        fen = board.fen()

        our_val = piece_val[board.piece_type_at(fsq)]
        if board.is_en_passant(move):
            their_val = piece_val[chess.PAWN]
        else:
            their_val = piece_val[board.piece_type_at(tsq)]

        if their_val > our_val:
            return their_val - our_val

        board.push(move)

        swaplist = [their_val]
        swap_count = 0
        lastval = our_val
        while True:
            attackers = self.get_attackers(board.turn, tsq)
            if len(attackers) == 0:
                break
            attackers_sorted = sorted([(board.piece_at(sq), sq) for sq in attackers], key=lambda piece: piece_val[piece[0].piece_type])
            lowest_val_attacker_sq = attackers_sorted[0][1]
            candidate_move = chess.Move(lowest_val_attacker_sq, tsq)
            board.push(candidate_move)
            swap_count += 1

            swaplist.append(swaplist[-1] + lastval)
            lastval = piece_val[attackers_sorted[0][0].piece_type]


            attackers = self.get_attackers(board.turn, tsq)
            if len(attackers) == 0:
                break
            attackers_sorted = sorted([(board.piece_at(sq), sq) for sq in attackers], key=lambda piece: piece_val[piece[0].piece_type])
            lowest_val_attacker_sq = attackers_sorted[0][1]
            candidate_move = chess.Move(lowest_val_attacker_sq, tsq)
            board.push(candidate_move)
            swap_count += 1

            swaplist.append(swaplist[-1] + lastval)
            lastval = -piece_val[attackers_sorted[0][0].piece_type]


        for i in range(swap_count+1):
            board.pop()

        for n in range(len(swaplist) - 1, 0, -1):
            if n & 1:
                if swaplist[n] <= swaplist[n - 1]:
                    swaplist[n - 1] = swaplist[n]
            else:
                if swaplist[n] >= swaplist[n - 1]:
                    swaplist[n - 1] = swaplist[n]

        if swaplist[0] < 0:
            return -MAXVALUE
        else:
            return swaplist[0]



if __name__ == '__main__':
    board = chess.Board()#"2bqkbn1/2pppp2/np2N3/r3P1p1/p2N2B1/5Q2/PPPPKPP1/RNB2r2 w KQkq - 0 1")
    ab = AlphaBetaSearch()
    ab.search(board, 7)

