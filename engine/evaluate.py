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

# Piece-square tables: bonus/penalty per square, from White's perspective.
# Index 0 = a1, index 63 = h8 (matches chess.SQUARES ordering).
# Values are in the same unit as material (roughly hundredths of a pawn... here, tenths of a point).

PAWN_TABLE = [
     0,   0,   0,   0,   0,   0,   0,   0,
     5,  10,  10, -20, -20,  10,  10,   5,
     5,  -5, -10,   0,   0, -10,  -5,   5,
     0,   0,   0,  20,  20,   0,   0,   0,
     5,   5,  10,  25,  25,  10,   5,   5,
    10,  10,  20,  30,  30,  20,  10,  10,
    50,  50,  50,  50,  50,  50,  50,  50,
     0,   0,   0,   0,   0,   0,   0,   0
]

KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

BISHOP_TABLE = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

ROOK_TABLE = [
     0,   0,   0,   0,   0,   0,   0,   0,
     5,  10,  10,  10,  10,  10,  10,   5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
    -5,   0,   0,   0,   0,   0,   0,  -5,
     0,   0,   0,   5,   5,   0,   0,   0
]

QUEEN_TABLE = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,   5,   5,   5,   0, -10,
     -5,   0,   5,   5,   5,   5,   0,  -5,
      0,   0,   5,   5,   5,   5,   0,  -5,
    -10,   5,   5,   5,   5,   5,   0, -10,
    -10,   0,   5,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20
]

KING_TABLE = [
     20,  30,  10,   0,   0,  10,  30,  20,
     20,  20,   0,   0,   0,   0,  20,  20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]

PIECE_SQUARE_TABLES = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
    chess.KING: KING_TABLE
}

def evaluate_position(board):
    """
    Returns a score based on piece placement (positional value),
    using the piece-square tables above.
    Positive = white is better positioned, negative = black is.
    """
    score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            table = PIECE_SQUARE_TABLES[piece.piece_type]

            if piece.color == chess.WHITE:
                # Tables are written from White's perspective, so use the square directly.
                score += table[square]
            else:
                # For Black, flip the square vertically (mirror the table).
                mirrored_square = chess.square_mirror(square)
                score -= table[mirrored_square]

    return score

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
    otherwise combines material count and positional value.
    """
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -9999
        else:
            return 9999

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    material_score = evaluate_material(board) * 100  # convert to same scale as position tables
    position_score = evaluate_position(board)

    return material_score + position_score