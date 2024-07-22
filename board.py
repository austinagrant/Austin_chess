import sys

from White_Pawn import W_P
from White_Knight import W_N
from White_Rook import W_R
from White_Bishop import W_B
from Black_Pawn import B_P
from Black_Knight import B_N
from Black_Rook import B_R
from Black_Bishop import B_B
from piece import Piece
from move import Move
    
    
    
class Board():
    
    board_matrix:list[str]
    
    white_pieces:list[Piece]
    black_pieces:list[Piece]
    
    
    white_bitboard:int
    black_bitboard:int
    
    def __init__(self):
        self.white_pieces = [W_P()]
        self.black_pieces = [B_P()]
        self.white_bitboard = self.gen_board(self.white_pieces)
        self.black_bitboard = self.gen_board(self.black_pieces)
        
    def gen_board(self, piece_list:list[Piece]) -> int:
        board = 0
        for p in piece_list:
            board = board | p.bitboard
        return board
    
    def print_board(board:int):
        s = format(board, '065b')
        for i in range(0,len(s),8):
            print(s[i:i+8])

    def is_occupied(self, index=None, board=None) -> bool:
        
        both = self.white_bitboard | self.black_bitboard
        if board is None:
            return both & (1 << index) != 0
        elif index is None:
            return both & board != 0
    
    def piece_at(self, index:int, white_team:bool)->Piece:
        '''Return the piece at the given index only looking at bool's team'''
        team = self.white_pieces
        if not white_team:
            team = self.black_pieces
        loc = 1 << index
        for p in team:
            if p.bitboard & loc != 0:
                return p
        return None
    
    def update_team_board(self, old_index:int, new_index:int, team:bool) -> None:
        '''Update the given teams bitboard'''
        if team:
            self.white_bitboard = (self.white_bitboard ^ (1 << old_index)) | (1 << new_index)
        else:
            self.black_bitboard = (self.black_bitboard ^ (1 << old_index)) | (1 << new_index)
        
    
    def doMove(self, m:Move) -> None:
        to_move = m.piece
        # print("Doing:", m)
        # check if we are capturing
        try:
            self.is_occupied(index=m.end_index)
        except ValueError:
            print(m)
        if self.is_occupied(index=m.end_index):
            m.taken = self.piece_at(m.end_index, not to_move.white_team)
            if m.taken is None:
                print(m, "\n", to_move.white_team, "\n", self)
                [print(p, p.indices) for p in (self.black_pieces if to_move.white_team else self.white_pieces)]
            m.taken.do_move(m.end_index, 65)
            self.update_team_board(m.end_index, 65, not to_move.white_team)
        # Tell the piece to actually move
        to_move.do_move(m.start_index, m.end_index)
        # update team boards
        self.update_team_board(m.start_index, m.end_index, to_move.white_team)
        
        
    def undoMove(self, m:Move) -> None:
        to_move = m.piece
        # print("Undo:", m)
        # Put taken piece back on board
        if m.taken is not None:
            taken = m.taken
            taken.do_move(65, m.end_index)
            self.update_team_board(65, m.end_index, taken.white_team)
        # move piece back
        to_move.do_move(m.end_index, m.start_index)
        # update team board
        self.update_team_board(m.end_index, m.start_index, to_move.white_team)
        
        
        
        
    def DFS_Max(self, curr_depth:int, cut_off:int, alpha:int, beta:int)-> Move:
        if curr_depth >= cut_off:
            return Move(None, eval=self.eval())
        best_move = None
        for p in self.white_pieces:
            for m in p.generateMoves(self.white_bitboard, self.black_bitboard):
                if m is None:
                    print(p)
                self.doMove(m)
                # print("Calling Min @ depth:", curr_depth)
                min_move = self.DFS_Min(curr_depth+1, cut_off, alpha, beta)
                if min_move.eval >= alpha:
                    alpha = min_move.eval
                    best_move = m
                    if alpha >= beta:
                        self.undoMove(m)
                        break
                    
                self.undoMove(m)
        if best_move is None:
            alpha = -sys.maxsize
            best_move = Move(None)
            print("AAAAAAAA")
        best_move.eval = alpha
        return best_move
            
    def DFS_Min(self, curr_depth:int, cut_off:int, alpha:int, beta:int)-> Move:
        if curr_depth >= cut_off:
            return Move(None, eval=self.eval())
        best_move = None
        for p in self.black_pieces:
            for m in p.generateMoves(self.black_bitboard, self.white_bitboard):
                self.doMove(m)
                # print("Calling Max @ depth:", curr_depth)
                max_move = self.DFS_Max(curr_depth+1, cut_off, alpha, beta)
                # print("Max eval:", max_move.eval)
                if max_move.eval < beta:
                    beta = max_move.eval
                    best_move = m
                    if alpha >= beta:
                        self.undoMove(m)
                        break  
                self.undoMove(m)
        if best_move is None:
            beta = sys.maxsize
            best_move = Move(None)
        best_move.eval = beta
        return best_move
    
    
    def eval(self):
        white_total, black_total = 0, 0
        for p in self.white_pieces:
            for index in p.indices:
                white_total += p.value + p.positional_value[index]
        for p in self.black_pieces:
            for index in p.indices:
                black_total += p.value + p.positional_value[index]
        return white_total - black_total
    
    def populate_board(self) -> None:
        board = [" "] * 64
        for p in self.white_pieces:
            for index in p.indices:
                board[index] = p.__str__()
        for p in self.black_pieces:
            for index in p.indices:
                board[index] = p.__str__()
        self.board_matrix = board
        
            
    
    def __str__(self) -> str:
        self.populate_board()
        b = "+----------------------------------------+\n"
        b = "".join([b, "|                                        |\n", "|     +---+---+---+---+---+---+---+---+  |\n|  8  | "])
        for i in range(63, 0, -8):
            for j in range(7, -1, -1):
                elem = self.board_matrix[i-j]
                b = "".join([b, elem, " | "])
                if j == 0 and i != 7:
                    b = "".join([b, " |\n|     +---+---+---+---+---+---+---+---+  |\n|  ", str((i - j) // 8), "  | "])
        b = "".join([b, " |\n|     +---+---+---+---+---+---+---+---+  |\n", "|                                        |\n", 
                "|       A   B   C   D   E   F   G   H    |\n", "|                                        |\n", 
                "+----------------------------------------+\n"])
        return b
    
    
b = Board()
print(b)