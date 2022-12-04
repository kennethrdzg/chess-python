from chess_pieces import *
from re import fullmatch
from math import inf, isinf

def print_board(board: list, turn: bool)->None: 
    if turn: 
        for i in range(7, -1, -1): 
            rank = str(i+1) + " "
            for j in range(8):
                rank += str(board[i*8+j]) + " "
            print(rank)
        print("  A B C D E F G H \n")
    else: 
        for i in range(8): 
            rank = str(i+1)+" "
            for j in range(7, -1, -1): 
                rank += str(board[i*8+j])+" "
            print(rank)
        print("  H G F E D C B A \n")

def is_in_check(board: list, turn: bool, white_pieces: list, black_pieces: list)->bool: 

    if turn:
        player_pieces = white_pieces
        enemy_pieces = black_pieces
    else: 
        player_pieces = black_pieces
        enemy_pieces = white_pieces
    king = None
    for piece in player_pieces: 
        if isinstance(piece, King): 
            king = piece.position
            break
    for piece in enemy_pieces: 
        if piece.position >= 0 and piece.position <= 63: 
            move_list = piece.legal_moves(board)
            if king in move_list: 
                return True
    return False

def square_to_num(square: str)->int: 
    file = "abcdefgh".find(square[0])
    if file == -1: 
        return -1
    rank = int(square[1])
    if rank <1 or rank > 8: 
        return -1
    return (rank-1)*8+file

