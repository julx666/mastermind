from collections import Counter


class Judge:
    @staticmethod
    def check(k, hidden, guess):
        """Check a guess against the hidden code in a Mastermind-like game.

        Args:
            k: Maximum color value (1 to k)
            hidden: List of numbers representing the hidden code
            guess: List of numbers representing the guess

        Returns:
            Tuple of (exact matches, color matches)
        """
        # Basic validation
        if len(hidden) != len(guess):
            raise ValueError("Sequences must be the same length")

        if any(x < 1 or x > k for x in hidden + guess):
            raise ValueError(f"All numbers must be between 1 and {k}")

        # Count exact matches (right color, right position)
        correct_position_and_color = sum(h == q for h, q in zip(hidden, guess))

        # Get unmatched pegs and count color matches
        hidden_remaining = [h for h, q in zip(hidden, guess) if h != q]
        guess_remaining = [q for h, q in zip(hidden, guess) if h != q]

        hidden_remaining = set(hidden_remaining)
        guess_remaining = set(guess_remaining)

        correct_color = 0
        for color in guess_remaining:
            if color in hidden_remaining:
                correct_color += 1

        return correct_position_and_color, correct_color

# Example usage
# hidden = [2,3,1,2]
# query = [2,3,1,1]
# judge = Judge()
# print(judge.check(4, hidden, query))
