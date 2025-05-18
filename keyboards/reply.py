from aiogram.utils.keyboard import ReplyKeyboardBuilder

def start_kb():
    kb = ReplyKeyboardBuilder()

    kb.button(text='BlackJack')
    kb.button(text='Hangman')
    kb.button(text='Rock Paper and Scissors')
    kb.button(text='Quizzler')
    kb.button(text='Guess a number')
    kb.button(text='Scramble a Word')

    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)