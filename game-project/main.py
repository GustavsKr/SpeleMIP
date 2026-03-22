import random
import tkinter as tk
from tkinter import messagebox
from ai import choose_move

COLORS = {
    1: "#5db2fd",
    2: "#5ce695",
    3: "#f7a32e",
    4: "#f44fb7",
}


class SimpleUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Spēle Number Balls")
        self.root.minsize(820, 520)

        self.sequence = []
        self.player_score = 100
        self.computer_score = 100
        self.current_player = None
        self.ball_map = {}

        top = tk.Frame(root, padx=10, pady=10)
        top.pack(side=tk.TOP, fill=tk.X)

        self.player_label = tk.Label(
            top, text="Spēlētājs: 100", font=("Arial", 12, "bold"), width=12, anchor="w"
        )
        self.player_label.grid(row=0, column=0, padx=8, pady=5)

        self.computer_label = tk.Label(
            top, text="Dators: 100", font=("Arial", 12, "bold"), width=14, anchor="w"
        )
        self.computer_label.grid(row=0, column=1, padx=8, pady=5)

        tk.Label(top, text="Secības garums (15–25):", anchor="w").grid(
            row=0, column=2, padx=8, pady=5
        )

        self.len_entry = tk.Entry(top, width=6, justify="center")
        self.len_entry.insert(0, "15")
        self.len_entry.grid(row=0, column=3, padx=8, pady=5)

        tk.Label(top, text="Pirmais spēlētājs:", anchor="w").grid(
            row=0, column=4, padx=8, pady=5
        )

        first_player_frame = tk.Frame(top)
        first_player_frame.grid(row=0, column=5, padx=8, pady=5)

        self.first_player = tk.StringVar(value="Spēlētājs")
        tk.Radiobutton(
            first_player_frame, text="Spēlētājs", variable=self.first_player, value="Spēlētājs"
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            first_player_frame, text="Dators", variable=self.first_player, value="Dators"
        ).pack(side=tk.LEFT)

        tk.Label(top, text="MI Mods:", anchor="w").grid(
            row=0, column=6, padx=8, pady=5
        )

        ai_frame = tk.Frame(top)
        ai_frame.grid(row=0, column=7, padx=8, pady=5)

        self.ai_mode = tk.StringVar(value="alphabeta")
        tk.Radiobutton(
            ai_frame, text="Alpha-Beta", variable=self.ai_mode, value="alphabeta"
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            ai_frame, text="Minimaks", variable=self.ai_mode, value="minimaks"
        ).pack(side=tk.LEFT)

        status_frame = tk.Frame(top)
        status_frame.grid(row=1, column=0, columnspan=8, sticky="w", padx=8, pady=5)

        self.start_btn = tk.Button(status_frame, text="Start", width=12, command=self.start_game)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 8))

        self.rules_btn = tk.Button(status_frame, text="Noteikumi", width=12, command=self.show_rules)
        self.rules_btn.pack(side=tk.LEFT, padx=(0, 12))

        self.status = tk.Label(
            status_frame,
            text="Izvēlieties pirmo spēlētāju, mākslīgā intelekta režīmu un secības garumu, pēc tam nospiediet Start.",
            anchor="w"
        )
        self.status.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.canvas = tk.Canvas(
            root,
            width=780,
            height=380,
            bg="#cde0f2",
            highlightthickness=1
        )
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
        self.player_label.config(text=f"Spēlētājs: {self.player_score}")
        self.computer_label.config(text=f"Dators: {self.computer_score}")

        self.sequence = self.generate_sequence(n)
        if self.sequence is None:
            messagebox.showerror("Kļūda", "Garumam jābūt no 15 līdz 25.")
            return

        self.start_btn.config(state=tk.DISABLED)

        self._draw_balls()
        self.status.config(
            text=f"Sākt. Pirmais: {self.first_player.get()} | MI: {self.ai_mode.get()}"
        )

        if self.first_player.get() == "Dators":
            self.root.after(1000, self.computer_move)

    
    def _read_length(self):
        try:
            n = int(self.len_entry.get().strip())
        except ValueError:
            messagebox.showerror("Kļūda", "Garumam jābūt veselam skaitlim.")
            return None

        if not (15 <= n <= 25):
            messagebox.showerror("Kļūda", "Garumam jābūt no 15 līdz 25.")
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
                x, y,
                text=str(val),
                font=("Arial", 14, "bold"),
                fill="#1a1a1a"
            )

            self.ball_map[circle_id] = (text_id, val)

    def check_early_end(self):
        if self.player_score < 70:
            messagebox.showinfo("Spēles beigas", "Spēlētājs nokrita zem 70 punktiem. Dators uzvarēja!")
            self._end_game()
            return True

        if self.computer_score < 70:
            messagebox.showinfo("Spēles beigas", "Dators nokrita zem 70 punktiem. Spēlētājs uzvarēja!")
            self._end_game()
            return True

        return False

    def on_click(self, event):
        if self.current_player != "Spēlētājs":
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

        self.sequence.remove(val)

        self.player_score, self.computer_score = self.apply_rules(
            self.player_score,
            self.computer_score,
            1,
            val
        )

        self.player_label.config(text=f"Spēlētājs: {self.player_score}")
        self.computer_label.config(text=f"Dators: {self.computer_score}")

        if self.check_early_end():
            return

        if not self.sequence:
            self._end_game()
            return

        self.current_player = "Dators"
        self.root.after(500, self.computer_move)

    def computer_move(self):
        if not self.sequence:
            self._end_game()
            return

        move = choose_move(
            self.sequence,
            self.player_score,
            self.computer_score,
            2,
            algorithm=self.ai_mode.get(),
            depth=6
        )

        for circle_id, (text_id, val) in list(self.ball_map.items()):
            if val == move:
                self.canvas.delete(circle_id)
                self.canvas.delete(text_id)
                self.ball_map.pop(circle_id)

                self.sequence.remove(val)

                self.player_score, self.computer_score = self.apply_rules(
                    self.player_score,
                    self.computer_score,
                    2,
                    val,
                )

                self.player_label.config(text=f"Spēlētājs: {self.player_score}")
                self.computer_label.config(text=f"Dators: {self.computer_score}")

                if self.check_early_end():
                    return

                if not self.sequence:
                    self._end_game()
                    return

                self.current_player = "Spēlētājs"
                break

    def generate_sequence(self, input_number: int):
        if not (15 <= input_number <= 25):
            return None
        return [random.randint(1, 4) for _ in range(input_number)]

    def apply_rules(self, p1, p2, current_player, number):
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
        return p1, p2

    def show_rules(self):
        rules_text = (
            "Katram spēlētājam ir piešķirts 100 punktu.\n"
            "Spēlētāji izpilda gājienus pēc kārtas.\n"
            "Katrā gājienā izvēlas vienu skaitli.\n"
            "Ja tiek izņemts pāra skaitlis, tad no spēlētāja punktu skaita tiek atņemta "
            "izņemtā skaitļa divkāršota summa.\n"
            "Ja tiek izņemts nepāra skaitlis, tad šis skaitlis tiek pieskaitīts "
            "pretinieka punktu skaitam.\n"
            "Ja kāda spēlētāja punktu skaits nokrīt zem 70, viņš automātiski zaudē spēli.\n"
            "Spēle beidzas, kad virkne ir tukša.\n"
            "Uzvar spēlētājs, kam spēles beigās ir palicis mazāk punktu.\n"
        )

        messagebox.showinfo("Spēles noteikumi", rules_text)

    def _end_game(self):
        if self.player_score < self.computer_score:
            winner = "Spēlētājs uzvarēja!"
        elif self.player_score > self.computer_score:
            winner = "Dators uzvarēja!"
        else:
            winner = "Neizšķirts!"

        play_again = messagebox.askyesno(
            "Spēles beigas",
            f"Spēlētājs: {self.player_score}\nDators: {self.computer_score}\n{winner}\n\nJauna spēle?"
        )

        self.current_player = None

        if play_again:
            self.start_btn.config(state=tk.NORMAL)
        else:
            self.status.config(text="Spēle pabeigta")


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
# https://chatgpt.com/share/69bf130c-094c-8010-becf-5f097637766e (70 punktu limits)
# https://chatgpt.com/share/69bf233b-78e8-8010-bb20-bc06c16e2821 (efektīvāk atjaunināt teksta laukus)