# Evaluates guessed letters against the target word.
from collections import Counter


def evaluate_guess(
    target: str,
    guess: str
):

    result = ["GREY"] * 5

    remaining = Counter()

    # First pass
    # Find exact matches
    for i in range(5):

        if guess[i] == target[i]:

            result[i] = "GREEN"

        else:

            remaining[target[i]] += 1

    # Second pass
    # Find correct letters in wrong positions
    for i in range(5):

        if result[i] == "GREEN":
            continue

        if remaining[guess[i]] > 0:

            result[i] = "ORANGE"

            remaining[guess[i]] -= 1

    return result