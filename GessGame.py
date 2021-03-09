# Author: Donald Logan Kiser
# Date: 05/19/2020
# Description:

class GessGame():
    """
    represents a game of Gess
    """
    def __init__(self):
        """
        initializes GessGame object s.t. all attributes are in their beginning state
        """
        self._board = Board()
        self._game_state = 'UNFINISHED'
        self._black_turn = True

    def get_board(self):
        """
        returns current state of the board
        """
        return self._board

    def get_game_state(self):
        """
        returns current game state
        """
        return self._game_state

    def get_black_turn(self):
        """
        returns boolean indicating whether it is black's turn
        """
        return self._black_turn

    def resign_game(self):
        """
        changes game state to indicate that the opposing player has won
        """
        if self._black_turn:
            self._game_state = 'WHITE_WON'
        elif not self._black_turn:
            self._game_state = 'BLACK_WON'

    def make_move(self, start, end):
        """
        attempt to move 3x3 piece w/ center at "start" to piece w/ center at "end"
        """
        # handle case where game has already been finished
        if self.game_is_finished():
            return False

        # define some convenient helper variables
        start_row = self.get_row(start)
        start_column = self.get_column(start)
        end_row = self.get_row(end)
        end_column = self.get_column(end)
        change_row = end_row - start_row
        change_column = end_column - start_column

        # handle case where starting piece coordinates are out of range
        if self.is_piece_out_of_range(start_row, start_column):
            return False

        # handle case where ending piece coordinates are out of range
        if self.is_piece_out_of_range(end_row, end_column):
            return False

        # handle case where requested move results in the same board state (zero distance)
        if change_row == 0 and change_column == 0:
            return False

        # handle case where both row/column changes are non-zero and not equal magnitude
        if change_row != 0 and change_column != 0 and abs(change_row) != abs(change_column):
            return False

        # define helper variables to represent the distance of the move
        distance = 0
        if change_row == 0:
            distance = abs(change_column)
        elif change_column == 0:
            distance = abs(change_row)
        elif change_row != 0 and change_column != 0:
            distance = abs(change_row)

        # define helper variables to represent single unit direction of desired move
        direction_row = 0
        direction_column = 0

        if change_row < 0:
            direction_row = -1
        elif change_row > 0:
            direction_row = 1

        if change_column < 0:
            direction_column = -1
        elif change_column > 0:
            direction_column = 1

        # initialize Piece object based on starting row and column
        current_piece = Piece(start_row, start_column, self._board)

        # handle case where requested piece contains no stones
        if self.is_no_stones(current_piece):
            return False

        # handle case where piece contains only the current player's stones
        if self._black_turn and not self.is_all_black_stones(current_piece):
            return False
        elif not self._black_turn and not self.is_all_white_stones(current_piece):
            return False

        # handle case where distance of move is not allowed for designated piece
        if not self.is_distance_allowed(current_piece, distance):
            return False

        # handle case where direction of move is allowed for designated piece
        if not self.is_direction_allowed(current_piece, direction_row, direction_column):
            return False

        # handle case where move is obstructed by a piece
        if self.is_move_obstructed(current_piece, direction_row, direction_column, distance):
            return False

        # copy board attribute in case board update results in destruction of player's final ring
        board_backup = self._board.board_deepcopy()

        # invalid move cases have been handled, now update board
        self.update_board(current_piece, direction_row, direction_column, distance)

        # update the boarder squares to make sure they are all containing '_' stones
        for count in range(20):
            self._board.update_board(0, count, '_')
            self._board.update_board(19, count, '_')
            self._board.update_board(count, 0, '_')
            self._board.update_board(count, 19, '_')

        # handle case where player attempts to destroy their final ring
        if self._black_turn and self.is_no_black_rings():
            self._board.restore_board_to_backup(board_backup)
            return False
        elif not self._black_turn and self.is_no_white_rings():
            self._board.restore_board_to_backup(board_backup)
            return False

        # handle case where either player destroys their opponents final ring
        if self._black_turn and self.is_no_white_rings():
            self._game_state = 'BLACK_WON'
            return True
        elif not self._black_turn and self.is_no_black_rings():
            self._game_state = 'WHITE_WON'
            return True

        # handle case where move was valid, but the player did not win the game
        self._black_turn = not self._black_turn
        return True

    def is_no_black_rings(self):
        """
        returns boolean indicating whether a black 3x3 ring exists on the board
        """
        for row in range(2, 18, 1):
            for column in range(2, 18, 1):
                piece = Piece(row, column, self._board)
                if piece.get_stone_list() == ['B', 'B', 'B', 'B', '_', 'B', 'B', 'B', 'B']:
                    return False

        return True

    def is_no_white_rings(self):
        """
        returns boolean indicating whether a white 3x3 ring exists on the board
        """
        for row in range(2, 18, 1):
            for column in range(2, 18, 1):
                piece = Piece(row, column, self._board)
                if piece.get_stone_list() == ['W', 'W', 'W', 'W', '_', 'W', 'W', 'W', 'W']:
                    return False

        return True

    def update_board(self, current_piece, direction_row, direction_column, distance):
        """
        update move's path to '_' and update stones at destination 3x3
        """
        # loop through move path and record indices visited by piece **NOTE: final destination excluded from loop
        working_piece = Piece(current_piece.get_center_row(), current_piece.get_center_column(), self._board)
        path_indices_set = []
        for index in range(distance):
            for indices in working_piece.get_indices_list():
                if indices not in path_indices_set:
                    path_indices_set.append(indices)
            working_piece = Piece(working_piece.get_center_row() + direction_row,
                                  working_piece.get_center_column() + direction_column, self._board)

        # loop through indices recorded above and update board
        for indices in path_indices_set:
            self._board.update_board(indices[0], indices[1], '_')

        # loop through squares in final destination and update board
        current_piece_squares = current_piece.get_square_list()
        working_piece_indices = working_piece.get_indices_list()
        for count in range(len(current_piece_squares)):
            self._board.update_board(working_piece_indices[count][0],
                                     working_piece_indices[count][1], current_piece_squares[count].get_stone())

    def is_move_obstructed(self, current_piece, direction_row, direction_column, distance):
        """
        return boolean indicating whether move is obstructed by stones
        """
        # loop through move path searching for obstructions **NOTE: final destination excluded from testing
        for index in range(distance - 1):
            next_piece = Piece(current_piece.get_center_row() + direction_row,
                               current_piece.get_center_column() + direction_column, self._board)
            current_piece_indices = current_piece.get_indices_list()
            next_piece_squares = next_piece.get_square_list()
            for next_square in next_piece_squares:
                if next_square.get_indices() not in current_piece_indices and next_square.get_stone() != '_':
                    return True

            # update pieces for next iteration
            current_piece = next_piece

        return False

    def is_direction_allowed(self, piece, direction_row, direction_column):
        """
        returns boolean indicating whether direction of requested move is valid
        """
        # handle case where border square in direction of move doesn't contain a black stone
        if self._black_turn and piece.get_stone_list_matrix()[direction_row + 1][direction_column + 1] != 'B':
            return False

        # handle case where border square in direction of move doesn't contain a white stone
        if not self._black_turn and piece.get_stone_list_matrix()[direction_row + 1][direction_column + 1] != 'W':
            return False

        return True

    def is_distance_allowed(self, piece, distance):
        """
        returns boolean indicating whether distance of requested move is within range
        """
        # handle case where center doesn't contain a black stone and move distance > 3
        if distance > 3 and self._black_turn and piece.get_c().get_stone() != 'B':
            return False

        # handle case where center doesn't contain a white stone and move distance > 3
        if distance > 3 and not self._black_turn and piece.get_c().get_stone() != 'W':
            return False

        return True

    def is_piece_out_of_range(self, row, column):
        """
        returns boolean indicating whether piece centered at (row, column) is out of range
        """
        if row not in range(1, 19, 1):
            return True
        elif column not in range(1, 19, 1):
            return True
        else:
            return False

    def is_all_white_stones(self, piece):
        """
        returns boolean indicating whether Piece object input contains all white stones
        """
        for stone in piece.get_stone_list():
            if stone == 'B':
                return False

        return True

    def is_all_black_stones(self, piece):
        """
        returns boolean indicating whether Piece object input contains all black stones
        """
        for stone in piece.get_stone_list():
            if stone == 'W':
                return False

        return True

    def is_no_stones(self, piece):
        """
        returns boolean indicating whether Piece object input contains no stones
        """
        for stone in piece.get_stone_list():
            if stone == 'W' or stone == 'B':
                return False

        return True

    def change_turn(self):
        """
        changes the boolean value of GessGame._black_turn
        """
        self._black_turn = not self._black_turn

    def get_indices(self, center):
        """
        receives string argument ('b6', 'e7', etc) and returns numeric indices in list format
        """
        indices = []

        # convert second coordinate to integer and append as first index
        indices.append(int(center[1:]) - 1)

        # convert first coordinate to integer and append as second index
        letter_index = ord(center[0]) - 97
        indices.append(letter_index)

        return indices

    def get_row(self, center):
        """
        receives string argument ('b6', 'e7', etc) and returns numeric row index
        """
        return int(center[1:]) - 1

    def get_column(self, center):
        """
        receives string argument ('b6', 'e7', etc) and returns numeric column index
        """
        return ord(center[0]) - 97

    def game_is_finished(self):
        """
        returns boolean indicating whether game_state is NOT 'UNFINISHED'
        """
        return self.get_game_state() != 'UNFINISHED'

