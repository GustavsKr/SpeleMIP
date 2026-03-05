import tkinter as tk
from src.gui import SimpleUI
from src.rules import apply_rules

class SpelesKoks():
    def __init__(self, generated_numbers, players_points, computers_points):
        self.generated_numbers = generated_numbers
        self.players_points = players_points
        self.computers_points = computers_points

        self.children = []  


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