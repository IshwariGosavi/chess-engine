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

board = chess.Board()
move_history = []
game_mode = "bot"          # "bot" or "friend"
game_started = False       # has a mode been picked yet?
game_over_flag = False     # true if the game ended via resignation
game_over_message = None   # e.g. "White wins by resignation!"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/board")
def get_board():
    """
    Returns the full current state — used both for normal syncing
    and for restoring the game correctly after a page refresh.
    """
    return jsonify({
        "fen": board.fen(),
        "is_game_over": board.is_game_over() or game_over_flag,
        "turn": "white" if board.turn == chess.WHITE else "black",
        "mode": game_mode,
        "game_started": game_started,
        "game_over_message": game_over_message
    })


@app.route("/api/human-move", methods=["POST"])
def human_move():
    if board.is_game_over() or game_over_flag:
        return jsonify({"error": "Game is already over"}), 400

    data = request.get_json()
    move_uci = data.get("move")

    try:
        move = chess.Move.from_uci(move_uci)
    except ValueError:
        return jsonify({"error": "Invalid move format"}), 400

    if move not in board.legal_moves:
        return jsonify({"error": "Illegal move"}), 400

    san = board.san(move)
    board.push(move)
    move_history.append(san)

    return jsonify({
        "fen": board.fen(),
        "is_game_over": board.is_game_over(),
        "mode": game_mode
    })


@app.route("/api/engine-move")
def engine_move():
    if board.is_game_over() or game_over_flag:
        return jsonify({"error": "Game is already over"}), 400

    best_move = get_best_move(board, depth=3)
    san = board.san(best_move)
    board.push(best_move)
    move_history.append(san)

    return jsonify({
        "move": best_move.uci(),
        "fen": board.fen(),
        "is_game_over": board.is_game_over()
    })


@app.route("/api/moves")
def get_moves():
    return jsonify({"moves": move_history})


@app.route("/api/undo", methods=["POST"])
def undo_move():
    global move_history, game_over_flag, game_over_message

    moves_undone = 0

    if len(board.move_stack) > 0:
        board.pop()
        move_history.pop()
        moves_undone += 1

    if len(board.move_stack) > 0 and moves_undone == 1:
        board.pop()
        move_history.pop()
        moves_undone += 1

    # Undoing always un-ends the game — covers both checkmate
    # and resignation cases.
    game_over_flag = False
    game_over_message = None

    return jsonify({
        "fen": board.fen(),
        "moves_undone": moves_undone
    })


@app.route("/api/reset", methods=["POST"])
def reset_board():
    global board, move_history, game_over_flag, game_over_message
    board = chess.Board()
    move_history = []
    game_over_flag = False
    game_over_message = None
    return jsonify({"fen": board.fen()})


@app.route("/api/set-mode", methods=["POST"])
def set_mode():
    global board, move_history, game_mode, game_started
    global game_over_flag, game_over_message

    data = request.get_json()
    mode = data.get("mode")

    if mode not in ["bot", "friend"]:
        return jsonify({"error": "Invalid mode"}), 400

    game_mode = mode
    game_started = True
    board = chess.Board()
    move_history = []
    game_over_flag = False
    game_over_message = None

    return jsonify({"fen": board.fen(), "mode": game_mode})


@app.route("/api/resign", methods=["POST"])
def resign():
    global game_over_flag, game_over_message

    if board.is_game_over() or game_over_flag:
        return jsonify({"error": "Game is already over"}), 400

    resigning_side = "white" if board.turn == chess.WHITE else "black"
    winner = "black" if resigning_side == "white" else "white"

    game_over_flag = True
    game_over_message = winner.capitalize() + " wins by resignation!"

    return jsonify({
        "resigned": resigning_side,
        "winner": winner,
        "message": game_over_message
    })


if __name__ == "__main__":
    app.run(debug=True)