import random
import json
import os


class TakGame:
    def __init__(self, size=3, ai=False):
        # Initialize the game with a board of the given size (default is 3x3)
        # and an optional AI opponent. The board is a grid of stacks, and
        # the current player starts at 0 (Player 1). If AI is enabled, it loads memory from a file.
        self.size = size
        self.board = [[[] for _ in range(size)] for _ in range(size)]
        self.players = ['Player 1', 'Player 2']
        self.ai = ai
        self.current_player = 0
        self.move_history = []
        self.memory_file = "ai_memory.json"
        self.ai_memory = self.load_ai_memory()

    def load_ai_memory(self):
        # Loads AI memory from a file if it exists; otherwise, returns an empty dictionary.
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_ai_memory(self):
        # Saves the current AI memory to a file.
        with open(self.memory_file, 'w') as f:
            json.dump(self.ai_memory, f)

    def print_board(self):
        # Prints the current state of the game board, showing each stack's top piece
        # and separating rows with lines.
        for row in self.board:
            print(' | '.join([self.format_stack(stack) if stack else ' ' for stack in row]))
            print('-' * (self.size * 4 - 1))

    def format_stack(self, stack):
        # Returns the top piece of the stack for display purposes.
        return stack[-1]

    def place_piece(self, x, y, piece_type):
        # Places a piece on the board at the given (x, y) position, as long as the top piece
        # is not a standing stone (which blocks the tile). Adds the move to history if successful.
        if self.board[x][y] and self.board[x][y][-1].startswith('S'):
            print("Invalid move: standing stone blocks this tile.")
            return False

        piece = f'{piece_type}{self.current_player + 1}'
        self.board[x][y].append(piece)
        self.move_history.append((x, y, piece_type, self.current_player))
        return True

    def switch_player(self):
        # Switches to the other player (0 to 1 or 1 to 0).
        self.current_player = 1 - self.current_player

    def check_winner(self):
        # Checks if the current player has won by forming a road (flat stones)
        # horizontally, vertically, or diagonally across the board.
        player_piece = f'F{self.current_player + 1}'
        for i in range(self.size):
            # Check rows and columns for a winning road
            if all(self.get_top_piece(i, j) == player_piece for j in range(self.size)):
                return True
            if all(self.get_top_piece(j, i) == player_piece for j in range(self.size)):
                return True

        # Check both diagonals for a winning road
        if all(self.get_top_piece(i, i) == player_piece for i in range(self.size)):
            return True
        if all(self.get_top_piece(i, self.size - i - 1) == player_piece for i in range(self.size)):
            return True
        return False

    def get_top_piece(self, x, y):
        # Returns the top piece of the stack at position (x, y), or None if the stack is empty.
        if self.board[x][y]:
            return self.board[x][y][-1]
        return None

    def ai_move(self):
        # Executes the AI's turn. It tries to find the best move from memory,
        # block the opponent, build a road, or make a random move.
        move = self.get_best_move()
        if move:
            x, y, piece_type = move
            if self.place_piece(x, y, piece_type):
                print(f"AI places a {piece_type} stone at ({x}, {y})")
                return

        if self.block_opponent():
            return
        if self.build_ai_road():
            return

        self.random_ai_move()

    def get_best_move(self):
        # Retrieves the best move from AI memory based on the current board state.
        state_key = self.board_to_key(self.board)
        if state_key in self.ai_memory:
            best_moves = sorted(self.ai_memory[state_key], key=lambda m: m["success"], reverse=True)
            return best_moves[0]["move"] if best_moves else None
        return None

    def board_to_key(self, board):
        # Converts the current board state into a string key for use in the AI memory.
        return str([[self.get_top_piece(x, y) for y in range(self.size)] for x in range(self.size)])

    def block_opponent(self):
        # AI tries to block the opponent if the opponent is one move away from winning.
        opponent_piece = f'F{self.current_player % 2 + 1}'
        for i in range(self.size):
            # Check rows for blocking opportunities
            if sum(self.get_top_piece(i, j) == opponent_piece for j in range(self.size)) == self.size - 1:
                for j in range(self.size):
                    if self.get_top_piece(i, j) is None:
                        self.place_piece(i, j, 'F')
                        print(f"AI blocks at ({i}, {j})")
                        return True

            # Check columns for blocking opportunities
            if sum(self.get_top_piece(j, i) == opponent_piece for j in range(self.size)) == self.size - 1:
                for j in range(self.size):
                    if self.get_top_piece(j, i) is None:
                        self.place_piece(j, i, 'F')
                        print(f"AI blocks at ({j}, {i})")
                        return True
        return False

    def build_ai_road(self):
        # AI tries to build its own road if it is one move away from completing it.
        ai_piece = f'F{self.current_player + 1}'
        for i in range(self.size):
            # Check rows for road-building opportunities
            if sum(self.get_top_piece(i, j) == ai_piece for j in range(self.size)) == self.size - 1:
                for j in range(self.size):
                    if self.get_top_piece(i, j) is None:
                        self.place_piece(i, j, 'F')
                        print(f"AI builds road at ({i}, {j})")
                        return True
            # Check columns for road-building opportunities
            if sum(self.get_top_piece(j, i) == ai_piece for j in range(self.size)) == self.size - 1:
                for j in range(self.size):
                    if self.get_top_piece(j, i) is None:
                        self.place_piece(j, i, 'F')
                        print(f"AI builds road at ({j}, {i})")
                        return True
        return False

    def random_ai_move(self):
        # If no strategic move is found, the AI places a flat stone at a random valid position.
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.board[x][y] and self.board[x][y][-1].startswith('S'):
                continue
            if self.place_piece(x, y, 'F'):
                print(f"AI places a flat stone at ({x}, {y})")
                break

    def update_ai_memory(self, winner):
        # Updates the AI memory with the result of the game,
        # saving successful or unsuccessful moves based on whether the AI won or lost.
        result = 1 if winner == 'AI' else -1
        for x, y, piece_type, player in self.move_history:
            if player == 1:
                state_key = self.board_to_key(self.board)
                if state_key not in self.ai_memory:
                    self.ai_memory[state_key] = []
                self.ai_memory[state_key].append({
                    "move": (x, y, piece_type),
                    "success": result
                })
        self.save_ai_memory()

    def play_game(self):
        # Main loop for playing the game. Alternates turns between the players
        # (or between player and AI) until one player wins.
        print("Welcome to Tak! Players take turns placing stones.")
        while True:
            self.print_board()
            if self.ai and self.current_player == 1:
                self.ai_move()
            else:
                print(f"{self.players[self.current_player]}'s turn.")
                x = int(input(f"Enter the row (0-{self.size - 1}): "))
                y = int(input(f"Enter the column (0-{self.size - 1}): "))
                piece_type = input("Enter 'F' for flat stone or 'S' for standing stone: ").upper()

                if not self.place_piece(x, y, piece_type):
                    continue

            if self.check_winner():
                winner = self.players[self.current_player]
                print(f"{winner} wins!")
                self.print_board()
                if self.ai:
                    self.update_ai_memory(winner)
                break

            self.switch_player()


if __name__ == "__main__":
    # Start the game in either Player vs Player or Player vs AI mode based on user input.
    mode = input("Choose game mode: 1 for Player vs Player, 2 for Player vs AI: ")
    if mode == '2':
        game = TakGame(ai=True)
    else:
        game = TakGame()

    game.play_game()
