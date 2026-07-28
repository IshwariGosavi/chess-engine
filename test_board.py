from engine.board import (
    create_board,
    get_legal_moves,
    make_move,
    undo_move,
    is_game_over,
    get_result,
    print_board
)

board = create_board()
print("Starting position:")
print_board(board)
print()

print("Number of legal moves:", len(get_legal_moves(board)))
print()

success = make_move(board, "e2e4")
print("Played e2e4, success:", success)
print_board(board)
print()

failed = make_move(board, "e2e5")
print("Tried illegal move e2e5, success:", failed)
print()

undo_move(board)
print("After undoing:")
print_board(board)
print()

print("Is game over?", is_game_over(board))
print("Result:", get_result(board))