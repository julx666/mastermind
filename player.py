import random


class AutoPlayer:
    def __init__(self):
        self.used_queries = []

    def get_query(self, k):
        query = []
        for _ in range(k):
            # query.append(1)
            query.append(random.randint(1, k))
        if query not in self.used_queries:

            self.used_queries.append(query)
            return query
        else:
            self.get_query(k)


# o = AutoPlayer()
# for _ in range(5):
#     print("\n")
#     print(o.get_query(4))
