import random
import tkinter as tk
from tkinter import messagebox
from ai import choose_move, choose_move_minimax

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

        #noteikumu poga
        self.rules_btn = tk.Button(top, text="Rules", width=10, command=self.show_rules)
        self.rules_btn.pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(self.control_frame, text="", anchor="center")

        self.canvas = tk.Canvas(root, width=780, height=380, bg="#cde0f2", highlightthickness=1)
        self.canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)

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
        if self.sequence is None:
            messagebox.showerror("Error", "Length must be between 15 and 25.")
            return
        self.start_btn.pack_forget()
        self.status.pack()

        self._draw_balls()
        self.status.config(text=f"Started. First: {self.first_player.get()} | AI: {self.ai_mode.get()}")

        if self.first_player.get() == "Computer":
            self.root.after(1000, self.computer_move)

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
                min_x = r + 10
                max_x = w - r - 10
                min_y = r + 10
                max_y = h - r - 10

                if max_x <= min_x:
                    max_x = min_x + 1
                if max_y <= min_y:
                    max_y = min_y + 1

                nx = random.randint(min_x, max_x)
                ny = random.randint(min_y, max_y)
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

        if self.current_player != "Player":
            return

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

        self.player_score, self.computer_score = self.apply_rules(
            self.player_score,
            self.computer_score,
            1,
            val

        )

        if self.player_score < 70:
            messagebox.showinfo("Game Over", "Player nokļuva zem 70 – Player zaudē!")
            self._end_game(winner="Computer wins!")
            return
        elif self.computer_score < 70:
            messagebox.showinfo("Game Over", "Computer nokļuva zem 70 – Computer zaudē!")
            self._end_game(winner="Player wins!")
            return    
                        
        self.player_label.config(text=f"Player: {self.player_score}")
        self.computer_label.config(text=f"Computer: {self.computer_score}")

        self.status.config(text=f"Picked: {val} | Remaining: {len(self.sequence)}")

        if not self.sequence:
            self._end_game()
            return

        self.current_player = "Computer"
        self.root.after(500, self.computer_move)

    def generate_sequence(self, input_number: int):

        num_sequence = []

        if not isinstance(input_number, int):
            print("error: input must be integer")
            return None

        if input_number < 15 or input_number > 25:
            print("error: numbers must be between 15 and 25")
            return None


        for n in range(input_number):
            random_int = random.randint(1, 4)
            num_sequence.append(random_int)

        return num_sequence

    def apply_rules(self, p1, p2, current_player, number, limits=70):
        if number == 1:
            if current_player == 1:
                p2 += 1
            else:
                p1 += 1
        elif number == 3:
            if current_player == 1:
                p2 += 3
            else:
                p1 += 3
        elif number == 2:
            if current_player == 1:
                p1 -= 4
            else:
                p2 -= 4
        elif number == 4:
            if current_player == 1:
                p1 -= 8
            else:
                p2 -= 8

        # Nepieļaut punktus zem 0 (vai var arī threshold, ja gribi)
        p1 = max(p1, 0)
        p2 = max(p2, 0)

        return p1, p2


    def show_rules(self):

        rules_text = (
            "Katram spēlētājam ir piešķirts 100 punktu.\n"
            "Spēlētāji izpilda gājienus pēc kārtas.\n"
            "Katrā gājienā izvēlas vienu skaitli.\n"
            "Ja tiek izņemts pāra skaitlis (2 vai 4), tad no spēlētāja punktu skaita tiek atņemta izņemtā skaitļa divkāršota summa.\n"
            "Ja tiek izņemts nepāra skaitlis (1 vai 3), tad šis skaitlis tiek pieskaitīts pretinieka punktu skaitam.\n"
            "Ja spēlētāja punkti nokrīt zem 70 — viņš ZAUDĒ uzreiz.\n"
            "Spēle beidzas, kad virkne ir tukša.\n"
            "Uzvar spēlētājs, kam spēles beigās ir palicis mazāk punktu.\n"
            "Neizšķirts rezultāts ir tad, kad abiem spēlētājiem spēles beigās ir vienāds punktu skaits."

        )

        messagebox.showinfo("Game Rules", rules_text)

    def computer_move(self):

        if not self.sequence:
            self._end_game()
            return

        if self.ai_mode.get() == "alphabeta":
            move = choose_move(
                self.sequence,
                self.player_score,
                self.computer_score,
                2
            )
        else:
            move = choose_move_minimax(
                self.sequence,
                self.player_score,
                self.computer_score,
                2
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
                    val,
                )

                self.update_ui_scores()

                            # Pārbaudīt 70 punktus vai tukšu virkni
                if self.player_score < 70:
                    messagebox.showinfo("Game Over", "Player nokļuva zem 70 – Player zaudē!")
                    self._end_game(winner="Computer wins!")
                    return
                elif self.computer_score < 70:
                    messagebox.showinfo("Game Over", "Computer nokļuva zem 70 – Computer zaudē!")
                    self._end_game(winner="Player wins!")
                    return
                elif not self.sequence:
                    self._end_game()  # šeit var atstāt tukšu, jo uzvarētāju nosaka pēc punktiem
                    return

                self.current_player = "Player"

                break


    def _end_game(self, winner: str = None):
        """
        Pabeidz spēli. 
        Ja 'winner' ir norādīts, izmanto to tieši.
        Ja nav, nosaka uzvarētāju pēc punktu salīdzinājuma.
        """

        if winner is None:
            if self.player_score < self.computer_score:
                winner = "Player wins!"
            elif self.player_score > self.computer_score:
                winner = "Computer wins!"
            else:
                winner = "Tie game!"

        # Rāda paziņojumu un piedāvā jaunu spēli
        play_again = messagebox.askyesno(
            "Game Over",
            f"Game finished!\n"
            f"Player: {self.player_score}\n"
            f"Computer: {self.computer_score}\n\n"
            f"{winner}\n\nStart a new game?"
        )

        self.current_player = None

        if play_again:
            self.status.pack_forget()
            self.start_btn.pack()
        else:
            self.status.config(text="Game finished.")

def main():

    root = tk.Tk()
    SimpleUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


# https://chatgpt.com/share/699f5f9e-d234-8010-83b5-d1d331d7c133
# https://chatgpt.com/share/69aefceb-eb9c-8003-a68e-39eb44212653
# https://chatgpt.com/share/69bab664-42d0-8006-bded-637c29436fa1 
# https://chatgpt.com/share/69b2fae5-85dc-8010-a553-12b2c13887ec (noteikumu poga)
# https://chatgpt.com/share/69b9bfab-960c-8008-8746-179a7b55b237 (fullscreen un gui error labojumi)
# https://chatgpt.com/share/69bf130c-094c-8010-becf-5f097637766e ( 70 punktu limits)
# https://chatgpt.com/share/69bf233b-78e8-8010-bb20-bc06c16e2821 (efektīvāk atjaunināt teksta laukus)