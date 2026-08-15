# Chess Engine

A full-stack chess engine built from scratch, featuring a custom AI opponent powered by the Minimax algorithm with Alpha-Beta pruning. Play against the bot or challenge a friend, right in the browser.

🔗 **Live demo:**https://chess-engine-wwmm.onrender.com

## Features

- **Two game modes:** Play against the AI bot, or play locally against a friend (two humans, one board)
- **AI opponent** using Minimax search with Alpha-Beta pruning, evaluating positions using material count and piece-square tables
- **Legal move enforcement** : illegal moves are rejected and the board snaps back
- **Move history** displayed in standard algebraic notation (SAN), e.g. `1. e4 e5 2. Nf3 Nc6`
- **Undo** : reverses the last full round of moves
- **Resign** : end the game and declare the opponent the winner
- **Game-over detection** with specific reasons shown (checkmate, stalemate, draw by repetition, insufficient material, or resignation)
- **Pawn promotion** (auto-promotes to queen)
- **Persistent game state** : refreshing the page restores your game in progress

## Tech Stack

**Backend**
- Python 3
- [`python-chess`](https://python-chess.readthedocs.io/) — board representation, legal move generation, rules enforcement
- Flask — web server and REST API

**Frontend**
- HTML/CSS/JavaScript
- [`chessboard.js`](https://chessboardjs.com/) — interactive drag-and-drop chessboard rendering
- jQuery (chessboard.js dependency)

**AI**
- Minimax algorithm with Alpha-Beta pruning (custom implementation)
- Heuristic evaluation combining material count and piece-square tables

## How It Works

The project is split into four layers:

1. **Rules Engine** (`python-chess`) — handles legal move generation, check/checkmate detection, castling, en passant, and promotion. This project doesn't reimplement chess rules; it builds on this library.

2. **Evaluation Function** (`engine/evaluate.py`) — scores any board position numerically. Combines material count (pawn = 1, knight/bishop = 3, rook = 5, queen = 9) with piece-square tables that reward good piece placement (e.g., knights in the center over the corners).

3. **Search Algorithm** (`engine/search.py`) — the Minimax algorithm looks several moves ahead, assuming both sides play optimally, to pick the best move. Alpha-Beta pruning skips branches of the search tree that can't affect the final decision, making the search significantly faster without changing the result.

4. **Interface** (`app.py` + `templates/index.html`) — a Flask backend exposes a REST API (`/api/human-move`, `/api/engine-move`, `/api/undo`, etc.), and a `chessboard.js` frontend renders the board and talks to that API.

```
Human (browser) → Flask backend → python-chess (rules) → evaluate.py (scoring)
                                                          ↓
                                    search.py (Minimax + Alpha-Beta) → best move
                                                          ↓
                                    Flask backend → Human (browser) sees engine's move
```

## Project Structure

```
chess-engine/
├── engine/
│   ├── __init__.py
│   ├── board.py         # board handling helpers
│   ├── evaluate.py       # position evaluation (material + piece-square tables)
│   └── search.py         # Minimax + Alpha-Beta search
├── static/
├── templates/
│   └── index.html        # frontend: board, move list, controls
├── app.py                # Flask server and API routes
├── requirements.txt
└── README.md
```

## Running Locally

1. Clone the repository:
   ```
   git clone https://github.com/IshwariGosavi/chess-engine.git
   cd chess-engine
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the server:
   ```
   python app.py
   ```

5. Open your browser to `http://127.0.0.1:5000`

## Known Limitations

- Game state is stored in memory on the server, not per-user session — this works well for local/single-player use, but isn't designed for multiple simultaneous users on a deployed instance.
- The AI's search depth is fixed (depth 3 by default); deeper search means stronger but slower play.
- Pawn promotion always defaults to a queen (underpromotion isn't currently supported).

## Possible Future Improvements

- Replace hand-tuned evaluation weights with a trained ML model
- Add per-session game state for proper multi-user deployment
- Add difficulty levels by adjusting search depth
- Add an "explain this move" feature describing the engine's reasoning in plain language

## Author

Ishwari Gosavi
