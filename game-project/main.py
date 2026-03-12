import tkinter as tk
from src.gui import SimpleUI
from src.rules import apply_rules

class SpelesKoks:
    def __init__(self, sequence, player_score, computer_score, current_player):
        self.sequence = sequence
        self.player_score = player_score
        self.computer_score = computer_score
        self.current_player = current_player

        self.children = []  # nākamie stāvokļi 

def generate_children(node):

    for number in set(node.sequence):

        new_sequence = node.sequence.copy()
        new_sequence.remove(number)

        p1, p2 = apply_rules(
            node.player_score,
            node.computer_score,
            node.current_player,
            number
        )

        next_player = 2 if node.current_player == 1 else 1

        child = SpelesKoks(
            new_sequence,
            p1,
            p2,
            next_player
        )

        node.children.append(child)

def main():
    # Spēlētāju sākotnējie punkti
    p1, p2 = 100, 100
    # apply_rules(p1, p2, current_player, number)


    # Uzsākt spēles GUI
    root = tk.Tk()
    SimpleUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()