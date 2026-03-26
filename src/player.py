import random

class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.score = 0
        self.is_out = False

    def reset(self):
        self.score = 0
        self.is_out = False


    def add_score(self, runs):
        self.score += runs

    def get_score(self):
        return self.score


class AIPlayer(Player):
    def __init__(self, name="AI"):
        super().__init__(name)

    def get_input(self):
        return random.randint(1, 6)
