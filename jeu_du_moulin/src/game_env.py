class JeuDuMoulinEnv:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = None
        self.player_red = None
        self.player_blue = None
        self.game_over = False

    def initialize_board(self):
        """Initialise un plateau vide (3x3 pour simplifier)."""
        return [[" " for _ in range(3)] for _ in range(3)]

    def reset_game(self):
        """Réinitialise le jeu."""
        self.board = self.initialize_board()
        self.current_player = None
        self.game_over = False

    def is_valid_move(self, row, col):
        """Vérifie si un mouvement est valide."""
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == " "

    def make_move(self, row, col, color):
        """Effectue un mouvement si valide."""
        if self.is_valid_move(row, col):
            self.board[row][col] = color
            return True
        return False

    def switch_player(self):
        """Change le joueur actuel."""
        if self.current_player == self.player_red:
            self.current_player = self.player_blue
        else:
            self.current_player = self.player_red