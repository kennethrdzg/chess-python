WHITE = True
BLACK = False

class ChessPiece: 
    def __init__(self, color: bool, position: int) -> None:
        self.symbol = "#"
        self.color = color
        self.value = 0
        self.position = position
        self.has_moved = False
    def __str__(self) -> str:
        return self.symbol
    def legal_moves(self, board: list)->list: 
        return []
    def make_move(self, board: list, move: int)->None: 
        piece = board[move]
        if isinstance(piece, ChessPiece): 
            piece.position = -1
        board[move] = self
        board[self.position] = "."
        self.position = move
        self.has_moved = True
    def undo_move(self, board: list, move: int)->None: 
        self.make_move(board, move)
    def demote(self, board): 
        pass

class Pawn(ChessPiece): 
    def __init__(self, color: bool, position: int) -> None:
        super().__init__(color, position)
        self.value = 1
        if self.color: 
            self.symbol = "P"
        else: 
            self.symbol = "p"
    def legal_moves(self, board: list) -> list:
        move_list = list()
        diff = 8
        left_diagonal = 7
        right_diagonal = 9
        if self.color == BLACK: 
            diff *= -1
            left_diagonal *= -1
            right_diagonal *= -1

        if self.position + diff >= 0 and self.position + diff <= 63: 
            if board[self.position+diff] == ".": 
                #MOVE ONE SQUARE
                move_list.append(self.position+diff)

                if self.position + 2*diff >= 0 and self.position + 2*diff <= 63 and not self.has_moved: 
                    if board[self.position+diff*2] == ".": 
                        #MOVE TWO SQUARES
                        move_list.append(self.position+2*diff)

        #CAPTURE

        if self.position + left_diagonal >= 0 and self.position + left_diagonal <= 63 and (
            (self.position+left_diagonal)//8 == self.position//8 + 1 or (self.position+left_diagonal)//8 == self.position//8 - 1
        ) and ((self.position+left_diagonal)%8 == self.position%8-1 or (self.position+left_diagonal)%8 == self.position%8+1): 
            piece = board[self.position+left_diagonal]
            if isinstance(piece, ChessPiece) and piece.color != self.color: 
                move_list.append(self.position+left_diagonal)
        if self.position + right_diagonal >= 0 and self.position + right_diagonal <= 63 and (
            (self.position+right_diagonal)//8 == self.position//8+1 or (self.position+right_diagonal)//8 == self.position//8-1
        ) and ((self.position+right_diagonal)%8 == self.position%8-1 or (self.position+right_diagonal)%8 == self.position%8+1): 
            piece = board[self.position+right_diagonal]
            if isinstance(piece, ChessPiece) and piece.color != self.color: 
                move_list.append(self.position+right_diagonal)
        #EN PASSANT

        return move_list

    def can_promote(self)->bool: 
        if self.color == WHITE: 
            if self.position//8 == 7: 
                return True
        else: 
            if self.position//8 == 0: 
                return True
        return False
    def promote(self)->str: 
        print("PROMOTION: ")
        promotion = input("R/N/B/Q: ").strip().upper()
        while promotion not in "RNBQ": 
            promotion = input("R/N/B/Q: ").strip().upper()
        if promotion == "R": 
            return Rook(self.color, self.position)
        elif promotion == "N": 
            return Knight(self.color, self.position)
        elif promotion == "B": 
            return Bishop(self.color, self.position)
        return Queen (self.color, self.position)

class Rook(ChessPiece): 
    def __init__(self, color: bool, position: int) -> None:
        super().__init__(color, position)
        self.value = 5
        if self.color: 
            self.symbol = "R"
        else: 
            self.symbol = "r"
    def legal_moves(self, board: list) -> list:
        move_list = list()
        
        #DOWN
        temp_position = self.position - 8
        while temp_position >= 0: 
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
            temp_position -= 8

        #UP
        temp_position = self.position +8
        while temp_position <= 63: 
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
            temp_position += 8

        #RIGHT
        temp_position = self.position+1
        while temp_position // 8 == self.position // 8 and temp_position<=63:
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
            temp_position += 1

        #LEFT
        temp_position = self.position - 1
        while temp_position // 8 == self.position // 8 and temp_position >=0: 
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
            temp_position -= 1
        return move_list
        
