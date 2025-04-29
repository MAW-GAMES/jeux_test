class HumanPlayer:
    def __init__(self, color):
        self.color = color

    def choose_move(self, valid_moves):
        """Demande au joueur humain de choisir un mouvement."""
        move = None
        while move not in valid_moves:
            try:
                move = input(f"Choisissez votre mouvement parmi {valid_moves} (format: row,col) : ")
                move = tuple(map(int, move.split(',')))
            except ValueError:
                print("Entrée invalide. Veuillez entrer une ligne et une colonne séparées par une virgule.")
        return move