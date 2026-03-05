import tkinter as tk
from src.gui import SimpleUI
from src.rules import apply_rules


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