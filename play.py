#!/usr/bin/env python3
import chess
from engine import AlphaBetaSearch, eval_func


def main():
    board = chess.Board()

    forced = False
    our_time, opp_time = 1000, 1000 # time in centi-seconds
    show_thinking = True
    depth = 2

    # print name of chess engine
    print('Chesser')

    stack = []
    while True:
        if stack:
            smove = stack.pop()
        else:
            smove = input()

        if smove == 'quit':
            break

        elif smove == 'uci':
            print('uciok')

        elif smove == 'isready':
            print('readyok')

        elif smove == 'ucinewgame':
            stack.append('position fen ' + chess.STARTING_FEN)

        elif smove.startswith('position'):
            params = smove.split(' ', 2)
            if params[1] == 'fen':
                fen = params[2]
                board = chess.Board(fen)

        elif smove.startswith('go'):
            #  default options
            depth = 1000
            movetime = -1

            # parse parameters
            params = smove.split(' ')
            if len(params) == 1: continue

            i = 0
            while i < len(params):
                param = params[i]
                if param == 'depth':
                    i += 1
                    depth = int(params[i])
            ap = AlphaBetaSearch(board.turn)
            ap.minimax(board, depth)





if __name__ == '__main__':
    main()
