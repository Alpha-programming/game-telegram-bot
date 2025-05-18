from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from database.quizzler import get_categories
import math

def choose_action():
    kb = InlineKeyboardBuilder()
    kb.button(text='Start',callback_data='start')
    kb.button(text='Info',callback_data='info_blackjack')
    kb.adjust(2)

    return kb.as_markup()

def continue_or_finish():
    kb = InlineKeyboardBuilder()
    kb.button(text='Get extra card', callback_data=f'extra')
    kb.button(text='Finish', callback_data='finish')

    kb.adjust(2)
    return kb.as_markup()

def choose_action_hangman():
    kb = InlineKeyboardBuilder()
    kb.button(text='Start', callback_data='begin')
    kb.button(text='Info', callback_data='hangman_info')

    kb.adjust(2)
    return kb.as_markup()

def choose_difficulty_hangman():
    kb = InlineKeyboardBuilder()
    kb.button(text='Easy', callback_data='easy')
    kb.button(text='Medium', callback_data='medium')
    kb.button(text='Hard', callback_data='hard')

    kb.adjust(3)
    return kb.as_markup()

def choose_action_rps():
    kb = InlineKeyboardBuilder()
    kb.button(text='Start', callback_data='go')
    kb.button(text='Info', callback_data='rps_info')

    kb.adjust(2)
    return kb.as_markup()

def choose_rock_paper_scissor():
    kb = InlineKeyboardBuilder()
    kb.button(text='Rock', callback_data='rock')
    kb.button(text='Paper', callback_data='paper')
    kb.button(text='Scissors', callback_data='scissors')

    kb.adjust(3)
    return kb.as_markup()

def choose_action_quiz():
    kb = InlineKeyboardBuilder()
    kb.button(text='Start', callback_data='initiate')
    kb.button(text='Info', callback_data='data_quiz')

    kb.adjust(2)
    return kb.as_markup()

def choose_categories_quiz(start=0, limit=9, current_page=1):
    kb = InlineKeyboardBuilder()
    total_pages = math.ceil(len(get_categories()) / 9)

    for category in get_categories()[start:limit]:

        id_cat = category['id']
        name_cat = category['name']
        kb.button(text=name_cat, callback_data=f'category+{name_cat}+{id_cat}')

    kb.adjust(3)
    pagination_buttons = []
    if current_page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(text='⏪ Previous page)',
                                 callback_data=f'prev_page:{start}:{limit}:{current_page}')
        )

    pagination_buttons.append(InlineKeyboardButton(text=f'{current_page}/{total_pages}', callback_data='current'))

    if current_page < total_pages:
        pagination_buttons.append(
            InlineKeyboardButton(text='Next page ⏩ ',
                                 callback_data=f'next_page:{start}:{limit}:{current_page}:{total_pages}')
        )

    if pagination_buttons:
        kb.row(*pagination_buttons)

    return kb.as_markup()

def choose_difficulty_quiz():
    kb = InlineKeyboardBuilder()
    kb.button(text='Easy', callback_data=f'level:easy')
    kb.button(text='Medium', callback_data=f'level:medium')
    kb.button(text='Hard', callback_data=f'level:hard')

    kb.adjust(3)
    return kb.as_markup()

def choose_type_quiz():
    kb = InlineKeyboardBuilder()
    kb.button(text='Multiple Choice',callback_data=f'type:multiple')
    kb.button(text='True/False',callback_data=f'type:boolean')

    kb.adjust(2)
    return kb.as_markup()

def ready_quiz():
    kb = InlineKeyboardBuilder()
    kb.button(text='Ready', callback_data='ready')

    return kb.as_markup()

def answer_questions(answers,current,total):
    kb = InlineKeyboardBuilder()
    for answer in answers:
        data = f"answer:{answer}:{current}:{total}"
        if len(data) <= 64:
            kb.button(text=answer, callback_data=data)
        else:
            print(f"Warning: Data for answer '{answer}' is too long.")
    kb.adjust(1)
    return kb.as_markup()


def choose_action_number():
    kb = InlineKeyboardBuilder()
    kb.button(text='Start',callback_data='launch')
    kb.button(text='Info',callback_data='number_info')
    kb.adjust(2)

    return kb.as_markup()

def choose_action_scramble_word():
    kb = InlineKeyboardBuilder()
    kb.button(text='Start',callback_data='commence')
    kb.button(text='Info',callback_data='scramble_info')
    kb.adjust(2)

    return kb.as_markup()

def choose_level_scramble():
    kb = InlineKeyboardBuilder()
    kb.button(text='Easy', callback_data=f'difficulty:easy')
    kb.button(text='Medium', callback_data=f'difficulty:medium')
    kb.button(text='Hard', callback_data=f'difficulty:hard')

    kb.adjust(3)
    return kb.as_markup()