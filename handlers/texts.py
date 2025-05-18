from aiogram import Router,F
from aiogram.types import Message
from keyboards.inline import choose_action,choose_action_hangman, choose_action_rps,choose_action_quiz,choose_action_number,choose_action_scramble_word

router = Router()
@router.message(F.text == 'BlackJack')
async def blackjack(message: Message):
    await message.reply(text="If you want to start a BlackJack game press 'Start' button\nIf you want to get familiarized with the game press 'Info' button",reply_markup=choose_action())

@router.message(F.text == 'Hangman')
async def hangman(message: Message):
    await message.reply(text="If you want to start a Hangman game press 'Start' button\nIf you want to get familiarized with the game press 'Info' button",reply_markup=choose_action_hangman())

@router.message(F.text == 'Rock Paper and Scissors')
async def hangman(message: Message):
    await message.reply(text="If you want to start a Rock Paper and Scissor game press 'Start' button\nIf you want to get familiarized with the game press 'Info' button",reply_markup=choose_action_rps())

@router.message(F.text == 'Quizzler')
async def hangman(message: Message):
    await message.reply(text="If you want to start a Quiz game press 'Start' button\nIf you want to get familiarized with the game press 'Info' button",reply_markup=choose_action_quiz())

@router.message(F.text == 'Guess a number')
async def hangman(message: Message):
    await message.reply(text="If you want to start a Guess a number game press 'Start' button\nIf you want to get familiarized with the game press 'Info' button",reply_markup=choose_action_number())

@router.message(F.text == 'Scramble a Word')
async def hangman(message: Message):
    await message.reply(text="If you want to start a Scramble a Word game press 'Start' button\nIf you want to get familiarized with the game press 'Info' button",reply_markup=choose_action_scramble_word())