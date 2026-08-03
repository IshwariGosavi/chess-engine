"""
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


@app.route("/api/engine-move")
def engine_move():
    """
    Asks the engine to calculate and play its best move
    on the current board, then returns the updated position.
    """
    if board.is_game_over():
        return jsonify({"error": "Game is already over"}), 400

    best_move = get_best_move(board, depth=3)
    board.push(best_move)

    return jsonify({
        "move": best_move.uci(),
        "fen": board.fen(),
        "is_game_over": board.is_game_over()
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

    board.push(move)

    return jsonify({
        "fen": board.fen(),
        "is_game_over": board.is_game_over()
    })

@app.route("/api/reset", methods=["POST"])
def reset_board():
    """Resets the board to the starting position."""
    global board
    board = chess.Board()
    return jsonify({"fen": board.fen()})


if __name__ == "__main__":
    app.run(debug=True)