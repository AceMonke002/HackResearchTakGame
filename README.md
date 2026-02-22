# Tak Game (Python)

This project is a Python-based implementation of the board game Tak with support for both Player vs Player and Player vs AI gameplay.

The primary focus of this project is learning game logic, state management, and basic AI decision-making rather than creating a perfect or complete Tak engine.

---

## Project Goals

- Practice implementing game rules and turn-based logic
- Learn how to represent and manage a dynamic game board
- Experiment with simple AI strategies and learning through memory
- Improve Python fundamentals such as classes, file I/O, and data structures
- Build a playable terminal-based game from scratch

---

## Features

- Configurable board size (default 3x3)
- Player vs Player mode
- Player vs AI mode
- Stack-based board system
- Flat stones and standing stones
- Win detection using road-style connections
- Simple AI with:
  - Blocking logic
  - Road-building logic
  - Random fallback moves
  - Persistent memory stored in JSON

---

## AI Behavior

The AI uses a layered decision-making approach:

1. Attempts to use stored successful moves from previous games
2. Tries to block the opponent from winning
3. Attempts to complete its own road
4. Falls back to a random valid move if no strategic option exists

AI performance improves over time by saving game outcomes to a local memory file (`ai_memory.json`).

---

## How to Run

1. Make sure Python 3 is installed
2. Clone the repository
3. Run the game from the terminal:

```bash
python3 tak_game.py
```

---

## Disclaimer

This project is an educational, non-commercial implementation inspired by the board game Tak.

It is intended solely for learning purposes, including practicing game logic, Python programming, and basic AI concepts. This project is not affiliated with, endorsed by, or connected to the official creators or publishers of Tak.

All trademarks and game concepts belong to their respective owners.
