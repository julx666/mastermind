import random


class Interface:
    @staticmethod
    def is_query_duplicated():
        """
        Prints a message indicating that the query has already been used and prompts the user to provide a new one.

        This function does not take any parameters and does not return any values.
        """
        print("You have already used this query. Please provide a new one.")

    @staticmethod
    def get_n_from_user():
        """
        Prompt the user to enter a positive integer value for 'n', which represents the sequence length.
        
        The function will repeatedly ask the user for input until a valid positive integer is provided.
        
        Returns:
            int: A positive integer entered by the user.
        """
        while True:
            n = input("Enter n (the sequence length): ")
            if n.isdigit() and int(n) > 0:
                return int(n)
            else:
                print("n must be a positive!")

    @staticmethod
    def get_k_from_user():
        """
        Prompt the user to enter a positive integer value for k (the number of colors).

        This method repeatedly asks the user to input a value for k until a valid positive integer is provided.
        If the input is not a positive integer, it will prompt the user again with an error message.

        Returns:
            int: A positive integer representing the number of colors.
        """
        while True:
            k = input("Enter k (the number of colors): ")
            if k.isdigit() and int(k) > 0:
                return int(k)
            else:
                print("k must be positive!")

    def get_game_config(self):
        """
        Configures the game settings based on user input and game mode.

        This method interacts with the user to determine the values for `n` (length of the sequence) 
        and `k` (range of possible values in the sequence). It also allows the user to choose the 
        game mode, which can be either "auto" or another mode. Depending on the game mode and 
        whether the hidden sequence should be random, it generates the hidden sequence accordingly.

        Returns:
            tuple: A tuple containing:
                - n (int): Length of the sequence.
                - k (int): Range of possible values in the sequence.
                - game_mode (str): The chosen game mode.
                - hidden_seq (list): The generated hidden sequence.
        """
        n = self.get_n_from_user()
        k = self.get_k_from_user()
        game_mode = self.choose_game_mode()
        hidden_seq = None

        if game_mode == "auto":
            if self.is_hidden_seq_random():
                hidden_seq = self.get_seq_from_the_user(n, k)
            else:
                hidden_seq = [random.randint(1, k) for _ in range(n)]
        else:
            hidden_seq = [random.randint(1, k) for _ in range(n)]

        return n, k, game_mode, hidden_seq

    @staticmethod
    def choose_game_mode():
        """
        Prompts the user to choose a game mode between 'auto' and 'manual'.

        The function will repeatedly ask the user for input until a valid game mode is entered.
        If the input is not 'auto' or 'manual', it will print an error message and prompt again.

        Returns:
            str: The chosen game mode, either 'auto' or 'manual'.
        """
        game_mode = input("Which game mode are you choosing? auto or manual: ").lower()

        while True:
            if game_mode == "auto" or game_mode == "manual":
                return game_mode
            else:
                print("Wrong input!")
                game_mode = input("Which game mode are you choosing? auto or manual: ")

    @staticmethod
    def is_hidden_seq_random() -> bool:
        """
        Asks the user if they want to choose the hidden sequence themselves or have it generated randomly.

        Returns:
            bool: True if the user wants to choose the hidden sequence, False if it should be generated randomly.
        """
        hidden_seq_random = input(
            "Do you want to choose hidden sequence by yourself"
            "otherwise it is going to be generated randomly [y/n]: "
        ).lower()

        while True:
            if hidden_seq_random == "y" or hidden_seq_random == "n":
                if hidden_seq_random == "y":
                    return True
                else:
                    return False
            else:
                print("Wrong input!")
                hidden_seq_random = input(
                    "Do you want to choose hidden sequence by yourself"
                    "otherwise it is going to be generated randomly [y/n]: "
                ).lower()

    @staticmethod
    def get_seq_from_the_user(n, k, seq_type="hidden"):
        """
        Prompts the user to input a sequence of numbers and validates the input.

        Args:
            n (int): The expected length of the sequence.
            k (int): The maximum value for the numbers in the sequence.
            seq_type (str, optional): A descriptor for the type of sequence being requested. Defaults to "hidden".

        Returns:
            list: A list of integers representing the validated sequence.

        The function repeatedly prompts the user to input a sequence of numbers separated by commas.
        It performs the following validations:
        - All elements must be numbers.
        - The sequence must contain exactly `n` numbers.
        - All numbers must be in the range [1, `k`].

        If the input is invalid, the function prints an error message and prompts the user again.
        """
        while True:
            seq = input(
                f"Give the {seq_type} sequence ({n} numbers in the range [1, {k}], separated by comas): "
            )
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
        """
        Prompts the user to input a hidden sequence.

        Args:
            n (int): The length of the sequence.
            k (int): The range of possible values in the sequence.

        Returns:
            list: The hidden sequence entered by the user.
        """
        hidden_seq = self.get_seq_from_the_user(n, k, "hidden")
        return hidden_seq

    def get_query_seq_from_the_user(self, n, k):
        """
        Prompts the user to input a sequence of length `n` with elements in the range [0, k-1].

        Args:
            n (int): The length of the sequence to be input by the user.
            k (int): The range of values for each element in the sequence (0 to k-1).

        Returns:
            list: A list containing the sequence of integers input by the user.
        """
        query_seq = self.get_seq_from_the_user(n, k, "query")
        return query_seq
