import pygame
from game_env import JeuDuMoulinEnv
from player.human_player import HumanPlayer
from player.ai_player import AIPlayer

# Constants for the interface
WIDTH, HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 250, 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu du Moulin")

font = pygame.font.Font(None, 36)


def draw_button(text, x, y, color, text_color=WHITE):
    """Draw a button with text."""
    pygame.draw.rect(screen, color, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
    screen.blit(text_surface, text_rect)


def draw_game_board():
    """Draw the Jeu du Moulin game board with proper connections."""
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    square_sizes = [300, 200, 100]  # Outer, middle, and inner squares

    # Draw concentric squares
    for size in square_sizes:
        top_left = (center_x - size // 2, center_y - size // 2)
        pygame.draw.rect(screen, BLACK, (*top_left, size, size), 2)

    # Draw connecting lines between squares
    pygame.draw.line(screen, BLACK, (center_x - square_sizes[0] // 2, center_y), (center_x - square_sizes[1] // 2, center_y), 2)
    pygame.draw.line(screen, BLACK, (center_x + square_sizes[0] // 2, center_y), (center_x + square_sizes[1] // 2, center_y), 2)
    pygame.draw.line(screen, BLACK, (center_x, center_y - square_sizes[0] // 2), (center_x, center_y - square_sizes[1] // 2), 2)
    pygame.draw.line(screen, BLACK, (center_x, center_y + square_sizes[0] // 2), (center_x, center_y + square_sizes[1] // 2), 2)


def draw_tokens(board):
    """Draw tokens on the board."""
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    square_size = 100  # Distance between grid points

    for row in range(3):
        for col in range(3):
            if board[row][col] == "red":
                pygame.draw.circle(screen, RED, (center_x + (col - 1) * square_size, center_y + (row - 1) * square_size), 15)
            elif board[row][col] == "blue":
                pygame.draw.circle(screen, BLUE, (center_x + (col - 1) * square_size, center_y + (row - 1) * square_size), 15)


def main_menu():
    """Display the main menu to choose game mode and token color."""
    running = True
    game_mode = None
    player1_color = None
    player2_color = None

    while running:
        screen.fill(WHITE)

        # Draw title
        title_surface = font.render("Jeu du Moulin", True, BLACK)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 8))
        screen.blit(title_surface, title_rect)

        # Draw buttons for game mode
        draw_button("Play vs Player", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 4, GRAY)
        draw_button("Play vs AI", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 4 + 100, GRAY)

        # Draw buttons for token color
        draw_button("Red", WIDTH // 4 - BUTTON_WIDTH // 2, HEIGHT // 2 + 100, RED)
        draw_button("Blue", WIDTH // 4 * 3 - BUTTON_WIDTH // 2, HEIGHT // 2 + 100, BLUE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Check for game mode selection
                if WIDTH // 2 - BUTTON_WIDTH // 2 <= x <= WIDTH // 2 + BUTTON_WIDTH // 2:
                    if HEIGHT // 4 <= y <= HEIGHT // 4 + BUTTON_HEIGHT:
                        game_mode = "player_vs_player"
                    elif HEIGHT // 4 + 100 <= y <= HEIGHT // 4 + 100 + BUTTON_HEIGHT:
                        game_mode = "player_vs_ai"

                # Check for token color selection
                if WIDTH // 4 - BUTTON_WIDTH // 2 <= x <= WIDTH // 4 + BUTTON_WIDTH // 2 and HEIGHT // 2 + 100 <= y <= HEIGHT // 2 + 100 + BUTTON_HEIGHT:
                    player1_color = "red"
                    player2_color = "blue"
                elif WIDTH // 4 * 3 - BUTTON_WIDTH // 2 <= x <= WIDTH // 4 * 3 + BUTTON_WIDTH // 2 and HEIGHT // 2 + 100 <= y <= HEIGHT // 2 + 100 + BUTTON_HEIGHT:
                    player1_color = "blue"
                    player2_color = "red"

                # Start the game if both game mode and colors are selected
                if game_mode and player1_color and player2_color:
                    running = False

    return game_mode, player1_color, player2_color


def game_loop(game_mode, player1_color, player2_color):
    """Run the game loop."""
    env = JeuDuMoulinEnv()

    # Initialize players
    player1 = HumanPlayer(player1_color)
    player2 = HumanPlayer(player2_color) if game_mode == "player_vs_player" else AIPlayer(player2_color)

    # Assign players to the environment
    env.player_red = player1 if player1_color == "red" else player2
    env.player_blue = player2 if player1_color == "red" else player1
    env.current_player = env.player_red

    running = True
    while running:
        screen.fill(WHITE)

        # Draw the game board
        draw_game_board()

        # Draw tokens
        draw_tokens(env.board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and isinstance(env.current_player, HumanPlayer):
                x, y = event.pos
                # Convert mouse position to grid position
                center_x, center_y = WIDTH // 2, HEIGHT // 2
                square_size = 100
                col = (x - center_x + square_size) // square_size
                row = (y - center_y + square_size) // square_size

                if 0 <= row < 3 and 0 <= col < 3 and env.board[int(row)][int(col)] == " ":
                    env.board[int(row)][int(col)] = env.current_player.color
                    env.switch_player()

        # If it's the AI's turn
        if isinstance(env.current_player, AIPlayer):
            valid_moves = [(row, col) for row in range(3) for col in range(3) if env.is_valid_move(row, col)]
            if valid_moves:
                row, col = env.current_player.choose_move(valid_moves)
                env.make_move(row, col, env.current_player.color)
                env.switch_player()

        pygame.display.flip()


def main():
    """Main function to run the game."""
    game_mode, player1_color, player2_color = main_menu()
    game_loop(game_mode, player1_color, player2_color)


if __name__ == "__main__":
    main()