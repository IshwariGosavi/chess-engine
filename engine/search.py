import chess
from engine.evaluate import evaluate


def minimax(board, depth, maximizing_player):
    """
    Recursively explores the game tree up to `depth` moves ahead.
    Returns the best achievable score from this position.

    maximizing_player: True if it's White's turn to move (trying to maximize score),
                        False if it's Black's turn (trying to minimize score).
    """

    # Base case: stop recursing if we've hit our depth limit or the game is over
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval_score)
        return max_eval

    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval_score)
        return min_eval

def get_best_move(board, depth):
    """
    Returns the best move for the current player, searching `depth` moves ahead.
    """
    best_move = None
    maximizing = board.turn == chess.WHITE

    if maximizing:
        best_value = -float('inf')
    else:
        best_value = float('inf')

    for move in board.legal_moves:
        board.push(move)
        value = minimax(board, depth - 1, not maximizing)
        board.pop()

        if maximizing and value > best_value:
            best_value = value
            best_move = move
        elif not maximizing and value < best_value:
            best_value = value
            best_move = move

    return best_move