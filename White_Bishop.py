# White Bishop
from typing import TYPE_CHECKING, Generator
from move import Move
from piece import Piece
if TYPE_CHECKING:
    from move import Move
    
    
    
class W_B(Piece):
    
    positional_value:list[int] = [ 
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10,-10,-10,-10,-10,-20]
    
    anti_diag_mask = [
        0b11111111,
        0b1, 0b11111110,
        0b11, 0b11111100,
        0b111, 0b11111000,
        0b1111, 0b11110000,
        0b11111, 0b11100000,
        0b111111, 0b11000000,
        0b1111111, 0b10000000
    ]
    diag_mask = [
        0b11111111,
        0b1111111, 0b10000000,
        0b111111, 0b11000000,
        0b11111, 0b11100000,
        0b1111, 0b11110000,
        0b111, 0b11111000,
        0b11, 0b11111100,
        0b1, 0b11111110
    ]
    
    def __init__(self, board=0b00100100):
        super(W_B, self).__init__(board, True, 330)
        
    def __str__(self) -> str:
        return "♗"
    
    def generateMoves(self, team_board=0, opp_board=0) -> Generator[Move, None, None]:
        for pos in self.generatePositions():
            rot_pos = self.pseudoRotate45Clock(1 << pos)
            rot_ind = self.getMSB(rot_pos)
            team_board_45 = self.pseudoRotate45Clock(team_board)
            opp_board_45 = self.pseudoRotate45Clock(opp_board)
            row = rot_ind // 8
            col = rot_ind % 8
            shift_row = 0b11111111
            bishop = 1 << col
            # print("bishop:", bin(bishop))
            team_row = ((team_board_45 >> (row * 8)) & shift_row)
            opp_row = ((opp_board_45 >> (row * 8)) & shift_row)
            # print("team_row:", bin(team_row), "opp_row:", bin(opp_row))
            
            
            fin = (((team_row - (bishop << 1)) ^ team_row) & ~team_row)
            # print("fin:", bin(fin))
            fin2 = (opp_row ^ (opp_row - (bishop << 1)))
            # print("fin2_opp:", bin(fin2))
            
            rev_bishop = self.reverse_bits(bishop)
            # print("rev_bishop", bin(rev_bishop))
            rev_team_row = self.reverse_bits(team_row)
            # print("rev_team_row:", bin(rev_team_row))
            rev_opp_row = self.reverse_bits(opp_row)
            # print("rev_opp_row:", bin(rev_opp_row))
            
            rev_team_row = rev_team_row & shift_row
            # print("rev_team_row:", bin(rev_team_row))
            rev_opp_row = rev_opp_row & shift_row
            # print("rev_opp_row:", bin(rev_opp_row))

            
            fin3 = ((((rev_team_row - (rev_bishop << 1)) ^ rev_team_row) & ~rev_team_row) & shift_row)
            # print("fin3 pre rev:", bin(fin3))
            fin3 = self.reverse_bits(fin3)
            # print("fin3 post rev:", bin(fin3))
            fin4 = self.reverse_bits((opp_row ^ (opp_row - (rev_bishop << 1))) & shift_row)
            # print("fin4:", bin(fin4))
            move_row = ((fin | fin3) & (fin2 | fin4))
            # print("move_row pre mask:", bin(move_row))
            indy = self.calc_index(row, col)
            # print("mask", bin(self.diag_mask[indy]))
            move_row = move_row & self.diag_mask[indy]
            
            # print("move_row:", bin(move_row))
            move_row = move_row << (row * 8)
            board = self.pseudoRotate45Counter(move_row)
            # print("board pre rot:", bin(board))
            board = self.right_rotate(board, 8)
            
            # print(bin(board))
            
            while board != 0:
                msb = self.getMSB(board)
                board = board ^ (1 << msb)
                m = Move(self, pos, msb)
                # print("diag", m)
                yield m
            
            # print("ANTIDIAG")
            rot_ind = self.getMSB(self.pseudoRotate45Counter(1 << pos))
            row = rot_ind // 8
            col = rot_ind % 8
            shift_row = 0b11111111
            bishop = 1 << col
            team_row = ((self.pseudoRotate45Counter(team_board) >> (row * 8)) & shift_row)
            opp_row = ((self.pseudoRotate45Counter(opp_board) >> (row * 8)) & shift_row)
            # print("team_row:", bin(team_row), "opp_row:", bin(opp_row), "bishop:", bin(bishop))
            
            
            fin = (((team_row - (bishop << 1)) ^ team_row) & ~team_row) & shift_row
            # print("fin:", bin(fin))
            fin2 = (opp_row ^ (opp_row - (bishop << 1))) & shift_row
            # print("fin2_opp:", bin(fin2))
            
            rev_bishop = self.reverse_bits(bishop)
            # print("rev_bishop", bin(rev_bishop))
            rev_team_row = self.reverse_bits(team_row)
            # print("rev_team_row:", bin(rev_team_row))
            rev_opp_row = self.reverse_bits(opp_row)
            # print("rev_opp_row:", bin(rev_opp_row))
            
            rev_team_row = rev_team_row & shift_row
            # print("rev_team_row:", bin(rev_team_row))
            rev_opp_row = rev_opp_row & shift_row
            # print("rev_opp_row:", bin(rev_opp_row))

            
            fin3 = ((((rev_team_row - (rev_bishop << 1)) ^ rev_team_row) & ~rev_team_row) & shift_row)
            # print("fin3 pre rev:", bin(fin3))
            fin3 = self.reverse_bits(fin3)
            # print("fin3 post rev:", bin(fin3))
            fin4 = self.reverse_bits((opp_row ^ (opp_row - (rev_bishop << 1))) & shift_row)
            move_row = ((fin | fin3) & (fin2 | fin4)) & shift_row
            # print("move_row pre mask:", bin(move_row))
            move_row &= self.anti_diag_mask[self.calc_anti_diag_index(row, col)]
            # print("move_row:", bin(move_row))
            board = move_row << (row * 8)
            inter = self.pseudoRotate45Clock(board)
            # print("Intermediate board:", bin(inter))
            board = self.right_rotate(inter, 8)
            
            while board != 0:
                msb = self.getMSB(board)
                board = board ^ (1 << msb)
                m = Move(self, pos, msb)
                # print("Anti", m)
                yield m
            
            
# diag = 0x8040201008040201
# b_diag = 0x80402010080402
# anti = 0x0102040810204080


