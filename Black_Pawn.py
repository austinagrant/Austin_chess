# Black Pawn
from typing import TYPE_CHECKING, Generator
from piece import Piece
if TYPE_CHECKING:
    from move import Move
    
    
class B_P(Piece):
    
    positional_value:list[int] = [
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0]
    
    def __init__(self, board=0b0000000011111111000000000000000000000000000000000000000000000000):
        super(B_P, self).__init__(board, False, 100)
        
    def __str__(self) -> str:
        return "♟"
        
    def alt_move_rule_1(self, occ:int) -> int:
        return self.bitboard & ~(occ << 8)
    def alt_move_rule_2(self, forward1:int, occ:int) -> int:
        return 0xff000000000000 & forward1 & ~(occ << 16)
    def alt_attack_rule_1(self, opp_board:int) -> int:
        return  self.bitboard & (opp_board << 7) & 0xefefefefefefefef 
    def alt_attack_rule_2(self, opp_board:int) -> int:
        return self.bitboard & (opp_board << 9) & 0xfefefefefefefefe 

    def generateMoves(self, team_board=0, opp_board=0) -> Generator['Move', None, None]:
        from move import Move
        occ = team_board | opp_board
        forward1 = self.alt_move_rule_1(occ)
        forward1_copy = int(forward1)
        while forward1 != 0 :
            msb = self.getMSB(forward1)
            m = Move(self, msb, msb - 8)
            m.pawn_transform = msb < 16
            forward1 = forward1 ^ (1 << msb)
            # print("push1", m)
            yield m
            
        forward2 = self.alt_move_rule_2(forward1_copy, occ)
        while forward2 != 0:
            msb = self.getMSB(forward2)
            forward2 = forward2 ^ (1 << msb)
            m = Move(self, msb, msb-16)
            # print("push2", m)
            yield m
            
        attackLeft = self.alt_attack_rule_2(opp_board)
        while attackLeft != 0:
            msb = self.getMSB(attackLeft)
            m = Move(self, msb, msb-9)
            m.pawn_transform = msb < 16
            attackLeft = attackLeft ^ (1 << msb)
            # print("left", m)
            yield m
            
        attackRight = self.alt_attack_rule_1(opp_board)
        while(attackRight != 0):
            msb = self.getMSB(attackRight)
            m = Move(self, msb, msb-7)
            m.pawn_transform = (msb < 16)
            attackRight = attackRight ^ (1 << msb)
            # print("right", m)
            yield m