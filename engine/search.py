import chess
from engine.evaluate import evaluate


def minimax(board, depth, alpha, beta, maximizing_player):
    """ Recursively explores the game tree up to `depth` moves ahead,
    using Alpha-Beta pruning to skip branches that can't affect
    the final decision.
    """
    
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing_player:
        # White's turn: try to find the move with the HIGHEST score.
        max_eval = -float('inf')

        for move in board.legal_moves:
            board.push(move)  # play the move hypothetically
            eval_score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()  # undo it, so we can try the next move

            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)

            # Pruning: if Black already has a better option elsewhere
            # (beta), Black would never let the game reach this branch.
            # No point exploring further down this path.
            if beta <= alpha:
                break

        return max_eval

    else:
        # Black's turn: try to find the move with the LOWEST score
        # (most negative = best for Black).
        min_eval = float('inf')

        for move in board.legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()

            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)

            # Pruning: if White already has a better option elsewhere
            # (alpha), White would never let the game reach this branch.
            if beta <= alpha:
                break

        return min_eval


def get_best_move(board, depth):
    """
    Determines the best move for whoever's turn it currently is,
    by running Alpha-Beta minimax on every legal move from this
    position and picking whichever leads to the best outcome.
    """

    best_move = None
    maximizing = board.turn == chess.WHITE

    # Starting bounds: no guarantees yet for either side.
    alpha = -float('inf')
    beta = float('inf')

    # Start best_value at the "worst possible" value for whoever is
    # moving, so that any real move immediately looks better.
    if maximizing:
        best_value = -float('inf')
    else:
        best_value = float('inf')

    for move in board.legal_moves:
        board.push(move)
        # Evaluate this move by searching one level deeper,
        # from the opponent's perspective.
        value = minimax(board, depth - 1, alpha, beta, not maximizing)
        board.pop()

        if maximizing and value > best_value:
            best_value = value
            best_move = move
            alpha = max(alpha, best_value)

        elif not maximizing and value < best_value:
            best_value = value
            best_move = move
            beta = min(beta, best_value)

    return best_move