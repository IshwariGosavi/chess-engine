import chess
import time
from engine.search import get_best_move

board = chess.Board()

print("Finding best move at depth 2...")
start = time.time()
move = get_best_move(board, 2)
end = time.time()

print("Best move:", move)
print("Time taken:", round(end - start, 2), "seconds")