from player import Player, AIPlayer
import random

class HandCricketGame:
    def __init__(self):
        self.user = Player("You")
        self.ai = AIPlayer("AI")
        self.first_innings_score = 0
        self.target = 0
        self.first_batter = None
        self.first_score = 0
        self.user_score_final = 0
        self.ai_score_final = 0

    def toss(self):
        print("\n--- TOSS TIME ---")
        choice = input("Choose 'odd' or 'even': ").lower()
        try:
            user_number = int(input("Enter your toss number (1–6): "))
        except ValueError:
            print("Invalid number. Try again.")
            return self.toss()

        if user_number < 1 or user_number > 6:
            print("Please enter a number between 1 and 6.")
            return self.toss()

        ai_number = random.randint(1, 6)
        total = user_number + ai_number
        print(f"AI chose: {ai_number}, Total: {total}")

        if (total % 2 == 0 and choice == 'even') or (total % 2 != 0 and choice == 'odd'):
            print("You won the toss!")
            while True:
                decision = input("Choose 'bat' or 'bowl': ").strip().lower()
                if decision in ['bat', 'bowl']:
                    break
                print("❌ Invalid input. Please type 'bat' or 'bowl'.")

            if decision == 'bat':
                self.first_innings(self.user, self.ai)
                self.second_innings(self.ai, self.user)
            else:
                self.first_innings(self.ai, self.user)
                self.second_innings(self.user, self.ai)
        else:
            print("AI won the toss!")
            decision = random.choice(['bat', 'bowl'])
            print(f"AI chooses to {decision}")
            if decision == 'bat':
                self.first_innings(self.ai, self.user)
                self.second_innings(self.user, self.ai)
            else:
                self.first_innings(self.user, self.ai)
                self.second_innings(self.ai, self.user)

    def first_innings(self, striker, defender):
        print(f"\n--- FIRST INNINGS: {striker.name} is batting ---")
        while not striker.is_out:
            bat = striker.get_input()
            bowl = defender.get_input()
            print(f"{defender.name} bowled: {bowl}")
            print(f"{striker.name} played: {bat}")

            if bat == bowl:
                striker.is_out = True
                print(f"{striker.name} is OUT!")
            else:
                striker.add_score(bat)
                print(f"{striker.name} score: {striker.get_score()}")

        self.first_innings_score = striker.get_score()
        self.target = self.first_innings_score + 1
        self.first_batter = striker.name
        self.first_score = striker.get_score()

        print(f"\nEnd of innings. {striker.name} scored: {self.first_innings_score}")
        print(f"Target for {defender.name}: {self.target}")

        striker.reset()

    def second_innings(self, striker, defender):
        print(f"\n--- SECOND INNINGS: {striker.name} is batting ---")
        while not striker.is_out:
            bat = striker.get_input()
            bowl = defender.get_input()
            print(f"{defender.name} bowled: {bowl}")
            print(f"{striker.name} played: {bat}")

            if bat == bowl:
                striker.is_out = True
                print(f"{striker.name} is OUT!")
                break
            else:
                striker.add_score(bat)
                print(f"{striker.name} score: {striker.get_score()}")

            if striker.get_score() >= self.target:
                break

        if striker == self.user:
            self.user_score_final = striker.get_score()
            self.ai_score_final = self.first_score
        else:
            self.ai_score_final = striker.get_score()
            self.user_score_final = self.first_score

        self.show_result()

        self.user.reset()
        self.ai.reset()

    def show_result(self):
        print("\n--- MATCH RESULT ---")
        print(f"You: {self.user_score_final}")
        print(f"AI : {self.ai_score_final}")

        if self.user_score_final > self.ai_score_final:
            print("🏆 You WIN! 🎉")
        elif self.user_score_final < self.ai_score_final:
            print("😞 You LOSE!")
        else:
            print("🤝 It's a TIE!")
