from aiogram.fsm.state import State, StatesGroup

class HangmanState(StatesGroup):
    secret_word = State()
    guessed_word = State()
    wrong_guesses = State()
    attempts = State()

class QuizState(StatesGroup):
    amount = State()

class GuessNumState(StatesGroup):
    number = State()

class WordScrambleState(StatesGroup):
    word = State()