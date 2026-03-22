import random
import tkinter as tk
from tkinter import messagebox
from ai import choose_move  # Unified function for both alphabeta and minimax

COLORS = {
    1: "#5db2fd",
    2: "#5ce695",
    3: "#f7a32e",
    4: "#f44fb7",
}


class SimpleUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Number Balls Game")
        self.root.state("zoomed")

        self.sequence = []
        self.player_score = 100
        self.computer_score = 100
        self.ball_map = {}

        # --- Top controls ---
        top = tk.Frame(root, padx=10, pady=10)
        self.player_label = tk.Label(top, text="Player: 100", font=("Arial", 12, "bold"))
        self.player_label.pack(side=tk.LEFT, padx=20)

        self.computer_label = tk.Label(top, text="Computer: 100", font=("Arial", 12, "bold"))
        self.computer_label.pack(side=tk.LEFT, padx=20)
        top.pack(side=tk.TOP, fill=tk.X)

        tk.Label(top, text="Sequence length (15–25):").pack(side=tk.LEFT, padx=(15, 5))
        self.len_entry = tk.Entry(top, width=6)
        self.len_entry.insert(0, "15")
        self.len_entry.pack(side=tk.LEFT, padx=8)

        tk.Label(top, text="First player:").pack(side=tk.LEFT, padx=(15, 5))
        self.first_player = tk.StringVar(value="Player")
        tk.Radiobutton(top, text="Player", variable=self.first_player, value="Player").pack(side=tk.LEFT)
        tk.Radiobutton(top, text="Computer", variable=self.first_player, value="Computer").pack(side=tk.LEFT)

        tk.Label(top, text="AI mode:").pack(side=tk.LEFT, padx=(15, 5))
        self.ai_mode = tk.StringVar(value="alphabeta")
        tk.Radiobutton(top, text="Alpha-Beta", variable=self.ai_mode, value="alphabeta").pack(side=tk.LEFT)
        tk.Radiobutton(top, text="Minimax", variable=self.ai_mode, value="minimax").pack(side=tk.LEFT)

        self.control_frame = tk.Frame(top)
        self.control_frame.pack(side=tk.LEFT, padx=12)

        self.start_btn = tk.Button(self.control_frame, text="Start", width=10, command=self.start_game)
        self.start_btn.pack()

        self.rules_btn = tk.Button(top, text="Rules", width=10, command=self.show_rules)
        self.rules_btn.pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(self.control_frame, text="", anchor="center")

        self.canvas = tk.Canvas(root, width=780, height=380, bg="#cde0f2", highlightthickness=1)
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)

    # ----------------- Game logic -----------------
    def start_game(self):
        n = self._read_length()
        if n is None:
            return
        self.canvas.delete("all")
        self.ball_map.clear()

        self.current_player = self.first_player.get()
        self.player_score = 100
        self.computer_score = 100
        self.player_label.config(text=f"Player: {self.player_score}")
        self.computer_label.config(text=f"Computer: {self.computer_score}")

        self.sequence = self.generate_sequence(n)
        self.start_btn.pack_forget()
        self.status.pack()
        self._draw_balls()
        self.status.config(text=f"Started. First: {self.first_player.get()} | AI: {self.ai_mode.get()}")

        if self.first_player.get() == "Computer":
            self.root.after(1000, self.computer_move)

    def computer_move(self):
        if not self.sequence:
            self._end_game()
            return

        # Unified AI call for either algorithm
        move = choose_move(
            self.sequence,
            self.player_score,
            self.computer_score,
            2,
            algorithm=self.ai_mode.get(),
            depth=6  # Adjust depth for performance
        )

        for circle_id, (text_id, val) in list(self.ball_map.items()):
            if val == move:
                self.canvas.delete(circle_id)
                self.canvas.delete(text_id)
                self.ball_map.pop(circle_id)

                try:
                    self.sequence.remove(val)
                except ValueError:
                    pass

                self.player_score, self.computer_score = self.apply_rules(
                    self.player_score,
                    self.computer_score,
                    2,
                    val
                )

                self.update_ui_scores()

                if self.player_score < 70:
                    messagebox.showinfo("Game Over", "Player nokļuva zem 70 – Player zaudē!")
                    self._end_game(winner="Computer wins!")
                    return
                elif self.computer_score < 70:
                    messagebox.showinfo("Game Over", "Computer nokļuva zem 70 – Computer zaudē!")
                    self._end_game(winner="Player wins!")
                    return
                elif not self.sequence:
                    self._end_game()
                    return

                self.current_player = "Player"
                break

    # ----------------- Helper methods -----------------
    def update_ui_scores(self):
        self.player_label.config(text=f"Player: {self.player_score}")
        self.computer_label.config(text=f"Computer: {self.computer_score}")

    def _read_length(self):
        try:
            n = int(self.len_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Length must be an integer.")
            return None
        if not (15 <= n <= 25):
            messagebox.showerror("Error", "Length must be between 15 and 25.")
            return None
        return n

    def generate_sequence(self, n: int):
        return [random.randint(1, 4) for _ in range(n)]

    def _draw_balls(self):

        self.root.update_idletasks()
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()

        self.canvas.delete("all")
        self.ball_map.clear()

        w, h = int(self.canvas.winfo_width() or 780), int(self.canvas.winfo_height() or 380)
        r, padding = 22, 12
        placed = []

        def ok(nx, ny):
            for px, py in placed:
                if (nx - px)**2 + (ny - py)**2 < (2*r + padding)**2:
                    return False
            return True

        for val in self.sequence:
            for _ in range(3000):
                nx, ny = random.randint(r+10, w-r-10), random.randint(r+10, h-r-10)
                if ok(nx, ny):
                    break
            placed.append((nx, ny))
            circle_id = self.canvas.create_oval(nx-r, ny-r, nx+r, ny+r, fill=COLORS[val], outline="#3a3a3a", width=2)
            text_id = self.canvas.create_text(nx, ny, text=str(val), font=("Arial", 14, "bold"), fill="#1a1a1a")
            self.ball_map[circle_id] = (text_id, val)

    def on_click(self, event):
        if self.current_player != "Player": return
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        circle_id = next((item for item in items if item in self.ball_map), None)
        if circle_id is None: return

        text_id, val = self.ball_map.pop(circle_id)
        self.canvas.delete(circle_id)
        self.canvas.delete(text_id)

        try: self.sequence.remove(val)
        except ValueError: pass

        self.player_score, self.computer_score = self.apply_rules(self.player_score, self.computer_score, 1, val)
        self.update_ui_scores()

        if self.player_score < 70:
            messagebox.showinfo("Game Over", "Player nokļuva zem 70 – Player zaudē!")
            self._end_game(winner="Computer wins!")
            return
        elif self.computer_score < 70:
            messagebox.showinfo("Game Over", "Computer nokļuva zem 70 – Computer zaudē!")
            self._end_game(winner="Player wins!")
            return
        elif not self.sequence:
            self._end_game()
            return

        self.current_player = "Computer"
        self.root.after(500, self.computer_move)

    def apply_rules(self, p1, p2, current_player, number, limits=70):
        if number == 1:
            if current_player == 1: p2 += 1
            else: p1 += 1
        elif number == 2:
            if current_player == 1: p1 -= 4
            else: p2 -= 4
        elif number == 3:
            if current_player == 1: p2 += 3
            else: p1 += 3
        elif number == 4:
            if current_player == 1: p1 -= 8
            else: p2 -= 8
        return max(p1, 0), max(p2, 0)

    def show_rules(self):
        rules_text = (
            "Katram spēlētājam ir 100 punkti.\n"
            "Gājieni pēc kārtas.\n"
            "Izvēloties pāra skaitli (2 vai 4), tas tiek atņemts no punktiem divkārši.\n"
            "Izvēloties nepāra skaitli (1 vai 3), tas tiek pieskaitīts pretinieka punktiem.\n"
            "Ja punkti nokrīt zem 70 - zaudējums.\n"
            "Spēle beidzas, kad virkne tukša.\n"
            "Uzvar tas, kam mazāk punktu.\n"
            "Neizšķirts, ja vienādi punkti."
        )
        messagebox.showinfo("Game Rules", rules_text)

    def _end_game(self, winner=None):
        if winner is None:
            if self.player_score < self.computer_score: winner = "Player wins!"
            elif self.player_score > self.computer_score: winner = "Computer wins!"
            else: winner = "Tie game!"

        play_again = messagebox.askyesno(
            "Game Over",
            f"Player: {self.player_score}\nComputer: {self.computer_score}\n{winner}\nStart a new game?"
        )
        self.current_player = None
        if play_again:
            self.status.pack_forget()
            self.start_btn.pack()
        else:
            self.status.config(text="Game finished.")

import sys

def main():
    root = tk.Tk()
    
    # cross-platform window sizing
    if sys.platform == "darwin":  # macOS
        root.geometry("1024x768")
    else:
        root.state("zoomed")
    
    SimpleUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# https://chatgpt.com/share/699f5f9e-d234-8010-83b5-d1d331d7c133
# https://chatgpt.com/share/69aefceb-eb9c-8003-a68e-39eb44212653
# https://chatgpt.com/share/69bab664-42d0-8006-bded-637c29436fa1 
# https://chatgpt.com/share/69b2fae5-85dc-8010-a553-12b2c13887ec (noteikumu poga)
# https://chatgpt.com/share/69b9bfab-960c-8008-8746-179a7b55b237 (fullscreen un gui error labojumi)
# https://chatgpt.com/share/69bf130c-094c-8010-becf-5f097637766e (70 punktu limits)
# https://chatgpt.com/share/69bf233b-78e8-8010-bb20-bc06c16e2821 (efektīvāk atjaunināt teksta laukus)