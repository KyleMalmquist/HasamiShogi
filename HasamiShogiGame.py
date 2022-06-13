# Name: Kyle Malmquist
# Date: 12-3-2021
# Description: A game of Hasami Shogi

class HasamiShogiGame:
    """
    Represents a game of Hasami Shogi
    """
    def __init__(self):
        """
        Creates a game of Hasami Shogi
        """
        self._game_state = 'UNFINISHED'  # Game state can be 'UNFINISHED', 'RED_WON', or 'BLACK_WON'
        self._active_player = 'BLACK'  # 'BLACK' starts and alternates turns with 'RED'
        self._black_captured_pieces = 0
        self._red_captured_pieces = 0

        # Game board represented by a dictionary of lists
        # 'B' = black pieces
        # 'R' = red pieces
        # '.' = unoccupied square
        self._game_board = {'x_axis': [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                            'a': ['a', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
                            'b': ['b', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                            'c': ['c', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                            'd': ['d', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                            'e': ['e', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                            'f': ['f', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                            'g': ['g', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                            'h': ['h', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                            'i': ['i', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
                            }

    def set_game_state(self, state):
        """
        Sets the game state
        """
        self._game_state = state

    def set_active_player(self, player):
        """
        Sets the active player
        """
        self._active_player = player

    def set_captured_pieces(self, color, amount):
        """
        Sets the amount of captured pieces for a color
        """
        if color == 'BLACK':
            self._black_captured_pieces += amount
        else:
            self._red_captured_pieces += amount

    def set_square_occupant(self, square, occupant):
        """
        Sets a the occupant of a square
        """
        # Formatting
        if occupant == 'BLACK':
            occupant = "B"
        elif occupant == 'RED':
            occupant = 'R'
        else:
            occupant = '.'

        row, column = square
        column = int(column)
        list_to_return = self._game_board.get(row)
        list_to_return[column] = occupant
        self._game_board[row] = list_to_return

    def get_game_state(self):
        """
        Returns the game state
        """
        return self._game_state

    def get_active_player(self):
        """
        Returns the active player
        """
        return self._active_player

    def get_number_captured_pieces(self, color):
        """
        Returns how many pieces of a color have been captured
        """
        if color == 'BLACK':
            return self._black_captured_pieces
        elif color == 'RED':
            return self._red_captured_pieces

    def get_square_occupant(self, square):
        """
        Returns the occupant of a square
        """
        row, column = square
        column = int(column)

        row = self._game_board.get(row)
        return_value = row[column]

        # Formatting
        if return_value == 'B':
            return 'BLACK'
        elif return_value == 'R':
            return 'RED'
        else:
            return 'NONE'

    def make_move(self, square_from, square_to):
        """
        Moves a piece from a square to another square if it is legal to do so, and captures any applicable pieces
        """
        if self.validate_move(square_from, square_to) is False:
            return False
        else:
            if self.get_active_player() == 'BLACK':
                self.set_square_occupant(square_from, 'None')
                self.set_square_occupant(square_to, 'BLACK')
                self.set_active_player('RED')
            else:
                self.set_square_occupant(square_from, 'None')
                self.set_square_occupant(square_to, 'RED')
                self.set_active_player('BLACK')

        # Capture pieces
        self.capture_check(square_to)

    def validate_move(self, square_from, square_to):
        """
        Validates that a move is legal
        """
        if self.get_square_occupant(square_from) != self.get_active_player():
            return False

        if self.get_game_state() != 'UNFINISHED':
            return False

        row_from, column_from = square_from
        row_to, column_to = square_to
        if row_from != row_to and column_from != column_to:
            return False

        if self.get_square_occupant(square_to) != 'NONE':
            return False

        # Stop pieces from jumping other pieces if attempting to move horizontally
        if row_from == row_to:
            if column_from < column_to:
                test_column = int(column_from) + 1
                while test_column <= int(column_to):
                    if self.get_square_occupant(row_from + str(test_column)) != 'NONE':
                        return False
                    test_column += 1
            else:
                test_column = int(column_from) - 1
                while test_column >= int(column_to):
                    if self.get_square_occupant(row_from + str(test_column)) != 'NONE':
                        return False
                    test_column -= 1

        # Stop pieces from jumping other pieces if attempting to move vertically
        if column_from == column_to:

            # Get a list of row values
            list_of_keys = []
            for key in self._game_board:
                list_of_keys.append(key)

            # Get the starting and ending row
            start = 0
            end = 0
            for key in list_of_keys:
                if key == row_from:
                    break
                else:
                    start += 1
            for key in list_of_keys:
                if key == row_to:
                    break
                else:
                    end += 1

            # Get a list of rows to check
            list_of_rows_to_check = []
            if start < end:
                start += 1
                while start <= end:
                    list_of_rows_to_check.append(list_of_keys[start])
                    start += 1
            else:
                start -= 1
                while start >= end:
                    list_of_rows_to_check.append(list_of_keys[start])
                    start -= 1

            # Return false if any pieces would be jumped
            for row in list_of_rows_to_check:
                if self.get_square_occupant(row + str(column_to)) != 'NONE':
                    return False

    def capture_check(self, square):
        """
        Captures any applicable pieces
        """
        color = self.get_square_occupant(square)

        # Corner captures
        if self.get_square_occupant('a2') and self.get_square_occupant('b1') == color:
            if self.get_square_occupant('a1') != color and self.get_square_occupant('a1') is not None:
                self.set_square_occupant('a1', 'NONE')
                if color == 'BLACK':
                    self.set_captured_pieces('RED', 1)
                else:
                    self.set_captured_pieces('BLACK', 1)
        if self.get_square_occupant('a8') and self.get_square_occupant('b9') == color:
            if self.get_square_occupant('a9') != color and self.get_square_occupant('a9') is not None:
                self.set_square_occupant('a9', 'NONE')
                if color == 'BLACK':
                    self.set_captured_pieces('RED', 1)
                else:
                    self.set_captured_pieces('BLACK', 1)
        if self.get_square_occupant('h1') and self.get_square_occupant('i2') == color:
            if self.get_square_occupant('i1') != color and self.get_square_occupant('i1') is not None:
                self.set_square_occupant('i1', 'NONE')
                if color == 'BLACK':
                    self.set_captured_pieces('RED', 1)
                else:
                    self.set_captured_pieces('BLACK', 1)
        if self.get_square_occupant('h9') and self.get_square_occupant('i8') == color:
            if self.get_square_occupant('i9') != color and self.get_square_occupant('i9') is not None:
                self.set_square_occupant('i9', 'NONE')
                if color == 'BLACK':
                    self.set_captured_pieces('RED', 1)
                else:
                    self.set_captured_pieces('BLACK', 1)

    def print_game_board(self):
        """
        Prints the game board
        """
        print('')
        for key in self._game_board:
            print(*self._game_board.get(key), sep=' ')
