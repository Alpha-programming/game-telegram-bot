import random
URL = "https://random-word-api.herokuapp.com/word?number=1"

hangman_stages = [
        """
          +---+
              |
              |
              |
              ===
        """,
        """
          +---+
          O   |
              |
              |
              ===
        """,
        """
          +---+
          O   |
          |   |
              |
              ===
        """,
        """
          +---+
          O   |
         /|   |
              |
              ===
        """,
        """
          +---+
          O   |
         /|\\  |
              |
              ===
        """,
        """
          +---+
          O   |
         /|\\  |
         /    |
              ===
        """,
        """
          +---+
          O   |
         /|\\  |
         / \\  |
              ===
        """
    ]

with open(f'database/easy_words_1M.txt', 'r', encoding='utf-8') as easy_file:
    easy_words = easy_file.read().splitlines()

with open(f'database/medium_words_1M.txt', 'r', encoding='utf-8') as medium_file:
    medium_words = medium_file.read().splitlines()

with open(f'database/hard_words_1M.txt', 'r', encoding='utf-8') as hard_file:
    hard_words = hard_file.read().splitlines()

def generate_random_word(level):
        if level == 'easy':
                return random.choice(easy_words)
        elif level == 'medium':
                return random.choice(medium_words)
        elif level == 'hard':
                return random.choice(hard_words)


