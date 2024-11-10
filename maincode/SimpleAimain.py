# import random
#
# class TakGame:
#     def __init__(self, size=3, ai=False):
#         self.size = size
#         self.board = [[[] for _ in range(size)] for _ in range(size)]  # Stack of pieces per tile
#         self.players = ['Player 1', 'Player 2']
#         self.ai = ai
#         self.current_player = 0
#
#     def print_board(self):
#         for row in self.board:
#             print(' | '.join([self.format_stack(stack) if stack else ' ' for stack in row]))
#             print('-' * (self.size * 4 - 1))
#
#     def format_stack(self, stack):
#         return stack[-1]  # Show the top stone only
#
#     def place_piece(self, x, y, piece_type):
#         # If the tile has a standing stone, no one can place a piece on it.
#         if self.board[x][y] and self.board[x][y][-1].startswith('S'):
#             print("Invalid move: standing stone blocks this tile.")
#             return False
#
#         piece = f'{piece_type}{self.current_player + 1}'
#         self.board[x][y].append(piece)  # Place the piece on top of the stack
#         return True
#
#     def switch_player(self):
#         self.current_player = 1 - self.current_player
#
#     def check_winner(self):
#         player_piece = f'F{self.current_player + 1}'
#         for i in range(self.size):
#             if all(self.get_top_piece(i, j) == player_piece for j in range(self.size)):
#                 return True
#             if all(self.get_top_piece(j, i) == player_piece for j in range(self.size)):
#                 return True
#
#         if all(self.get_top_piece(i, i) == player_piece for i in range(self.size)):
#             return True
#         if all(self.get_top_piece(i, self.size - i - 1) == player_piece for i in range(self.size)):
#             return True
#         return False
#
#     def get_top_piece(self, x, y):
#         if self.board[x][y]:
#             return self.board[x][y][-1]
#         return None
#
#     def ai_move(self):
#         # Step 1: Check if the player is about to win, and block them
#         if self.block_opponent():
#             return
#
#         # Step 2: Try to build the AI's own road by making smart moves
#         if self.build_ai_road():
#             return
#
#         # Step 3: If no critical moves, make a random valid move
#         self.random_ai_move()
#
#     def block_opponent(self):
#         # Block the player if they are close to winning
#         opponent_piece = f'F{self.current_player % 2 + 1}'
#         for i in range(self.size):
#             # Check rows
#             if sum(self.get_top_piece(i, j) == opponent_piece for j in range(self.size)) == self.size - 1:
#                 for j in range(self.size):
#                     if self.get_top_piece(i, j) is None:
#                         self.place_piece(i, j, 'F')
#                         print(f"AI blocks at ({i}, {j})")
#                         return True
#             # Check columns
#             if sum(self.get_top_piece(j, i) == opponent_piece for j in range(self.size)) == self.size - 1:
#                 for j in range(self.size):
#                     if self.get_top_piece(j, i) is None:
#                         self.place_piece(j, i, 'F')
#                         print(f"AI blocks at ({j}, {i})")
#                         return True
#         return False
#
#     def build_ai_road(self):
#         # Try to complete a road for the AI by making a strategic move
#         ai_piece = f'F{self.current_player + 1}'
#         for i in range(self.size):
#             # Check rows for AI to complete its own road
#             if sum(self.get_top_piece(i, j) == ai_piece for j in range(self.size)) == self.size - 1:
#                 for j in range(self.size):
#                     if self.get_top_piece(i, j) is None:
#                         self.place_piece(i, j, 'F')
#                         print(f"AI builds road at ({i}, {j})")
#                         return True
#             # Check columns for AI to complete its own road
#             if sum(self.get_top_piece(j, i) == ai_piece for j in range(self.size)) == self.size - 1:
#                 for j in range(self.size):
#                     if self.get_top_piece(j, i) is None:
#                         self.place_piece(j, i, 'F')
#                         print(f"AI builds road at ({j}, {i})")
#                         return True
#         return False
#
#     def random_ai_move(self):
#         # AI chooses a random valid tile and places a flat stone (F)
#         while True:
#             x = random.randint(0, self.size - 1)
#             y = random.randint(0, self.size - 1)
#             if self.board[x][y] and self.board[x][y][-1].startswith('S'):
#                 continue  # Skip if there's a standing stone
#             if self.place_piece(x, y, 'F'):
#                 print(f"AI places a flat stone at ({x}, {y})")
#                 break
#
#     def play_game(self):
#         print("Welcome to Tak! Players take turns placing stones.")
#         while True:
#             self.print_board()
#             if self.ai and self.current_player == 1:
#                 self.ai_move()
#             else:
#                 print(f"{self.players[self.current_player]}'s turn.")
#                 x = int(input(f"Enter the row (0-{self.size - 1}): "))
#                 y = int(input(f"Enter the column (0-{self.size - 1}): "))
#                 piece_type = input("Enter 'F' for flat stone or 'S' for standing stone: ").upper()
#
#                 if not self.place_piece(x, y, piece_type):
#                     continue  # Invalid move, ask again
#
#             if self.check_winner():
#                 print(f"{self.players[self.current_player]} wins!")
#                 self.print_board()
#                 break
#
#             self.switch_player()
#
#
# if __name__ == "__main__":
#     # Choose game mode: Player vs Player or Player vs AI
#     mode = input("Choose game mode: 1 for Player vs Player, 2 for Player vs AI: ")
#     if mode == '2':
#         game = TakGame(ai=True)  # Player vs AI
#     else:
#         game = TakGame()  # Player vs Player
#
#     game.play_game()