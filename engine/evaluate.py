import chess

# Standard piece values used in most chess engines
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}


def evaluate_material(board):
    """
    Returns a score based purely on material.
    Positive = white is ahead, negative = black is ahead.
    """
    score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

    return score


def evaluate(board):
    """
    Main evaluation function. Checks for checkmate first,
    otherwise falls back to material count.
    """
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -9999
        else:
            return 9999

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    return evaluate_material(board)