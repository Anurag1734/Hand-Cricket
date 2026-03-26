import tkinter as tk
from tkinter import messagebox
import random
from game import HandCricketGame
from player import Player, AIPlayer

class HandCricketUI:
    def __init__(self, root, user=None, ai=None):
        self.root = root  # ✅ This line is mandatory
        self.user = user or Player("You")
        self.ai = ai or AIPlayer("AI")
        self.game = HandCricketGame()
        self.first_innings_score = 0
        self.target = 0
        self.first_batter = ""
        self.first_score = 0
        self.user_score_final = 0
        self.ai_score_final = 0
        self.innings = 1  # To track which innings we're in


        self.show_start_screen()
    def show_start_screen(self):
        self.clear_screen()

        # Background frame
        start_frame = tk.Frame(self.root, bg="#f0f4f8")
        start_frame.pack(expand=True, fill=tk.BOTH)

        # Centered card
        card = tk.Frame(start_frame, bg="white", padx=40, pady=30, relief=tk.RIDGE, bd=2)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Game Title
        tk.Label(card, text="🏏 HandCricket", font=("Helvetica", 24, "bold"), fg="#2c3e50", bg="white").pack(pady=(0, 10))

        # Optional subtitle
        tk.Label(card, text="A fun single-player cricket game!", font=("Helvetica", 12), fg="#7f8c8d", bg="white").pack(pady=(0, 20))

        # Start Button
        start_button = tk.Button(
            card,
            text="Start Game ▶️",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg="#2c3e50",
            padx=20,
            pady=10,
            relief="raised",
            bd=3,
            highlightbackground="#d1d9e6",  # light shadow border
            activebackground="#f0f0f0",
            activeforeground="#2c3e50",
            command=self.show_toss_screen
        )
        start_button.pack(pady=10)


    def show_toss_screen(self):
        self.clear_screen()

        self.toss_frame = tk.Frame(self.root, pady=20)
        self.toss_frame.pack()

        tk.Label(self.toss_frame, text="🪙 Choose Odd or Even", font=("Helvetica", 14)).pack(pady=10)

        choice_frame = tk.Frame(self.toss_frame)
        choice_frame.pack()

        tk.Button(choice_frame, text="Odd", width=10, command=lambda: self.set_user_odd_even("odd")).pack(side=tk.LEFT, padx=10)
        tk.Button(choice_frame, text="Even", width=10, command=lambda: self.set_user_odd_even("even")).pack(side=tk.LEFT, padx=10)

        self.toss_choice_label = tk.Label(self.toss_frame, text="", font=("Helvetica", 12))
        self.toss_choice_label.pack(pady=10)

    def set_user_odd_even(self, choice):
        self.user_choice = choice
        self.toss_choice_label.config(text=f"You chose: {choice.upper()}")
        self.show_number_selection()

    def show_number_selection(self):
        tk.Label(self.toss_frame, text="Choose a number (1–6):", font=("Helvetica", 14)).pack(pady=10)
        num_frame = tk.Frame(self.toss_frame)
        num_frame.pack()

        for i in range(1, 7):
            tk.Button(num_frame, text=str(i), width=4, command=lambda n=i: self.resolve_toss(n)).pack(side=tk.LEFT, padx=5)

    def resolve_toss(self, user_num):
        ai_num = random.randint(1, 6)
        total = user_num + ai_num
        result_text = f"You chose {user_num}, AI chose {ai_num}. Total is {total} → "

        is_even = total % 2 == 0
        if (self.user_choice == "even" and is_even) or (self.user_choice == "odd" and not is_even):
            result_text += "You won the toss!"
            self.show_bat_bowl_choice()
        else:
            result_text += "AI won the toss!"
            self.ai_chooses_bat_or_bowl()

        self.toss_choice_label.config(text=result_text)

    def show_bat_bowl_choice(self):
        tk.Label(self.toss_frame, text="Choose to Bat or Bowl:", font=("Helvetica", 14)).pack(pady=10)
        choice_frame = tk.Frame(self.toss_frame)
        choice_frame.pack()

        tk.Button(choice_frame, text="Bat", width=10, command=lambda: self.start_match(user_bats=True)).pack(side=tk.LEFT, padx=10)
        tk.Button(choice_frame, text="Bowl", width=10, command=lambda: self.start_match(user_bats=False)).pack(side=tk.LEFT, padx=10)

    def ai_chooses_bat_or_bowl(self):
        ai_choice = random.choice(["bat", "bowl"])
        msg = f"AI chooses to {ai_choice.upper()}!"
        self.toss_choice_label.config(text=self.toss_choice_label.cget("text") + "\n" + msg)

        self.root.after(2000, lambda: self.start_match(user_bats=(ai_choice == "bowl")))

    def start_match(self, user_bats):
        self.clear_screen()
        if user_bats:
            self.prepare_match_screen(self.user, self.ai)
        else:
            self.prepare_match_screen(self.ai, self.user)

    def prepare_match_screen(self, striker, defender):
        self.striker = striker
        self.defender = defender

        if self.innings == 2:
            self.striker.reset()
            self.defender.reset()

        self.user_turn_frame = tk.Frame(self.root, bg="#f2f2f2", padx=20, pady=20)
        self.user_turn_frame.pack(pady=30)

        heading = tk.Label(self.user_turn_frame, text=f"{striker.name}'s Turn to Bat", font=("Arial", 16, "bold"), bg="#f2f2f2")
        heading.pack(pady=(0, 10))

        self.output_label = tk.Label(self.user_turn_frame, text="", font=("Courier", 12), bg="#f2f2f2")
        self.output_label.pack()

        self.score_label = tk.Label(self.user_turn_frame, text="Score: 0", font=("Helvetica", 14), fg="green", bg="#f2f2f2")
        self.score_label.pack(pady=10)

        if self.game.target:
            tk.Label(self.user_turn_frame, text=f"Target: {self.game.target}", font=("Helvetica", 12), bg="#f2f2f2").pack()

        button_frame = tk.Frame(self.user_turn_frame, bg="#f2f2f2")
        button_frame.pack(pady=10)

        for i in range(1, 7):
            btn = tk.Button(button_frame, text=str(i), font=("Arial", 14), width=4,
                            command=lambda num=i: self.play_turn(num))
            btn.grid(row=0, column=i, padx=5)

    def play_turn(self, user_input):
        if isinstance(self.defender, AIPlayer):
            ai_input = self.defender.get_input()  # AI bowls
            player_input = user_input             # Human bats
        else:
            ai_input = user_input                 # Human bowls
            player_input = self.striker.get_input()  # AI bats

        result_text = f"{self.defender.name} bowled: {ai_input}\n{self.striker.name} played: {player_input}"
        self.output_label.config(text=result_text)

        if player_input == ai_input:
            self.striker.is_out = True
            self.output_label.config(text=result_text + f"\n{self.striker.name} is OUT!")
            self.disable_buttons()

            if self.innings == 1:
                # First innings over
                self.game.first_innings_score = self.striker.get_score()
                self.game.target = self.game.first_innings_score + 1
                self.game.first_score = self.striker.get_score()
                self.game.first_batter = self.striker.name

                self.user_turn_frame.destroy()
                messagebox.showinfo("Innings Over", f"{self.striker.name} scored: {self.game.first_score}\nTarget for {self.defender.name}: {self.game.target}")
                
                self.innings = 2
                self.clear_screen()
                self.prepare_match_screen(self.defender, self.striker)
            else:
                # Second innings end
                if self.striker == self.user:
                    self.game.user_score_final = self.striker.get_score()
                    self.game.ai_score_final = self.game.first_score
                else:
                    self.game.ai_score_final = self.striker.get_score()
                    self.game.user_score_final = self.game.first_score

                self.user_turn_frame.destroy()
                self.show_result_screen()
            return

        self.striker.add_score(player_input)
        score = self.striker.get_score()
        self.score_label.config(text=f"Score: {score}")

        if self.game.target and score >= self.game.target:
            self.disable_buttons()
            if self.striker == self.user:
                self.game.user_score_final = score
                self.game.ai_score_final = self.game.first_score
            else:
                self.game.ai_score_final = score
                self.game.user_score_final = self.game.first_score

            self.output_label.config(text=result_text + f"\n{self.striker.name} chased the target! 🎯")
            self.user_turn_frame.destroy()
            self.show_result_screen()

    def show_result_screen(self):
        self.clear_screen()

        # Create a fullscreen container to center the result box
        container = tk.Frame(self.root, bg="#e9f1f7")
        container.pack(expand=True, fill=tk.BOTH)

        # Centered result box
        frame = tk.Frame(container, bg="white", padx=40, pady=30, relief=tk.RIDGE, bd=2)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        user_score = self.game.user_score_final
        ai_score = self.game.ai_score_final

        if user_score > ai_score:
            result = "🏆 You WIN! 🎉"
            result_color = "#27ae60"  # Soft Green
        elif user_score < ai_score:
            result = "😢 You LOSE!"
            result_color = "#e74c3c"  # Soft Red
        else:
            result = "🤝 It's a TIE!"
            result_color = "#3498db"  # Pleasant Blue

        tk.Label(frame, text="🏁 Match Result", font=("Helvetica", 18, "bold"), fg="#333", bg="white").pack(pady=(0, 15))

        score_text = f"👤 You: {user_score}   🤖 AI: {ai_score}"
        tk.Label(frame, text=score_text, font=("Helvetica", 14), fg="#555", bg="white").pack(pady=5)

        tk.Label(frame, text=result, font=("Helvetica", 16, "bold"), fg=result_color, bg="white").pack(pady=15)

        # Softer button color (teal-like)
        tk.Button(
            frame,
            text="Play Again 🔄",
            font=("Helvetica", 12, "bold"),
            bg="#20c997",       # Soft Teal
            fg="white",
            padx=12,
            pady=6,
            relief=tk.FLAT,
            activebackground="#17a589",
            activeforeground="white",
            command=self.restart_game
        ).pack(pady=10)


    def disable_buttons(self):
        for widget in self.user_turn_frame.winfo_children():
            if isinstance(widget, tk.Frame):  # button_frame
                for btn in widget.winfo_children():
                    btn.config(state="disabled")

    def restart_game(self):
        self.user = Player("You")
        self.ai = AIPlayer("AI")
        self.game = HandCricketGame()
        self.innings = 1
        self.show_toss_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HandCricketUI(root)
    root.mainloop()
