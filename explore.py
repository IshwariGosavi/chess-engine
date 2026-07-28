import chess

# ---------- Day 1: Basics ----------

board = chess.Board()
print("Starting position:")
print(board)
print()

move1 = chess.Move.from_uci("e2e4")
print("Is e2e4 legal?", move1 in board.legal_moves)
board.push(move1)
print(board)
print()

move2 = chess.Move.from_uci("e7e5")
board.push(move2)
print(board)
print()

print("Is it check?", board.is_check())
print("Is it checkmate?", board.is_checkmate())
print("Whose turn (True=white):", board.turn)
print()

# Trying an illegal move on purpose
try:
    illegal = chess.Move.from_uci("e2e5")
    board.push(illegal)
except Exception as e:
    print("Error:", e)
print()


# ---------- Day 2: Understanding board state ----------

# FEN notation
board = chess.Board()
print("Starting FEN:", board.fen())

board.push(chess.Move.from_uci("e2e4"))
print("After e4:", board.fen())
print()

# Loading a position directly from FEN
custom_board = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
print("Custom board from FEN:")
print(custom_board)
print()

# Inspecting individual squares and pieces
board = chess.Board()

square = chess.E2
piece = board.piece_at(square)
print("Piece at e2:", piece)

print("All pieces on the board:")
for square in chess.SQUARES:
    piece = board.piece_at(square)
    if piece:
        print(chess.square_name(square), "->", piece.symbol())
print()

# Piece values and colors
piece = board.piece_at(chess.E1)
print("Piece type:", piece.piece_type)   # 6 = king
print("Piece color:", piece.color)       # True = white, False = black
print("Symbol:", piece.symbol())         # 'K' = white king
print()

# Game-over detection methods
print("is_checkmate:", board.is_checkmate())
print("is_stalemate:", board.is_stalemate())
print("is_insufficient_material:", board.is_insufficient_material())
print("is_game_over:", board.is_game_over())
print("outcome:", board.outcome())
print()

# Playing through a short scripted game (Ruy Lopez opening)
board = chess.Board()
moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"]

for m in moves:
    board.push(chess.Move.from_uci(m))

print("Board after Ruy Lopez opening moves:")
print(board)
print("Game over?", board.is_game_over())
print("Legal moves now:", len(list(board.legal_moves)))