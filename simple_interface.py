class Interface:
    @staticmethod
    def choose_game_mode():
        game_mode = input("Which game mode are you choosing? auto or manual: ")

        while True:
            if game_mode == 'auto' or game_mode == 'manual':
                return game_mode
            else:
                print("Wrong input!")
                game_mode = input("Which game mode are you choosing? auto or manual: ")

    @staticmethod
    def is_hidden_seq_random():
        hidden_seq_random = input("Do you want to choose hidden sequence by yourself"
                                  "otherwise it is going to be generated randomly [y/n]: ")

        while True:
            if hidden_seq_random == 'y' or hidden_seq_random == 'n':
                return hidden_seq_random
            else:
                print("Wrong input!")
                hidden_seq_random = input("Do you want to choose hidden sequence by yourself"
                                          "otherwise it is going to be generated randomly [y/n]: ")

    @staticmethod
    def get_hidden_seq_from_the_user(k):
        while True:
            hidden_seq = input(
                f"Give the hidden sequence ({k} numbers in the range [1, {k}], separated by commas): ")
            hidden_seq = hidden_seq.split(",")

            # Check if all elements are digits
            if not all(ele.strip().isdigit() for ele in hidden_seq):
                print("Wrong input. All elements must be numbers.")
                continue

            # Convert to integers
            hidden_seq = [int(ele.strip()) for ele in hidden_seq]

            # Check length
            if len(hidden_seq) != k:
                print(f"Wrong input. The sequence must contain exactly {k} numbers.")
                continue

            # Check range
            if not all(1 <= ele <= k for ele in hidden_seq):
                print(f"Wrong input. All numbers must be in the range [1, {k}].")
                continue

            return hidden_seq  # Return valid sequence
