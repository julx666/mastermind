from judge import Judge
from player import AutoPlayer, ManualPlayer
from simple_interface import Interface


class Game:
    """
    Represents the main game logic, managing turns, player interactions, and game status.
    """

    def __init__(self):
        self.player = None
        self.judge = Judge()
        self.interface = Interface()
        self.n, self.k, self.game_mode, self.hidden_seq = (
            self.interface.get_game_config()
        )
        self.max_turns = 10  # Adjust maximum turns based on sequence length
        self.turns = 0  # Initialize turn counter
        self.choose_player()

    def choose_player(self):
        """
        Chooses the type of player based on the game mode.
        """
        if self.game_mode == "auto":
            self.player = AutoPlayer()
        else:
            self.player = ManualPlayer()

    def check_game_status(self, correct_position_and_color, correct_color):
        """
        Checks the current game status to determine if the game should continue.

        Args:
            correct_position_and_color (int): Number of exact matches.
            correct_color (int): Number of color matches (excluding position).

        Returns:
            bool: False if the game is won or lost, True otherwise.
        """
        if correct_position_and_color == len(self.hidden_seq):
            print(f"\nYou win!!! Found the sequence in {self.turns} turns.")
            return False
        elif self.turns >= self.max_turns:
            print(f"\nGame Over! Maximum turns ({self.max_turns}) reached.")
            print(f"The hidden sequence was: {self.hidden_seq}")
            return False
        else:
            print(f"Turn {self.turns}/{self.max_turns}")
            print(f"Correct position and color: {correct_position_and_color}")
            print(f"Correct color but wrong position: {correct_color}\n")
            return True

    def play(self):
        """
        Runs the main game loop.
        """
        print(
            f"\nGame started! Try to guess a sequence of length {self.n} using numbers 1 to {self.k}"
        )
        print(f"You have {self.max_turns} turns to guess correctly.\n")
        print("Press Ctrl+D at any time to end the game early.\n")

        while True:
            try:
                # Get query from the player
                query = self.player.get_query(self.n, self.k)
                print(f"Your guess: {query}")

                self.turns += 1

                # Check the query against the hidden sequence
                correct_position_and_color, correct_color = self.judge.check(
                    self.k, self.hidden_seq, query
                )

                # Check game status and break the loop if the game is over
                if not self.check_game_status(
                    correct_position_and_color, correct_color
                ):
                    break

            except EOFError:
                print("\nGame terminated. Goodbye!")
                print(f"The hidden sequence was: {self.hidden_seq}")
                break


g = Game()
g.play()