class Knight(ChessPiece): 
    def __init__(self, color: bool, position: int) -> None:
        super().__init__(color, position)
        self.value = 3
        if self.color: 
            self.symbol = "N"
        else: 
            self.symbol = "n"
    def legal_moves(self, board: list) -> list:
        move_list = list()

        if self.position - 17 >= 0 and (self.position-17)//8 == self.position//8-2 and (self.position-17)%8 == self.position%8 - 1: 
            if board[self.position - 17] == "." or board[self.position - 17].color != self.color: 
                move_list.append(self.position-17)

        if self.position - 15>=0 and (self.position-15)//8 == self.position//8-2 and (self.position-15)%8 == self.position%8 + 1: 
            if board[self.position - 15] == "." or board[self.position - 15].color != self.color: 
                move_list.append(self.position-15)

        if self.position -10 >=0 and (self.position-10)//8 == self.position//8-1 and (self.position-10)%8 == self.position%8-2:
            if board[self.position - 10] == "." or board[self.position - 10].color != self.color: 
                move_list.append(self.position-10)

        if self.position - 6 >= 0 and (self.position-6)//8 == self.position//8-1 and (self.position-6)%8 == self.position%8+2:
            if board[self.position - 6] == "." or board[self.position - 6].color != self.color: 
                move_list.append(self.position-6)

        if self.position + 6 <= 63 and (self.position+6)//8 == self.position//8+1 and (self.position+6)%8 == self.position%8-2:
            if board[self.position +6] == "." or board[self.position +6].color != self.color: 
                move_list.append(self.position+6)

        if self.position + 10 <= 63 and (self.position + 10) // 8 == self.position//8+1 and (self.position+10)%8 == self.position % 8 +2:
            if board[self.position +10] == "." or board[self.position +10].color != self.color: 
                move_list.append(self.position+10)

        if self.position + 15 <= 63 and (self.position+15)//8 == self.position//8+2 and (self.position+15)%8 == self.position % 8 -1:
            if board[self.position +15] == "." or board[self.position +15].color != self.color:
                move_list.append(self.position+15)

        if self.position + 17 <= 63 and (self.position + 17) //8 == self.position//8 + 2 and (self.position+17) % 8 == self.position % 8 +1: 
            if board[self.position +17] == "." or board[self.position +17].color != self.color: 
                move_list.append(self.position+17)

        return move_list

class Bishop(ChessPiece): 
    def __init__(self, color: bool, position: int) -> None:
        super().__init__(color, position)
        self.value = 3
        if self.color: 
            self.symbol = "B"
        else: 
            self.symbol = "b"
    def legal_moves(self, board: list) -> list:
        move_list = list()
        #LEFT-DOWN
        temp_position = self.position
        while temp_position-9 >= 0 and (temp_position-9)//8 == temp_position//8-1 and (temp_position-9)%8 == temp_position%8-1:
            temp_position -= 9
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
        #RIGHT-DOWN
        temp_position = self.position
        while temp_position-7 >= 0 and (temp_position-7)//8 == temp_position//8-1 and (temp_position-7)%8 == temp_position%8+1:
            temp_position -= 7
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
        #LEFT-UP
        temp_position = self.position
        while temp_position+7 <= 63 and (temp_position+7)//8 == temp_position//8+1 and (temp_position+7)%8 == temp_position%8-1:
            temp_position += 7
            if board[temp_position] == ".":
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
        #RIGHT-UP
        temp_position = self.position
        while temp_position+9 <= 63 and (temp_position+9)//8 == temp_position//8+1 and (temp_position+9)%8 == temp_position%8+1:
            temp_position += 9
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break            

        return move_list

class Queen(ChessPiece): 
    def __init__(self, color: bool, position: int) -> None:
        super().__init__(color, position)
        self.value = 9
        if self.color: 
            self.symbol = "Q"
        else: 
            self.symbol = "q"
    def legal_moves(self, board: list) -> list:
        move_list = list()

        #DOWN
        temp_position = self.position - 8
        while temp_position >= 0: 
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
            temp_position -= 8

        #UP
        temp_position = self.position +8
        while temp_position <= 63: 
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
            temp_position += 8

        #RIGHT
        temp_position = self.position+1
        while temp_position // 8 == self.position // 8 and temp_position<=63:
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
            temp_position += 1

        #LEFT
        temp_position = self.position - 1
        while temp_position // 8 == self.position // 8 and temp_position >=0: 
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
            temp_position -= 1

        #LEFT-DOWN
        temp_position = self.position
        while temp_position-9 >= 0 and (temp_position-9)//8 == temp_position//8-1 and (temp_position-9)%8 == temp_position%8-1:
            temp_position -= 9
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
        #RIGHT-DOWN
        temp_position = self.position
        while temp_position-7 >= 0 and (temp_position-7)//8 == temp_position//8-1 and (temp_position-7)%8 == temp_position%8+1:
            temp_position -= 7
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
        #LEFT-UP
        temp_position = self.position
        while temp_position+7 <= 63 and (temp_position+7)//8 == temp_position//8+1 and (temp_position+7)%8 == temp_position%8-1:
            temp_position += 7
            if board[temp_position] == ".":
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break
        #RIGHT-UP
        temp_position = self.position
        while temp_position+9 <= 63 and (temp_position+9)//8 == temp_position//8+1 and (temp_position+9)%8 == temp_position%8+1:
            temp_position += 9
            if board[temp_position] == ".": 
                move_list.append(temp_position)
            elif board[temp_position].color != self.color: 
                move_list.append(temp_position)
                break
            else: 
                break  
        return move_list


