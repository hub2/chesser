#!/usr/bin/env pypy3
from __future__ import print_function
import chess
from engine import AlphaBetaSearch
import sys
import time
import chess.polyglot

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    ap = AlphaBetaSearch()

    forced = False
    our_time, opp_time = 1000, 1000 # time in centi-seconds
    show_thinking = True

    # print name of chess engine
    print('Chesser')

    stack = []
    board = chess.Board()

    opening_book = chess.polyglot.MemoryMappedReader("../Formula14.bin")

    while True:
        if stack:
            smove = stack.pop()
        else:
            smove = input()
        eprint('[C] {}'.format(smove))

        if smove == 'quit':
            break

        elif smove == 'uci':
            print('uciok')

        elif smove == 'isready':
            print('readyok')

        elif smove == 'ucinewgame':
            stack.append('position fen ' + chess.STARTING_FEN)

        elif smove.startswith('position'):
            board = chess.Board()
            params = smove.split(' ', 2)
            if params[1] == 'fen':
                fen = params[2]
                board = chess.Board(fen)
            if params[1] == 'startpos':
                if len(params) > 2:
                    k = params[2].split(' ')
                    if k[0] == 'moves':
                        for move in k[1:]:
                            board.push(chess.Move.from_uci(move))

        elif smove.startswith('go'):

            #  default options
            movetime = -1
            depth = 6

            # parse parameters
            params = smove.split(' ')
            if len(params) == 1: continue

            i = 0
            while i < len(params):
                param = params[i]
                if param == 'depth':
                    i += 1
                    depth = int(params[i])
                if param == 'movetime':
                    i += 1
                    movetime = int(params[i])
                i+=1

            book_move = opening_book.get(board, None)
            if book_move is not None:
                eprint("Found opening book move {} with value {}".format(book_move.move().uci(), book_move.weight))
                print('bestmove ' + book_move.move().uci())
                continue

            eprint("Starting AlphaBetaSearch with depth {}".format(depth))

            s = time.time()

            val, move = ap.minimax(board, depth, board.turn)

            e = time.time()
            usedtime = (e-s)*1000

            print('info depth {} score {} time {} nodes {}'.format(depth, val, int(usedtime), ap.nodes))
            eprint('info depth {} score {} time {} nodes {}'.format(depth, val, int(usedtime), ap.nodes))
            print('bestmove ' + move.uci())

        elif smove.startswith('time'):
            our_time = int(smove.split()[1])

        elif smove.startswith('otim'):
            opp_time = int(smove.split()[1])

if __name__ == '__main__':
    main()
