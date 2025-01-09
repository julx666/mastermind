import random
from simple_interface import Interface


class AutoPlayer:
    def __init__(self):
        self.used_queries = []

    def get_query(self, k):
        # Calculate maximum possible attempts to avoid infinite recursion
        max_possibilities = k ** k
        attempts = 0
        max_attempts = min(max_possibilities, 100)  # Limit attempts to avoid excessive recursion

        while attempts < max_attempts:
            query = [random.randint(1, k) for _ in range(k)]
            if query not in self.used_queries:
                self.used_queries.append(query)
                return query
            attempts += 1

        # If we can't find a unique query after max attempts
        raise RuntimeError("Unable to generate unique query after maximum attempts")


class ManualPlayer:
    def __init__(self, interface):
        self.used_queries = []
        self.interface = interface

    def get_query(self, k):
        # while True:
        #     query = self.interface.get_query_seq_from_the_user(k)
        #     if query not in self.used_queries:
        #         self.used_queries.append(query)
        #         return query
        return self.interface.get_query_seq_from_the_user(k)


# o = AutoPlayer()
# for _ in range(5)
#     print("\n")
#     print(o.get_query(4))
