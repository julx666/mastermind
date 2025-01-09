class Interface:

    @staticmethod
    def get_k_from_user():
        while True:
            k = int(input("Enter k (the length of sequences): "))
            if k > 0:
                return k
            else:
                print("K must be positive!")

    @staticmethod
    def get_n_from_user():
        while True:
            n = int(input("Enter n (the number of attempts): "))
            if n > 0:
                return n
            else:
                print("n must be a positive!")

    def get_game_config(self):
        k = self.get_k_from_user()
        n = self.get_n_from_user()
        game_mode = self.choose_game_mode()

        if game_mode == "auto":
            random_generated = input(("Do you want choose hidden sequence? otherwise it will be generated [y/n]: "))
            if random_generated == "y":
                hidden_seq = input("Give hidden sequence: ")
                return hidden_seq

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
    def get_seq_from_the_user(k, seq_type="hidden"):
        while True:
            seq = input(
                f"Give the {seq_type} sequence ({k} numbers in the range [1, {k}], separated by commas): ")
            seq = seq.split(",")

            # Check if all elements are digits
            if not all(ele.strip().isdigit() for ele in seq):
                print("Wrong input. All elements must be numbers.")
                continue

            # Convert to integers
            seq = [int(ele.strip()) for ele in seq]

            # Check length
            if len(seq) != k:
                print(f"Wrong input. The sequence must contain exactly {k} numbers.")
                continue

            # Check range
            if not all(1 <= ele <= k for ele in seq):
                print(f"Wrong input. All numbers must be in the range [1, {k}].")
                continue

            return seq  # Return valid sequence

    def get_hidden_seq_from_the_user(self, k):
        hidden_seq = self.get_seq_from_the_user(k, "hidden")
        return hidden_seq

    def get_query_seq_from_the_user(self, k):
        query_seq = self.get_seq_from_the_user(k, "query")
        return query_seq
