# Black Rook
# White Rook
from typing import TYPE_CHECKING, Generator
from move import Move
from piece import Piece
if TYPE_CHECKING:
    from move import Move
    
    
class B_R(Piece):
    positional_value:list[int] = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            0,  0,  0,  5,  5,  0,  0,  0]
    
    def __init__(self, board=0b1000000100000000000000000000000000000000000000000000000000000000):
        super(B_R, self).__init__(board, False, 500)
    def __str__(self) -> str:
        return "♜"
    
    
    
    def generateMoves(self, team_board=0, opp_board=0) -> Generator[Move, None, None]:
        from move import Move
        for pos in self.generatePositions():
            row = pos // 8
            shift_row = 0b11111111
            rook = (1 << (pos % 8))
            team_row = ((team_board >> (row * 8)) & shift_row)
            opp_row = ((opp_board >> (row * 8)) & shift_row)
            
            fin = ((team_row - (rook << 1)) ^ team_row) & ~team_row
            
            fin2 = (opp_row ^ (opp_row - (rook << 1)))
            reverse_rook = self.reverse_bits(rook)
            reverse_team_row = self.reverse_bits(team_row)
            reverse_opp_row = self.reverse_bits(opp_row)
            
            team_row = reverse_team_row & shift_row
            opp_row = reverse_opp_row & shift_row
            fin3 = self.reverse_bits((((team_row - (reverse_rook << 1)) ^ team_row) & ~team_row) & shift_row)
            fin4 = self.reverse_bits((opp_row ^ (opp_row - (reverse_rook << 1))) & shift_row)
            move_row = ((fin | fin3) & (fin2 | fin4)) & shift_row
            board = move_row << (row * 8)
            while board != 0:
                msb = self.getMSB(board)
                board = board ^ (1 << msb)
                m = Move(self, pos, msb)
                # print("rank", m)
                yield m
            yield from self.check_col(pos, team_board, opp_board)
            
            
    def check_col(self, pos:int, team_board=0, opp_board=0) -> Generator[Move, None, None]:
        rotated_rook = self.rotate90Clock(1 << pos)
        pos_rot = self.getMSB(rotated_rook)
        team_board = self.rotate90Clock(team_board)
        opp_board = self.rotate90Clock(opp_board)
        row = pos_rot // 8
        shift_row = 0b11111111
        rook = 1 << (pos_rot % 8)
        team_row = (team_board >> (row * 8)) & shift_row
        opp_row = (opp_board >> (row * 8)) & shift_row
        
        fin = (((team_row - (rook << 1)) ^ team_row) & ~team_row ) & shift_row
        fin2 = (opp_row ^ (opp_row - (rook << 1))) & shift_row
        reverse_rook = self.reverse_bits(rook)
        reverse_team_row = self.reverse_bits(team_row)
        reverse_opp_row = self.reverse_bits(opp_row)
        
        team_row = reverse_team_row & shift_row
        opp_row = reverse_opp_row & shift_row
        
        fin3 = self.reverse_bits((((team_row - (reverse_rook << 1)) ^ team_row) & ~team_row) & shift_row)
        fin4 = self.reverse_bits((opp_row ^ (opp_row - (reverse_rook << 1))) & shift_row)
        move_row = ((fin | fin3) & (fin2 | fin4)) & shift_row
        board = self.rotate90Counter(move_row << (row * 8))

        
        while board != 0:
            msb = self.getMSB(board)
            board = board ^ (1 << msb)
            m = Move(self, pos, msb)
            # print("file", m)
            yield m
            