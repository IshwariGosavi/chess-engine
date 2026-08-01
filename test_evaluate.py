import chess
from engine.evaluate import evaluate

# Starting position — should be exactly 0 (equal material)
board = chess.Board()
print("Starting position score:", evaluate(board))

# Remove a black knight manually to simulate white being ahead
board.remove_piece_at(chess.B8)
print("After removing black's knight:", evaluate(board))

# Fool's mate — fastest possible checkmate, to test checkmate detection
board2 = chess.Board()
moves = ["f2f3", "e7e5", "g2g4", "d8h4"]
for m in moves:
    board2.push(chess.Move.from_uci(m))
print("Fool's mate position score:", evaluate(board2))
print("Is checkmate?", board2.is_checkmate())