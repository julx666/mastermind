class Judge:
    """
    The Judge class provides a mechanism to compare a hidden sequence with a query sequence
    and evaluate how many elements match in position and color, and how many match in color only.
    """
    @staticmethod
    def check(k, hidden, query):
        """
        Compares a hidden sequence with a query sequence to determine:
        1. The number of exact matches (correct position and color).
        2. The number of partial matches (correct color, wrong position).

        Args:
            k (int): The number of colors allowed in the sequences.
            hidden (list): The hidden sequence to be guessed.
            query (list): The query sequence provided by the player.

        Returns:
            tuple containing:
                - correct_position_and_color (int): Count of exact matches.
                - correct_color (int): Count of correct colors in incorrect positions.

        Raises:
            ValueError: If the sequences have different lengths or contain invalid colors.
        """

        # Basic validation
        if len(hidden) != len(query):
            raise ValueError("Sequences must be the same length")

        if any(x < 1 or x > k for x in hidden + query):
            raise ValueError(f"All numbers must be between 1 and {k}")

        # Count exact matches (right color, right position)
        correct_position_and_color = sum(h == q for h, q in zip(hidden, query))

        # Get unmatched elements
        hidden_remaining = [h for h, q in zip(hidden, query) if h != q]
        query_remaining = [q for h, q in zip(hidden, query) if h != q]

        hidden_remaining = set(hidden_remaining)
        query_remaining = set(query_remaining)

        # Count partial matches (right color, wrong position)
        correct_color = 0
        for color in query_remaining:
            if color in hidden_remaining:
                correct_color += 1

        return correct_position_and_color, correct_color

# Example usage
# hidden = [2,3,1,2]
# query = [2,3,1,1]
# judge = Judge()
# print(judge.check(4, hidden, query))
