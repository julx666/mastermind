import random


class Interface:

    @staticmethod
    def is_query_duplicated():
        print("You have already used this query. Please provide a new one.")

    @staticmethod
    def get_n_from_user():
        while True:
            n = input("Enter n (the sequence length): ")
            if n.isdigit() and int(n) > 0:
                return int(n)
            else:
                print("n must be a positive!")

    @staticmethod
    def get_k_from_user():
        while True:
            k = input("Enter k (the number of colors): ")
            if k.isdigit() and int(k) > 0:
                return int(k)
            else:
                print("k must be positive!")

    def get_game_config(self):
        n = self.get_n_from_user()
        k = self.get_k_from_user()
        game_mode = self.choose_game_mode()
        hidden_seq = None

        if game_mode == "auto":
            if self.is_hidden_seq_random():  # co sie stanie kiedy uzytkownik wpisze 'yes'??
                # hidden_seq = input("Give hidden sequence: ")
                hidden_seq = self.get_seq_from_the_user(n, k)
            else:
                hidden_seq = [random.randint(1, k) for _ in range(n)]
        else:
            hidden_seq = [random.randint(1, k) for _ in range(n)]

        return n, k, game_mode, hidden_seq

    @staticmethod
    def choose_game_mode():
        game_mode = input("Which game mode are you choosing? auto or manual: ").lower()

        while True:
            if game_mode == 'auto' or game_mode == 'manual':
                return game_mode
            else:
                print("Wrong input!")
                game_mode = input("Which game mode are you choosing? auto or manual: ")

    @staticmethod
    def is_hidden_seq_random() -> bool:
        hidden_seq_random = input("Do you want to choose hidden sequence by yourself"
                                  "otherwise it is going to be generated randomly [y/n]: ").lower()

        while True:
            if hidden_seq_random == 'y' or hidden_seq_random == 'n':
                if hidden_seq_random == 'y':
                    return True
                else:
                    return False
            else:
                print("Wrong input!")
                hidden_seq_random = input("Do you want to choose hidden sequence by yourself"
                                          "otherwise it is going to be generated randomly [y/n]: ").lower()

    @staticmethod
    def get_seq_from_the_user(n, k, seq_type="hidden"):
        while True:
            seq = input(
                f"Give the {seq_type} sequence ({n} numbers in the range [1, {k}], separated by comas): ")
            seq = seq.split(",")

            # Check if all elements are digits
            if not all(ele.strip().isdigit() for ele in seq):
                print("Wrong input. All elements must be numbers.")
                continue

            # Convert to integers
            seq = [int(ele.strip()) for ele in seq]

            # Check length
            if len(seq) != n:
                print(f"Wrong input. The sequence must contain exactly {n} numbers.")
                continue

            # Check range
            if not all(1 <= ele <= k for ele in seq):
                print(f"Wrong input. All numbers must be in the range [1, {k}].")
                continue

            return seq  # Return valid sequence

    def get_hidden_seq_from_the_user(self, n, k):
        hidden_seq = self.get_seq_from_the_user(n, k, "hidden")
        return hidden_seq

    def get_query_seq_from_the_user(self, n, k):
        query_seq = self.get_seq_from_the_user(n, k, "query")
        return query_seq
