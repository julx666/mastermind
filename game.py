from judge import Judge
from player import AutoPlayer, ManualPlayer
from simple_interface import Interface


class Game:
    def __init__(self):
        self.player = None
        self.judge = Judge()
        self.interface = Interface()
        self.k = 4
        self.n = 10
        self.turns = 0
        self.game_mode = self.interface.choose_game_mode()
        print(self.game_mode)
        self.choose_player()
        self.hidden_seq_random = self.interface.is_hidden_seq_random()
        self.hidden_seq = self.interface.get_hidden_seq_from_the_user(self.k)

    def choose_player(self):
        if self.game_mode == 'auto':
            self.player = AutoPlayer()
        else:
            self.player = ManualPlayer()

    def play(self):
        print(f"Turn number: {self.turns}")
        print(f"hidden: {self.hidden_seq}")
        query = self.player.get_query(self.k)
        print(f"query: {query}")
        correct_position_and_color, correct_color = self.judge.check(self.k, self.hidden_seq, query)
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