def num_to_square(num: int)->str: 
    if num == -1: 
        return "None"
    return "ABCDEFGH"[num%8] + str(num//8+1)

def create_board()->list: 
    board = ["." for i in range(64)]
    #WHITE PIECES
    board[0] = Rook(True, 0)
    board[1] = Knight(True, 1)
    board[2] = Bishop(True, 2)
    board[3] = Queen(True, 3)
    board[4] = King(True, 4)
    board[5] = Bishop(True, 5)
    board[6] = Knight(True, 6)
    board[7] = Rook(True, 7)
    for i in range(8, 16): 
        board[i] = Pawn(True, i)
    #BLACK PIECES
    for i in range(48, 56): 
        board[i] = Pawn(False, i)
    board[56] = Rook(False, 56)
    board[57] = Knight(False, 57)
    board[58] = Bishop(False, 58)
    board[59] = Queen(False, 59)
    board[60] = King(False, 60)
    board[61] = Bishop(False, 61)
    board[62] = Knight(False, 62)
    board[63] = Rook(False, 63)
    return board

#Returns all legal moves for a specific piece. 
def all_legal_moves(board: list, piece: ChessPiece, white_pieces: list, black_pieces: list)->list: 
    if piece.position < 0 or piece.position > 63: 
        return []
    temp_move_list = piece.legal_moves(board)
    move_list = temp_move_list.copy()
    for move in temp_move_list: 
        #If King is in check it cannot castle
        if is_in_check(board, piece.color, white_pieces, black_pieces) and isinstance(piece, King) and abs(piece.position-move) == 2: 
            move_list.remove(move)
            continue
        temp = board[move]
        starting_position = piece.position
        has_moved = piece.has_moved
        piece.make_move(board, move)
        #Remove move from move list if it leaves the king in check
        if is_in_check(board, piece.color, white_pieces, black_pieces): 
            move_list.remove(move)

        piece.undo_move(board, starting_position)
        board[move] = temp
        if isinstance(board[move], ChessPiece): 
            board[move].position = move
        piece.has_moved = has_moved
    return move_list

def number_of_moves(board: list, turn: bool, white_pieces: list, black_pieces: list)->int: 
    if turn: 
        pieces = white_pieces
    else: 
        pieces = black_pieces
    num = 0
    for piece in pieces: 
        num += len(all_legal_moves(board, piece, white_pieces, black_pieces))
    return num

def is_valid_move(move: str)->bool: 
    if len(move) != 4: 
        return False
    if fullmatch("[a-h][1-8][a-h][1-8]", move) is None: 
        return False
    if square_to_num(move[:2]) == -1: 
        return False
    if square_to_num(move[2:]) == -1: 
        return False
    return True

def validate_int(phrase: str)->int: 
    num = input(phrase).strip()
    while fullmatch("[1-9]", num) is None: 
        num = input("Please enter an integer between 1 and 9: ").strip()
    return int(num)

class Prometheus: 
    def __init__(self, color: bool) -> None:
        self.color = color

    def material_evaluation(self, white_pieces: list, black_pieces: list)->int: 
        value = 0
        for piece in white_pieces: 
            if piece.position >= 0 and piece.position <= 63: 
                value += piece.value
        for piece in black_pieces: 
            if piece.position >= 0 and piece.position <= 63: 
                value -= piece.value
        if self.color == BLACK: 
            return -value
        return value

    def mobility_evaluation(self, board: list, white_pieces: list, black_pieces: list)->int: 
        return number_of_moves(board, self.color, white_pieces, black_pieces) - number_of_moves(board, not self.color, white_pieces, black_pieces)

    def board_evaluation(self, board: list, white_pieces: list, black_pieces: list)->int: 
        queen_penalty = 0
        for piece in white_pieces: 
            if isinstance(piece, Queen): 
                queen_penalty -= len(all_legal_moves(board, piece, white_pieces, black_pieces))
        for piece in black_pieces: 
            if isinstance(piece, Queen): 
                queen_penalty += len(all_legal_moves(board, piece, white_pieces, black_pieces))
        if self.color == BLACK: 
            queen_penalty *= -1
        material_value = self.material_evaluation(white_pieces, black_pieces)
        mobility_value = self.mobility_evaluation(board, white_pieces, black_pieces)
        return material_value+mobility_value+queen_penalty
    def make_a_move(self, board: list, turn: bool, white_pieces: list, black_pieces: list, depth: int): 
        print("Thinking...")
        best_move = self.minimax(board, turn, white_pieces, black_pieces, depth)
        return (best_move["start"], best_move["move"])
    def minimax(self, board: list, turn: bool, white_pieces: list, black_pieces: list, depth: int, Max = True, alpha = -inf, beta = inf)->dict: 
        n = number_of_moves(board, turn, white_pieces, black_pieces)
        print_board(board, self.color)
        if depth == 0 or n == 0: 
            if n == 0: 
                if not is_in_check(board, turn, white_pieces, black_pieces): 
                    #STALEMATE
                    return {"start": -1, "move": -1, "value": 0}
                if turn == self.color: 
                    return {"start": -1, "move": -1, "value": -inf}
                else: 
                    return {"start": -1, "move": -1, "value": inf}
            return {"start": -1, "move": -1, "value": self.board_evaluation(board, white_pieces, black_pieces)}
        if turn == WHITE: 
            pieces = white_pieces
        else: 
            pieces = black_pieces
        if Max: 
            best_move = {"start": -1, "move": -1, "value": -inf}
            best_value = -inf
            for piece in pieces: 
                if isinstance(piece, ChessPiece): 
                    move_list = all_legal_moves(board, piece, white_pieces, black_pieces)
                    for move in move_list: 
                        temp = board[move]
                        starting_position = piece.position
                        has_moved = piece.has_moved
                        piece.make_move(board, move)
                        promoted = False
                        if isinstance(piece, Pawn) and piece.can_promote(): 
                            promoted = True
                            board[piece.position] = Queen(piece.color, piece.position)
                            piece.position = -1
                        best_value = max(best_value, self.minimax(board, not turn, white_pieces, black_pieces, depth -1, False, alpha, beta)["value"])
                        alpha = max(alpha, best_value)
                        if promoted: 
                            del board[move]
                            board[move] = piece
                            piece.position = move
                        piece.undo_move(board, starting_position)
                        board[move] = temp
                        if isinstance(board[move], ChessPiece): 
                            board[move].position = move
                        piece.has_moved = has_moved
                        if best_value > best_move["value"]: 
                            best_move = {"start": starting_position, "move": move, "value": best_value}
                        elif isinf(best_value): 
                            best_move = {"start": starting_position, "move": move, "value": best_value}
                        if beta < alpha: 
                            break
        else: 
            best_move = {"start": -1, "move": -1, "value": inf}
            best_value = inf
            for piece in pieces: 
                if isinstance(piece, ChessPiece): 
                    move_list = all_legal_moves(board, piece, white_pieces, black_pieces)
                    for move in move_list: 
                        temp = board[move]
                        starting_position = piece.position
                        has_moved = piece.has_moved
                        piece.make_move(board, move)
                        promoted = False
                        if isinstance(piece, Pawn) and piece.can_promote(): 
                            promoted = True
                            board[piece.position] = Queen(piece.color, piece.position)
                            piece.position = -1
                        best_value = min(best_value, self.minimax(board, not turn, white_pieces, black_pieces, depth -1, True, alpha, beta)["value"])
                        beta = min(beta, best_value)
                        if promoted: 
                            del board[move]
                            board[move] = piece
                            piece.position = move
                        piece.undo_move(board, starting_position)
                        board[move] = temp
                        if isinstance(board[move], ChessPiece): 
                            board[move].position = move
                        piece.has_moved = has_moved
                        if best_value < best_move["value"]: 
                            best_move = {"start": starting_position, "move": move, "value": best_value}
                        elif isinf(best_value): 
                            best_move = {"start": starting_position, "move": move, "value": best_value}
                        if beta < alpha: 
                            break
        return best_move

def player_color()->bool: 
    p = input("Would you like to play as white (W) or black (B)? ").strip().lower()
    while p != "b" and p != "w": 
        p = input("B/W: ").strip().lower()
    return p == "w"

def player_make_a_move(player: bool, board: list, white_pieces: list, black_pieces: list): 
    invalid_move = True
    while invalid_move: 
        move = input("Your move: ").strip().lower()
        while not is_valid_move(move): 
            move = input("Invalid move: "+move)
        starting_position = square_to_num(move[:2])
        final_position = square_to_num(move[2:])
        if isinstance(board[starting_position], ChessPiece) and board[starting_position].color == player: 
            move_list = all_legal_moves(board, board[starting_position], white_pieces, black_pieces)
            if final_position in move_list: 
                invalid_move = False
            else:
                print("Cannot move "+move[:2]+" to "+move[2:])
        else: 
            print(move[:2]+" is not a valid piece to move")
    return (starting_position, final_position)

def main_loop():
    board = create_board()
    white_pieces = list()
    black_pieces = list()
    for square in board: 
        if isinstance(square, ChessPiece): 
            if square.color: 
                white_pieces.append(square)
            else: 
                black_pieces.append(square)
    player = player_color()
    chessBot = Prometheus(not player)
    max_depth = validate_int("Search depth: ")
    turn = WHITE
    n = number_of_moves(board, turn, white_pieces, black_pieces)
    rnd = 1
    print("Input movements in long algebraic notation (ex: \"b2b4\")")
    while n > 0: 
        print_board(board, turn)
        if turn == WHITE: 
            print("WHITE ("+str(rnd)+")")
        else: 
            print("BLACK ("+str(rnd)+")")

        if turn == player: 
            starting_position, final_position = player_make_a_move(player, board, white_pieces, black_pieces)
        else: 
            starting_position, final_position = chessBot.make_a_move(board, turn, white_pieces, black_pieces, max_depth)
        
        
        piece = board[starting_position]
        if isinstance(piece, ChessPiece): 
            piece.make_move(board, final_position)
            if isinstance(piece, Pawn) and piece.can_promote(): 
                if turn == player: 
                    board[piece.position] = piece.promote()
                    del piece
                else: 
                    board[piece.position] = Queen(turn, piece.position)
                    del piece
        #END OF TURN
        white_pieces.clear()
        black_pieces.clear()
        for square in board: 
            if isinstance(square, ChessPiece): 
                if square.color == WHITE: 
                    white_pieces.append(square)
                else: 
                    black_pieces.append(square)
        if turn == BLACK: 
            rnd += 1
        turn = not turn
        n = number_of_moves(board, turn, white_pieces, black_pieces)
        print("-"*20)
    print_board(board, turn)
    if is_in_check(board, turn, white_pieces, black_pieces): 
        if turn == WHITE: 
            print("BLACK WINS")
        else: 
            print("WHITE WINS")
    else: 
        print("STALEMATE")

def main(board: list, turn: bool, n: int, max_depth: int, rnd: int):
    white_pieces = list()
    black_pieces = list()
    for square in board: 
        if isinstance(square, ChessPiece): 
            if square.color: 
                white_pieces.append(square)
            else: 
                black_pieces.append(square)
    if n > 0: 
        print_board(board, turn)
        if turn == WHITE: 
            print("WHITE ("+str(rnd)+")")
        else: 
            print("BLACK ("+str(rnd)+")")

        #MINIMAX
        
        invalid_move = True
        while invalid_move: 
            move = input("Your move: ").strip().lower()
            while not is_valid_move(move): 
                move = input("Invalid move: "+move)
            starting_position = square_to_num(move[:2])
            final_position = square_to_num(move[2:])
            if isinstance(board[starting_position], ChessPiece) and board[starting_position].color == turn: 
                move_list = all_legal_moves(board, board[starting_position], white_pieces, black_pieces)
                if final_position in move_list: 
                    invalid_move = False
                else:
                    print("Cannot move "+move[:2]+" to "+move[2:])
            else: 
                print(move[:2]+" is not a valid piece to move")
        piece = board[starting_position]
        if isinstance(piece, ChessPiece): 
            piece.make_move(board, final_position)
            if isinstance(piece, Pawn) and piece.can_promote(): 
                board[piece.position] = piece.promote()
                del piece
        print("-"*20)

