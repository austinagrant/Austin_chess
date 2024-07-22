from board import Board
from move import Move
import sys

playing = True
DEPTH = 4
MOVES = 5


def white_move(b: Board) -> Move:
    m = b.DFS_Max(0, DEPTH, -sys.maxsize, sys.maxsize)
    print(m, "\n\n")
    return m
    
def black_move(b: Board) -> Move:
    m = b.DFS_Min(0, DEPTH, -sys.maxsize, sys.maxsize)
    print(m, "\n\n")
    return m


while playing:
    print("Starting Game")
    print("Depth:", DEPTH)
    print("Moves:", MOVES)
    b = Board()
    print(b)
    for _ in range(MOVES):
        print("White Move")
        white_m = white_move(b)
        if white_m is not None:
            b.doMove(white_m)
            print(b)
        else:
            print("White had no move")
            continue
        print("Black Move")
        black_m = black_move(b)
        if black_m is not None:
            b.doMove(black_m)
            print(b)
        else:
            print("Black had no move")
            continue
        
    break
    
    
    
