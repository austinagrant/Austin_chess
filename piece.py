# Piece Class

# parent class to simplify other pieces
from typing import TYPE_CHECKING, Generator

if TYPE_CHECKING:
    from move import Move

class Piece:
    deBruin:list[int] = [63, 0, 58, 1, 59, 47, 53, 2, 60, 39,
                48, 27, 54, 33, 42, 3, 61, 51, 37, 40, 49, 18, 28,
                20, 55, 30, 34, 11, 43, 14, 22, 4, 62, 57, 46, 52,
                38, 26, 32, 41, 50, 36, 17, 19, 29, 10, 13, 21, 56,
                45, 25, 31, 35, 16, 9, 12, 44, 24, 15, 8, 23, 7, 6, 5]
    white_team:bool = None
    bitboard:int = None
    indices:list[int] = None
    hasMoved:bool = False
    value:int = None
    positional_value:list[int]
    
    def __init__(self, board, white_team=None, val=None):
        self.bitboard = board
        self.indices = [ind for ind in self.generatePositions()]
        self.white_team = white_team
        self.value = val
    
    
    def calc_index(self, row: int, col: int) -> int:
        if row == 0:
            return 0
        elif col < (8 - row):
            return 2 * row - 1
        else:
            return 2 * row
        
    def calc_anti_diag_index(self, row: int, col: int) -> int:
        if row == 0:
            return 0
        elif col < row:
            return 2 * row - 1
        else:
            return 2 * row
        
    def getMSB(self, board: int) -> int:
        deB = 0x07EDD5E59A4E28C2
        deb_index = (((board & -board) * deB) >> 58) & 0x3f
        return self.deBruin[deb_index]

    def bin_str(self):
        '''Return binary string of Pieces bitboard'''
        return format(self.bitboard, '065b')
    
    def print_board(self):
        '''Print bitboard as a board'''
        s = format(self.bitboard, '065b')
        for i in range(0,len(s)-1, 8):
            print(s[i+8:i:-1])
            
    def generatePositions(self) -> Generator[int, None, None]:
        positions = int(self.bitboard)
        while positions != 0:
            msb = self.getMSB(positions)
            positions = positions ^ (1 << msb)
            yield msb
            
    def move_rule(self, position_index):
        '''Return a bitboard of possible moves from position_index'''
        return None
    
    
    def generateMoves(self, team_board=0, opp_board=0)-> Generator['Move', None, None]:
        '''Return a Generator to make pseudo Legal Moves'''
        return None
                
    def do_move(self, start_index:int, end_index:int) -> None:
        '''Blindly update bitboard and indices'''
        self.bitboard = (self.bitboard ^ (1 << start_index)) | (1 << end_index)
        try:
            self.indices.remove(start_index)
        except ValueError:
            pass
        if end_index >= 0 and end_index <= 63:
            self.indices.append(end_index)
        
    def make_moves(self, start_index:int, move_board:int) -> list['Move']:
        moves = []
        while move_board != 0:
            new_pos = self.getMSB(move_board)
            moves.append(Move(self, start_index, new_pos))
            move_board = move_board ^ (1 << new_pos)
        return moves
    
    def __str__(self):
        return "_"
        
    def reverse_bits(self, num):
        reversed_num = 0
        bit_length = num.bit_length()  # Number of bits in num
        
        for _ in range(bit_length):
            reversed_num = (reversed_num << 1) | (num & 1)
            num >>= 1
        
        # Pad to 64 bits
        reversed_num <<= (8 - bit_length)
    
        return reversed_num
    
    def flip_vertical(self, board:int) -> int:
        k1 = 0x00FF00FF00FF00FF
        k2 = 0x0000FFFF0000FFFF
        board = ((board >>  8) & k1) | ((board & k1) <<  8)
        board = ((board >> 16) & k2) | ((board & k2) << 16)
        board = ( board >> 32)       | ( board       << 32)
        return board

    def flipDiagA1H8(self, board:int) -> int:
        k1 = 0x5500550055005500
        k2 = 0x3333000033330000
        k4 = 0x0f0f0f0f00000000
        t      =  k4 & (board ^ (board << 28))
        board ^=  t ^ (t >> 28) 
        t      =  k2 & (board ^ (board << 14))
        board ^=  t ^ (t >> 14) 
        t      =  k1 & (board ^ (board <<  7))
        board ^=  t ^ (t >>  7) 
        
        return board & 0xffffffffffffffff
    
    
    def flipDiagH1A8(self, board:int) -> int:
        k1 = 0xaa00aa00aa00aa00
        k2 = 0xcccc0000cccc0000
        k4 = 0xf0f0f0f00f0f0f0f
        t      =  board ^ (board << 36) 
        board ^=  k4 & (t ^ (board >> 36))
        t      =  k2 & (board ^ (board << 18))
        board ^=  t ^ (t >> 18) 
        t      =  k1 & (board ^ (board <<  9))
        board ^=  t ^ (t >>  9)
        return board & 0xffffffffffffffff
    
    def rotate90Clock(self, board:int) -> int:
        return self.flipDiagH1A8(self.flip_vertical(board))
    
    def rotate90Counter(self, board:int) -> int:
        return self.flipDiagA1H8(self.flip_vertical(board))
    
    def right_rotate(self, to_shift:int, shifted_by :int) -> int:
        return ((to_shift >> shifted_by) | (to_shift << (64 - shifted_by))) & 0xffffffffffffffff
    
    def pseudoRotate45Clock(self, board:int) -> int:
        k1 = 0xAAAAAAAAAAAAAAAA
        k2 = 0xCCCCCCCCCCCCCCCC
        k4 = 0xF0F0F0F0F0F0F0F0
        board ^= k1 & (board ^ self.right_rotate(board, 8))
        board ^= k2 & (board ^ self.right_rotate(board, 16))
        board ^= k4 & (board ^ self.right_rotate(board, 32))
        return board & 0xffffffffffffffff
    
    def pseudoRotate45Counter(self, board:int):
        k1 = 0x5555555555555555
        k2 = 0x3333333333333333
        k4 = 0x0f0f0f0f0f0f0f0f
        board ^= k1 & (board ^ self.right_rotate(board,  8))
        board ^= k2 & (board ^ self.right_rotate(board, 16))
        board ^= k4 & (board ^ self.right_rotate(board, 32))
        return board & 0xffffffffffffffff
    
    
    
