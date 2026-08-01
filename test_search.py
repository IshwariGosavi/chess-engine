import chess
import time
from engine.search import get_best_move

board = chess.Board()

for depth in [2, 3, 4]:
    print(f"Finding best move at depth {depth}...")
    start = time.time()
    move = get_best_move(board, depth)
    end = time.time()
    print("Best move:", move)
    print("Time taken:", round(end - start, 2), "seconds")
    print()