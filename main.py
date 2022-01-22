"""Wordle Solver"""

from random import choice

word_list_path = "wordle-answers-alphabetical.txt"


def solve(word_list: list, secret_word: str):
    if not isinstance(secret_word, str) or len(secret_word) != 5:
        raise ValueError("Secret word is not a 5 character string.")

    guesses = 1
    while True:
        # Find word that hints at the max number of words
        guess = choose_word(word_list)
        print("Guess number {} is '{}'".format(guesses, guess.upper()))

        # Make guess
        print("Guessing from {} words.".format(len(word_list)))
        guess_match = wordle(guess, secret_word)

        if guess_match == [2, 2, 2, 2, 2]:
            print("Done")
            return

        elif -1 in guess_match:
            raise ValueError("Something went wrong with the Wordle check. -1 in result")

        # Trim invalid words from list.
        # TODO - Add alternate coverage methods.
        for i, letter in enumerate(guess):
            if guess_match[i] == 0:
                word_list = [word for word in word_list if letter not in word]
            elif guess_match[i] == 1:
                word_list = [word for word in word_list if letter in word and word[i] is not letter]
            else:
                word_list = [word for word in word_list if word[i] is letter]

        # run solve() again with new list
        guesses += 1


def get_word_list(path: str) -> list:
    words = []

    with open(path) as f:
        words = f.readlines()

    return [w.strip("\n\r") for w in words]


def wordle(guess: str, secret_word: str):
    """Run Wordle guess.

    args:
        guess: str - 5 letter guess
        secret_word: str - 5 letter solution

    returns:
        list: 0, 1, or 2 in each field.
            0: not in word
            1: in word, not in position
            2: in word and position

    errors:
        ValueError: Either word is not a string or 5 letters
    """
    if (
        not isinstance(guess, str)
        or not isinstance(secret_word, str)
        or len(guess) != 5
        or len(secret_word) != 5
    ):
        raise ValueError("Guess or word is not a 5 letter string.")

    output = [-1, -1, -1, -1, -1]

    for i, letter in enumerate(guess):
        if letter not in secret_word:
            output[i] = 0
        elif letter in secret_word and secret_word[i] is not letter:
            output[i] = 1
        else:
            output[i] = 2

    return output


def choose_word(word_list: list, mode=0) -> str:
    """Chooses word based on desired method

    args:
        word_list: list - list of words to choose from
        mode: int - choice method
            0: random choice
            1: max coverage choice

    returns:
        str: best word to use
    """
    if mode == 0:
        return choice(word_list)
    elif mode == 1:
        return max_coverage_word(word_list)


def max_coverage_word(word_list: list) -> str:
    """Chooses word that covers the most words in the list

    cache the answers to be use between uses.
    """

    pass


if __name__ == "__main__":
    word_list = get_word_list(word_list_path)

    word = choice(word_list)
    print("Word is '{}'.".format(word.upper()))

    solve(word_list, word)