class King(ChessPiece): 
    def __init__(self, color: bool, position: int) -> None:
        super().__init__(color, position)
        self.valor = 9999
        if self.color: 
            self.symbol = "K"
        else: 
            self.symbol = "k"
    def legal_moves(self, board: list) -> list:
        move_list = list()

        #LEFT-DOWN
        if (self.position-9)//8 == self.position//8 - 1 and (self.position-9)%8 == self.position%8 -1 and self.position-9 >= 0: 
            if board[self.position-9] == "." or board[self.position-9].color != self.color: 
                move_list.append(self.position-9)
        #DOWN
        if (self.position-8)//8 == self.position//8 - 1 and (self.position-8)%8 == self.position%8 and self.position-8 >= 0: 
            if board[self.position-8] == "." or board[self.position-8].color != self.color: 
                move_list.append(self.position-8)
        #RIGHT-DOWN
        if (self.position-7)//8 == self.position//8 - 1 and (self.position-7)%8 == self.position%8 + 1 and self.position-7 >= 0: 
            if board[self.position-7] == "." or board[self.position-7].color != self.color: 
                move_list.append(self.position-7)
        #LEFT
        if (self.position-1)//8 == self.position//8 and (self.position-1)%8 == self.position%8 - 1 and self.position-1>=0: 
            if board[self.position-1] == "." or board[self.position-1].color != self.color: 
                move_list.append(self.position-1)
        #RIGHT
        if (self.position+1)//8 == self.position//8 and (self.position+1)%8 == self.position%8 +1 and self.position+1<=63: 
            if board[self.position+1] == "." or board[self.position+1].color != self.color: 
                move_list.append(self.position+1)
        #LEFT-UP
        if (self.position+7)//8 == self.position//8 + 1 and (self.position+7)%8 == self.position%8-1 and self.position+7<=63: 
            if board[self.position+7] == "." or board[self.position+7].color != self.color: 
                move_list.append(self.position+7)
        #UP
        if (self.position+8)//8 == self.position//8+1 and (self.position+8)%8 == self.position%8 and self.position+8 <=63: 
            if board[self.position+8] == "." or board[self.position+8].color != self.color: 
                move_list.append(self.position+8)
        #RIGHT-UP
        if (self.position+9)//8 == self.position//8+1 and (self.position+9)%8 == self.position % 8 + 1 and self.position+9 <= 63: 
            if board[self.position+9] == "." or board[self.position+9].color != self.color: 
                move_list.append(self.position+9)

        #CASTLING
        if not self.has_moved: 
            #KINGSIDE
            rook = board[self.position+3]
            if board[self.position+1] == "." and board[self.position+2] == "." and isinstance(rook, Rook): 
                if rook.color == self.color and not rook.has_moved: 
                    move_list.append(self.position+2)
            #QUEENSIDE
            rook = board[self.position-4]
            if board[self.position-1] == "." and board[self.position-2] == "." and board[self.position-3] == "." and isinstance(rook, Rook): 
                if rook.color == self.color and not rook.has_moved: 
                    move_list.append(self.position-2)

        return move_list
    def make_move(self, board: list, move: int) -> None:
        #CASTLING
        if abs(self.position-move) == 2: 
            if move-self.position > 0: 
                #KINGSIDE
                rook = board[self.position+3]
                if isinstance(rook, Rook): 
                    rook.make_move(board, self.position+1)
            else: 
                #QUEENSIDE
                rook = board[self.position-4]
                if isinstance(rook, Rook): 
                    rook.make_move(board, self.position-1)
        if isinstance(board[move], ChessPiece): 
            board[move].position = -1
        board[move] = self
        board[self.position] = "."
        self.position = move
        self.has_moved = True
    def undo_move(self, board: list, move: int) -> None:
        if abs(self.position-move) == 2: 
            if self.position%8 == 6: 
                #KINGSIDE
                rook = board[self.position-1]
                if isinstance(rook, Rook): 
                    rook.undo_move(board, self.position+1)
            else: 
                #QUEENSIDE
                rook = board[self.position+1]
                if isinstance(rook, Rook): 
                    rook.undo_move(board, self.position-2)
            rook.has_moved = False
        board[move] = self
        board[self.position] = "."
        self.position = move
        self.has_moved
