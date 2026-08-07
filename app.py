"""
app.py

The Flask web server. This sits between the browser (frontend)
and the chess engine (engine/ folder). It serves the webpage and
exposes API endpoints the frontend calls to make moves and get
the engine's response.
"""

from flask import Flask, jsonify, render_template, request
import chess
from engine.search import get_best_move

app = Flask(__name__)

# For now, we keep a single global board in memory.
# (This is fine for a solo local project — a real multi-user app
# would need to track a separate board per session/user.)
board = chess.Board()
move_history = []  # stores moves in SAN format, e.g. ["e4", "e5", "Nf3", ...]
game_mode = "bot"  # can be "bot" or "friend"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/board")
def get_board():
    """
    Returns the current board position as a FEN string,
    plus whether the game has ended.
    """
    return jsonify({
        "fen": board.fen(),
        "is_game_over": board.is_game_over(),
        "turn": "white" if board.turn == chess.WHITE else "black"
    })


@app.route("/api/human-move", methods=["POST"])
def human_move():
    """
    Accepts a move from the human player (in UCI format, e.g. 'e2e4'),
    validates it's legal, and plays it if so.
    """
    data = request.get_json()
    move_uci = data.get("move")

    try:
        move = chess.Move.from_uci(move_uci)
    except ValueError:
        return jsonify({"error": "Invalid move format"}), 400

    if move not in board.legal_moves:
        return jsonify({"error": "Illegal move"}), 400

    san = board.san(move)  # get notation BEFORE pushing
    board.push(move)
    move_history.append(san)

    return jsonify({
        "fen": board.fen(),
        "is_game_over": board.is_game_over(),
        "mode": game_mode
    })


@app.route("/api/engine-move")
def engine_move():
    """
    Asks the engine to calculate and play its best move
    on the current board, then returns the updated position.
    """
    if board.is_game_over():
        return jsonify({"error": "Game is already over"}), 400

    best_move = get_best_move(board, depth=3)
    san = board.san(best_move)  # get notation BEFORE pushing
    board.push(best_move)
    move_history.append(san)

    return jsonify({
        "move": best_move.uci(),
        "fen": board.fen(),
        "is_game_over": board.is_game_over()
    })


@app.route("/api/moves")
def get_moves():
    """Returns the full move history in SAN notation."""
    return jsonify({"moves": move_history})


@app.route("/api/undo", methods=["POST"])
def undo_move():
    """
    Undoes the last two half-moves (your move + the engine's reply),
    so the human always gets their turn back.
    If there's only one move so far (engine hasn't replied yet,
    or it's the very first move), undoes just that one.
    """
    global move_history

    moves_undone = 0

    if len(board.move_stack) > 0:
        board.pop()
        move_history.pop()
        moves_undone += 1

    if len(board.move_stack) > 0 and moves_undone == 1:
        board.pop()
        move_history.pop()
        moves_undone += 1

    return jsonify({
        "fen": board.fen(),
        "moves_undone": moves_undone
    })


@app.route("/api/reset", methods=["POST"])
def reset_board():
    """Resets the board to the starting position."""
    global board, move_history
    board = chess.Board()
    move_history = []
    return jsonify({"fen": board.fen()})


@app.route("/api/set-mode", methods=["POST"])
def set_mode():
    """Sets the game mode ('bot' or 'friend') and resets the board."""
    global board, move_history, game_mode

    data = request.get_json()
    mode = data.get("mode")

    if mode not in ["bot", "friend"]:
        return jsonify({"error": "Invalid mode"}), 400

    game_mode = mode
    board = chess.Board()
    move_history = []

    return jsonify({"fen": board.fen(), "mode": game_mode})


if __name__ == "__main__":
    app.run(debug=True)