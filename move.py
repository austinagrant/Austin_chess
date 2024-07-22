# Move class
import copy
from typing import TYPE_CHECKING
import dataclasses

if TYPE_CHECKING:
    from piece import Piece
@dataclasses.dataclass
class Move():
    
    piece:'Piece'
    
    start_index:int
    
    end_index:int
    
    taken:'Piece'
    
    eval:int
    
    pawn_transform:bool = False
    
    transform:'Piece'
    
    
    def __init__(self, p: 'Piece', start_index=65, end_index=65, eval=0):
        self.piece = p
        self.start_index = start_index
        self.end_index = end_index
        self.eval = 0
        self.taken = None
    
    
    def clone(self, to_transform:'Piece'):
        new_move = copy.copy(self)
        new_move.transform = to_transform
        return new_move
        
    def convert_from_index(self,index:int) -> str:
        row = index // 8
        col = index % 8
        return "" + chr(ord('A') + col) + chr(49 + row)
    
    def __str__(self) -> str:
        return self.piece.__str__() + " from " + self.convert_from_index(self.start_index) + " to " + self.convert_from_index(self.end_index)
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Move):
            return self.piece == __value.piece and self.start_index == __value.start_index and self.end_index == __value.end_index
        else:
            return False
    
    