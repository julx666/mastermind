from judge import Judge
from player import AutoPlayer, ManualPlayer
from simple_interface import Interface


class Game:
    def __init__(self):
        self.player = None
        self.judge = Judge()
        self.interface = Interface()
        self.k, self.n, self.game_mode = self.interface.get_game_config(self)
        self.k = self.interface.get_k_from_user()
        self.n = self.interface.get_n_from_user()
        self.game_mode = self.interface.choose_game_mode()
        self.turns = 0
        print(self.game_mode)
        self.choose_player()
        self.is_hidden_seq_random = self.interface.is_hidden_seq_random()
        self.hidden_seq = self.interface.get_hidden_seq_from_the_user(self.k)
        self.get_seq_from_the_user = self.interface.get_seq_from_the_user(self.k, seq_type="hidden")
    def choose_player(self):
        if self.game_mode == 'auto':
            self.player = AutoPlayer()
        else:
            self.player = ManualPlayer()

    def set_seq_type(self):
        if self.get_seq_from_the_user:
            pass

    def play(self):
        print(f"Turn number: {self.turns}") #wspólne
        print(f"hidden: {self.hidden_seq}") #test
        query = self.player.get_query(self.k) #wspólne
        print(f"query: {query}") #wspólne
        correct_position_and_color, correct_color = self.judge.check(self.k, self.hidden_seq, query) #wspolne
        if correct_position_and_color == self.k: #osobna metoda
            print("win")
        elif self.n == self.turns:
            print("lose")
        else:
            print(f"correct_position_and_color: {correct_position_and_color}, correct_color: {correct_color}")
            self.turns += 1
            self.play()


g = Game()
g.play()
