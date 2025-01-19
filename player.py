import random
from simple_interface import Interface


class AutoPlayer:
    """
    Represents an automated player that generates unique random queries.
    """
    def __init__(self):
        self.used_queries = []
        self.interface = Interface()

    def get_query(self, n, k):
        """
        Generates a random query of length n with values in the range [1, k].
        Ensures that the query is unique.

        Args:
            n (int): Length of the query sequence.
            k (int): Number of colors.

        Returns:
            list: A unique query sequence.

        Raises:
            RuntimeError: If a unique query cannot be generated within the maximum attempts.
        """
        # Calculate maximum possible attempts to avoid infinite recursion
        max_possibilities = k ** n
        attempts = 0
        max_attempts = min(max_possibilities, 100)  # Limit attempts to avoid excessive recursion

        while attempts < max_attempts:
            query = [random.randint(1, k) for _ in range(n)]
            if query in self.used_queries:
                self.interface.is_query_duplicated()
            else:
                self.used_queries.append(query)
                return query
            attempts += 1

        # If we can't find a unique query after max attempts
        raise RuntimeError("Unable to generate unique query after maximum attempts")


class ManualPlayer:
    """
    Represents a manual player that provides queries via user input.
    """
    def __init__(self):
        self.used_queries = []
        self.interface = Interface()

    def get_query(self, n, k):
        """
        Asks the user to provide a query sequence.
        Ensures that the query is unique.

        Args:
            n (int): Length of the query sequence.
            k (int): Number of colors.

        Returns:
            list: A unique query sequence.
        """
        while True:
            query = self.interface.get_query_seq_from_the_user(n, k)
            if query in self.used_queries:
                self.interface.is_query_duplicated()
            else:
                self.used_queries.append(query)
                return query


# o = AutoPlayer()
# for _ in range(5)
#     print("\n")
#     print(o.get_query(4))
