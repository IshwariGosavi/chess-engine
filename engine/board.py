import chess


def create_board():
    """Returns a fresh board at the starting position."""
    return chess.Board()


def get_legal_moves(board):
    """Returns a list of all legal moves in the current position."""
    return list(board.legal_moves)


def make_move(board, move_uci):
    """
    Attempts to play a move given in UCI format (e.g. 'e2e4').
    Returns True if the move was legal and played, False otherwise.
    """
    move = chess.Move.from_uci(move_uci)
    if move in board.legal_moves:
        board.push(move)
        return True
    return False


def undo_move(board):
    """Undoes the last move played."""
    board.pop()


def is_game_over(board):
    """Returns True if the game has ended (checkmate, stalemate, draw, etc.)."""
    return board.is_game_over()


def get_result(board):
    """Returns the outcome of the game, or None if still in progress."""
    outcome = board.outcome()
    if outcome is None:
        return None
    return outcome.result()


def print_board(board):
    """Prints the board in a readable text format."""
    print(board)