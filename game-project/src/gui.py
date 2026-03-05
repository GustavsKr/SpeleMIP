
import random
import tkinter as tk
from tkinter import messagebox
from generator import generate_sequence

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
        self.root.minsize(820, 520)

        self.sequence = []
        self.player_score = 100
        self.computer_score = 100
        self.ball_map = {}  # circle_id -> (text_id, value)

        top = tk.Frame(root, padx=10, pady=10)
        self.player_label = tk.Label(top, text="Player: 100", font=("Arial", 12, "bold"))
        self.player_label.pack(side=tk.LEFT, padx=20)

        self.computer_label = tk.Label(top, text="Computer: 100", font=("Arial", 12, "bold"))
        self.computer_label.pack(side=tk.LEFT, padx=20)
        top.pack(side=tk.TOP, fill=tk.X)

        tk.Label(top, text="First player:").pack(side=tk.LEFT, padx=(15, 5))
        self.first_player = tk.StringVar(value="Player")
        tk.Radiobutton(top, text="Player", variable=self.first_player, value="Player").pack(side=tk.LEFT)
        tk.Radiobutton(top, text="Computer", variable=self.first_player, value="Computer").pack(side=tk.LEFT)

        tk.Label(top, text="AI mode:").pack(side=tk.LEFT, padx=(15, 5))
        self.ai_mode = tk.StringVar(value="alphabeta")
        tk.Radiobutton(top, text="Alpha-Beta", variable=self.ai_mode, value="alphabeta").pack(side=tk.LEFT)
        tk.Radiobutton(top, text="Minimax", variable=self.ai_mode, value="minimax").pack(side=tk.LEFT)

        self.start_btn = tk.Button(top, text="Start", width=10, command=self.start_game)
        self.start_btn.pack(side=tk.LEFT, padx=12)

        self.status = tk.Label(top, text="", anchor="w")
        self.status.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        self.canvas = tk.Canvas(root, width=780, height=380, bg="#cde0f2", highlightthickness=1)
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)

    def start_game(self):
        n = self._read_length()
        if n is None:
            return

        self.player_score = 100
        self.computer_score = 100
        self.player_label.config(text=f"Player: {self.player_score}")
        self.computer_label.config(text=f"Computer: {self.computer_score}")

        self.sequence = generate_sequence(n)
        if self.sequence is None:
            messagebox.showerror("Error", "Length must be between 15 and 25.")
            return

        self._draw_balls()
        self.status.config(text=f"Started. First: {self.first_player.get()} | AI: {self.ai_mode.get()}")
        
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

    def _draw_balls(self):
        self.canvas.delete("all")
        self.ball_map.clear()

        w = int(self.canvas.winfo_width() or 780)
        h = int(self.canvas.winfo_height() or 380)

        r = 22
        padding = 12
        placed = []
        tries = 3000

        def ok(nx, ny):
            for px, py in placed:
                dx = nx - px
                dy = ny - py
                if dx * dx + dy * dy < (2 * r + padding) ** 2:
                    return False
            return True

        for val in self.sequence:
            x, y = None, None
            for _ in range(tries):
                nx = random.randint(r + 10, max(r + 10, w - r - 10))
                ny = random.randint(r + 10, max(r + 10, h - r - 10))
                if ok(nx, ny):
                    x, y = nx, ny
                    break
            if x is None:
                x = random.randint(r + 10, w - r - 10)
                y = random.randint(r + 10, h - r - 10)

            placed.append((x, y))
            circle_id = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=COLORS.get(val, "#d0d0d0"),
                outline="#3a3a3a",
                width=2
            )
            text_id = self.canvas.create_text(
                x, y, text=str(val),
                font=("Arial", 14, "bold"),
                fill="#1a1a1a"
            )
            self.ball_map[circle_id] = (text_id, val)

    def on_click(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if not items:
            return

        circle_id = None
        for item_id in items:
            if item_id in self.ball_map:
                circle_id = item_id
                break

        if circle_id is None:
            for item_id in items:
                for c_id, (t_id, _) in self.ball_map.items():
                    if t_id == item_id:
                        circle_id = c_id
                        break
                if circle_id is not None:
                    break

        if circle_id is None:
            return

        text_id, val = self.ball_map.pop(circle_id)
        self.canvas.delete(circle_id)
        self.canvas.delete(text_id)

        try:
            self.sequence.remove(val)
        except ValueError:
            pass

        self.status.config(text=f"Picked: {val} | Remaining: {len(self.sequence)}")

