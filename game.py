from judge import Judge
from player import AutoPlayer
from simple_interface import Interface


class Game:
    def __init__(self):
        self.judge = Judge()
        self.player = AutoPlayer()
        self.interface = Interface()
        # self.interface =
        self.k = 4
        self.hidden = [1, 4, 3, 2]
        self.n = 10
        self.turns = 0
        self.game_mode = self.interface.choose_game_mode()
        print(self.game_mode)

    def play(self):
        print(f"Turn number: {self.turns}")
        print(f"hidden: {self.hidden}")
        query = self.player.get_query(self.k)
        print(f"query: {query}")
        correct_position_and_color, correct_color = self.judge.check(self.k, self.hidden, query)
        if correct_position_and_color == self.k:
            print("win")
        elif self.n == self.turns:
            print("lose")
        else:
            print(f"correct_position_and_color: {correct_position_and_color}, correct_color: {correct_color}")
            self.turns += 1
            self.play()


g = Game()
g.play()