class Board():
    """
    represents the board in a game of Gess
    """
    def __init__(self):
        """
        initializes the board according to beginning positions on chessvariants.com
        """
        self._board = [['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',1],
                       ['_','_','B','_','B','_','B','B','B','B','B','B','B','B','_','B','_','B','_','_',2],
                       ['_','B','B','B','_','B','_','B','B','B','B','_','B','_','B','_','B','B','B','_',3],
                       ['_','_','B','_','B','_','B','B','B','B','B','B','B','B','_','B','_','B','_','_',4],
                       ['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',5],
                       ['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',6],
                       ['_','_','B','_','_','B','_','_','B','_','_','B','_','_','B','_','_','B','_','_',7],
                       ['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',8],
                       ['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',9],
                       ['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',10],
                       ['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',11],
                       ['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',12],
                       ['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',13],
                       ['_','_','W','_','_','W','_','_','W','_','_','W','_','_','W','_','_','W','_','_',14],
                       ['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',15],
                       ['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',16],
                       ['_','_','W','_','W','_','W','W','W','W','W','W','W','W','_','W','_','W','_','_',17],
                       ['_','W','W','W','_','W','_','W','W','W','W','_','W','_','W','_','W','W','W','_',18],
                       ['_','_','W','_','W','_','W','W','W','W','W','W','W','W','_','W','_','W','_','_',19],
                       ['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',20],
                       ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t',21]]

    def get_board(self):
        return self._board

    def update_board(self, row, column, stone):
        """
        place stone at indices arguments
        """
        self._board[row][column] = stone

    def restore_board_to_backup(self, board_matrix):
        """
        restores Board._board attribute to a previous copy of the matrix
        """
        self._board = board_matrix

    def board_deepcopy(self):
        """
        returns a deep copy of the board attribute
        """
        new_board = []
        for row in self._board:
            new_board.append(row.copy())
        return new_board

class Piece():
    """
    represents a 3x3 piece in a game of Gess
    """
    def __init__(self, center_row, center_column, board):
        """
        initializes Gess game piece attributes according to coordinate arguments
        """
        self._center_row = center_row
        self._center_column = center_column
        self._nw = Square(center_row - 1,center_column - 1, board)
        self._n = Square(center_row - 1, center_column, board)
        self._ne = Square(center_row - 1, center_column + 1, board)
        self._w = Square(center_row, center_column - 1, board)
        self._c = Square(center_row, center_column, board)
        self._e = Square(center_row, center_column + 1, board)
        self._sw = Square(center_row + 1, center_column - 1, board)
        self._s = Square(center_row + 1, center_column, board)
        self._se = Square(center_row + 1, center_column + 1, board)

    def get_c(self):
        """
        return c attribute for Piece object
        """
        return self._c

    def get_center_row(self):
        """
        returns row index of Piece object
        """
        return self._center_row

    def get_center_column(self):
        """
        returns column index of Piece object
        """
        return self._center_column

    def get_square_list(self):
        """
        returns list of Square objects in current piece
        """
        return [self._nw, self._n, self._ne,
                self._w, self._c, self._e,
                self._sw, self._s, self._se]

    def get_indices_list(self):
        """
        returns list of lists of indices for Piece object
        """
        return [self._nw.get_indices(), self._n.get_indices(), self._ne.get_indices(),
                self._w.get_indices(), self._c.get_indices(), self._e.get_indices(),
                self._sw.get_indices(), self._s.get_indices(), self._se.get_indices()]

    def get_stone_list(self):
        """
        returns list of stones for Piece object
        """
        return [self._nw.get_stone(), self._n.get_stone(), self._ne.get_stone(),
                self._w.get_stone(), self._c.get_stone(), self._e.get_stone(),
                self._sw.get_stone(), self._s.get_stone(), self._se.get_stone()]

    def get_stone_list_matrix(self):
        """
        returns two dimensional list of lists of stones for Piece object
        """
        return [[self._nw.get_stone(), self._n.get_stone(), self._ne.get_stone()],
                [self._w.get_stone(), self._c.get_stone(), self._e.get_stone()],
                [self._sw.get_stone(), self._s.get_stone(), self._se.get_stone()]]

class Square():
    """
    represents a single 1x1 square in a game of Gess
    """
    def __init__(self, row, column, board):
        """
        initializes a Square object based on row and column coordinates passed
        """
        self._row = row
        self._column = column
        self._stone = board.get_board()[row][column]
        self._indices = [row, column]

    def get_stone(self):
        """
        returns the stone type located at the square
        """
        return self._stone

    def get_indices(self):
        """
        returns list of row and column indices for Square object
        """
        return self._indices

class InvalidMove(Exception):
    """

    """
    pass