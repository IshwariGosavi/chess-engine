import chess
from engine.evaluate import evaluate

# Starting position
board = chess.Board()
print("Starting position:", evaluate(board))

# Knight developed to center (good square) vs knight on the rim (bad square)
board2 = chess.Board()
board2.push(chess.Move.from_uci("g1f3"))  # knight to a strong central-ish square
print("After Nf3 (good knight square):", evaluate(board2))

board3 = chess.Board()
board3.push(chess.Move.from_uci("b1a3"))  # knight to a weak rim square
print("After Na3 (weak knight square):", evaluate(board3))