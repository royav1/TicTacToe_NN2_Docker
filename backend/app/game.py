# backend/app/game.py

# Game result constants
RESULT_X_WINS = 1
RESULT_O_WINS = -1
RESULT_DRAW = 0
RESULT_NOT_OVER = None

CELL_X = 1
CELL_O = -1
CELL_EMPTY = 0


class TicTacToe:
    def __init__(self, board=None, current_player=1):
        self.board = board if board is not None else [0] * 9
        self.current_player = current_player
        self.current_winner = None

    def make_move(self, position: int) -> bool:
        if 0 <= position <= 8 and self.board[position] == 0:
            self.board[position] = self.current_player
            return True
        return False

    def play_move(self, position: int):
        """Returns a new TicTacToe object with the move applied (immutable style)."""
        if self.board[position] != 0:
            raise ValueError("Invalid move: Cell already occupied.")

        new_board = self.board.copy()
        new_board[position] = self.current_player
        return TicTacToe(board=new_board, current_player=-self.current_player)

    def switch_player(self):
        self.current_player *= -1

    def available_moves(self):
        return [i for i, val in enumerate(self.board) if val == 0]

    def is_full(self):
        return all(val != 0 for val in self.board)

    def check_winner(self):
        b = self.board
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for i, j, k in lines:
            if b[i] == b[j] == b[k] != 0:
                self.current_winner = b[i]
                return b[i]
        return None

    def get_game_result(self):
        winner = self.check_winner()
        if winner == 1:
            return RESULT_X_WINS
        elif winner == -1:
            return RESULT_O_WINS
        elif self.is_full():
            return RESULT_DRAW
        else:
            return RESULT_NOT_OVER

    def get_valid_move_indexes(self):
        return [i for i, cell in enumerate(self.board) if cell == 0]

    def get_illegal_move_indexes(self):
        return [i for i, cell in enumerate(self.board) if cell != 0]

    def get_player_symbol(self):
        return 'X' if self.current_player == 1 else 'O'

    def print_board(self):
        symbols = {1: 'X', -1: 'O', 0: ' '}
        for i in range(0, 9, 3):
            row = [symbols[self.board[i + j]] for j in range(3)]
            print(" | ".join(row))
            if i < 6:
                print("--+---+--")

    def copy(self):
        return TicTacToe(board=self.board.copy(), current_player=self.current_player)


# 🎮 Game loop runner (used in training/evaluation)
def play_game(player_x, player_o):
    game = TicTacToe()
    while game.get_game_result() is RESULT_NOT_OVER:
        if game.current_player == 1:
            game = player_x(game)
        else:
            game = player_o(game)
    return game
