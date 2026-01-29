# 🎮 2048 Game with AI Difficulty

A Python implementation of the classic 2048 puzzle game with three intelligent difficulty levels powered by an Expectimax AI algorithm.

## ✨ Features

### Three AI-Powered Difficulty Modes:
- 🟢 **Easy:** AI spawns tiles in favorable positions to help you
- 🔵 **Medium:** Classic random spawning (original 2048 experience)
- 🔴 **Hard:** AI strategically places tiles to make the game challenging

### Other Features:
- **Smooth Animations:** Tiles slide and merge with fluid animations
- **Sound Effects:** Audio feedback for moves, merges, wins, and losses
- **Persistent High Score:** Your best score is saved between sessions
- **Clean UI:** Modern, colorful interface with difficulty indicators
- **Win Detection:** Celebrate when you reach 2048 (and keep playing if you want!)

## 📋 Requirements
- Python 3.11 or higher
- NumPy
- Pygame

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:HarvardEducatedVasik/2048.git
   cd GAME2048
Install dependencies:

Bash
pip install -r requirements.txt
Or install manually:

Bash
pip install numpy pygame pytest
First Run - Audio Setup: On first launch, you'll be asked if you want to download sound effects. Sound files (~100KB total) are automatically downloaded from the SoundFX collection. You can skip this and play without sound if preferred.

🎯 How to Play
Start the game:

Bash
python main.py
Select your difficulty from the menu.

Controls
⬆️ Up Arrow: Move tiles up

⬇️ Down Arrow: Move tiles down

⬅️ Left Arrow: Move tiles left

➡️ Right Arrow: Move tiles right

Game Rules
Tiles with the same number merge when they touch. Each move spawns a new tile (2 or 4). Combine tiles to reach 2048! The game ends when no moves are possible.

After Winning:

Press SPACE to continue playing for a higher score.

Press any other key to restart with difficulty selection.

🗂️ Project Structure
Plaintext
GAME2048/
├── ai/
│   ├── __init__.py
│   └── spawner.py       # AI difficulty system using Expectimax
├── game/
│   ├── __init__.py
│   ├── audio_manager.py # Sound effects system
│   ├── board.py         # Core game logic and board state
│   ├── utils.py         # Helper functions (tile merging, colors)
│   └── highscore.txt    # Persistent high score storage
├── rendering/
│   ├── __init__.py
│   ├── animation.py     # Tile animation system
│   ├── menu.py          # Difficulty selection menu
│   └── ui.py            # Game rendering and UI
├── tests/
│   ├── __init__.py
│   └── test_game.py     # Unit tests for core functionality
├── assets/              # Auto-downloaded sound files
│   ├── move.wav
│   ├── merge.wav
│   ├── win.wav
│   └── lose.wav
├── main.py              # Entry point - run this to play!
├── requirements.txt     # Python dependencies
└── README.md            # You are here
🧠 How the AI Works
The difficulty system uses the Expectimax algorithm to intelligently place tiles.

Algorithm Overview
Evaluation: For each empty cell, the AI simulates multiple moves (2-3) ahead.

Heuristics: Evaluates board states based on:

Empty tile count (more space = better for player)

Monotonicity (tiles flowing in one direction)

Smoothness (similar tiles adjacent)

Corner positioning (highest tile in corner = better)

Decision:

Easy: Picks positions with highest player score.

Hard: Picks positions with lowest player score.

Medium: Random (classic 2048).

Search Depth
Easy/Medium: 2 moves ahead

Hard: 3 moves ahead (more strategic)

🧪 Running Tests
Run the tests to verify game logic:

Bash
pytest tests/test_game.py -v
Test Coverage:

✅ Tile merging logic

✅ Board state management

✅ Move validation

✅ Win/lose conditions

✅ AI spawner behavior

🎵 Sound Credits
This game uses free, open-source sound effects from the SoundFX Collection by Dr. Ralf S. Engelschall. All sounds are licensed under either:

CC0 1.0 (Public Domain)

CC-BY 3.0 (Attribution required)

Specific sounds used:

Move: click1.mp3 - Subtle UI click

Merge: bling1.mp3 - Positive confirmation sound

Win: triumph1.mp3 - Victory fanfare

Lose: alarm2.mp3 - Game over alert

Attribution: Sound effects from SoundFX Collection © 2020-2022 Dr. Ralf S. Engelschall, licensed under CC0/CC-BY 3.0

🐛 Known Issues
Hard mode AI is very challenging (as intended!)

Slight delay when spawning on Hard difficulty due to deeper search

High score resets if highscore.txt is deleted

Enjoy the game and good luck reaching 2048! 🎉
