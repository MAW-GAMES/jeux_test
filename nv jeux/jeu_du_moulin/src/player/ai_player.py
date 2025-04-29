import random

class AIPlayer:
    def __init__(self, color):
        self.color = color

    def choose_move(self, valid_moves):
        """Choisit un mouvement aléatoire parmi les mouvements valides."""
        return random.choice(valid_moves)