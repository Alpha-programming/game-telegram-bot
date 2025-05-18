from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery,Message
from aiogram import Router,F
import random
from database.blackjack import deal_card,compare_cards,calculate_hand_value
from keyboards.inline import (continue_or_finish,choose_action,choose_difficulty_hangman,choose_action_hangman,
                              choose_rock_paper_scissor,choose_action_rps,choose_categories_quiz,choose_difficulty_quiz,
                              choose_type_quiz,answer_questions,ready_quiz,choose_action_quiz,choose_action_number,choose_action_scramble_word,choose_level_scramble)
from database.database import users_repo,blackjack_repo,quiz_repo
from datetime import datetime
from database.hangman import generate_random_word,hangman_stages
from misc.state import HangmanState, QuizState,GuessNumState,WordScrambleState
from database.rps import check_rps
from database.quizzler import get_categories,request_questions
from html import unescape
import random

router = Router()
SCORE = 0
# BlackJack game
@router.callback_query(F.data.startswith('start'))
async def blackjack(call: CallbackQuery):
    user_hand = []
    user_hand_values = []
    print(call.from_user.id)

    for _ in range(2):
        card, card_value = deal_card()
        user_hand.append(card)
        user_hand_values.append(card_value)
    user_score = calculate_hand_value(user_hand_values)

    computer_hand = []
    computer_hand_value = []
    for _ in range(2):
        card, card_value = deal_card()
        computer_hand.append(card)
        computer_hand_value.append(card_value)

    computer_score = calculate_hand_value(computer_hand_value)
    while calculate_hand_value(computer_hand_value) < 17:
        card, card_value = deal_card()

        computer_hand.append(card)
        computer_hand_value.append(card_value)


    user_id = users_repo.get_user(chat_id=call.from_user.id)
    blackjack_repo.delete_cards(user_id=user_id[0])
    blackjack_repo.add_cards(user_cards=' '.join(user_hand),
                             user_score=' '.join(map(str, user_hand_values)),
                             comp_cards=' '.join(computer_hand),
                             comp_score=' '.join(map(str,computer_hand_value)),
                             user_id=user_id[0]
                             )

    await call.message.edit_text(text=f"Your cards:{user_hand} Score:{user_score}\nDealer's first card:{computer_hand[0]}",
                                 reply_markup=continue_or_finish())

@router.callback_query(F.data.startswith('extra'))
async def get_extra_card(call: CallbackQuery):
    user_id = users_repo.get_user(chat_id=call.from_user.id)
    data = blackjack_repo.get_cards(user_id=user_id[0])

    user_cards = data[0].split(' ')
    user_score_list = list(map(int, data[1].split(' ')))
    comp_cards = data[2].split(' ')
    comp_score_list = list(map(int, data[3].split(' ')))


    for _ in range(1):
        card, card_value = deal_card()

        user_cards.append(card)
        user_score_list.append(card_value)


    comp_score = calculate_hand_value(comp_score_list)
    user_score = calculate_hand_value(user_score_list)

    blackjack_repo.delete_cards(user_id=user_id[0])
    blackjack_repo.add_cards(user_cards=' '.join(user_cards),
                             user_score=' '.join(map(str, user_score_list)),
                             comp_cards=' '.join(comp_cards),
                             comp_score=' '.join(map(str, comp_score_list)),
                             user_id=user_id[0]
                             )

    await call.message.edit_text(text=f"Your cards: {user_cards} Score: {user_score}\nDealer's cards: {comp_cards[0]}",reply_markup=continue_or_finish())

@router.callback_query(F.data.startswith('finish'))
async def finish_game(call: CallbackQuery):
    user_id = users_repo.get_user(chat_id=call.from_user.id)
    data = blackjack_repo.get_cards(user_id=user_id[0])

    user_cards = data[0].split(' ')
    user_score_list = list(map(int, data[1].split(' ')))
    comp_cards = data[2].split(' ')
    comp_score_list = list(map(int, data[3].split(' ')))

    user_score = calculate_hand_value(user_score_list)
    comp_score = calculate_hand_value(comp_score_list)
    await call.message.answer(text=f"Your cards: {user_cards} Score: {user_score}\nDealer's cards: {comp_cards} Score: {comp_score} Final: {compare_cards(comp_s=comp_score,user_s=user_score)}")

@router.callback_query(F.data.startswith('info_blackjack'))
async def blackjack_info(call: CallbackQuery):
    text_info = 'Blackjack is a popular casino card game where the goal is to have a hand value closer to 21 than the dealer without exceeding it. Each player is dealt two cards, and the dealer receives two cards, one face-up and one face-down. Number cards are worth their face value, face cards (Jack, Queen, King) are valued at 10, and Aces can be worth 1 or 11. Players can choose to hit (take another card) or stand (keep their current hand). The dealer must hit until reaching at least 17. The winner is the player closest to 21 without busting.'
    await call.message.edit_text(text=text_info,reply_markup=choose_action())


#Hangman Game
@router.callback_query(F.data.startswith('begin'))
async def hangman(call: CallbackQuery):
    await call.message.edit_text(text="Please choose a difficulty level 'Easy', 'Medium' or 'Hard'",reply_markup=choose_difficulty_hangman())

@router.callback_query(F.data.startswith('hangman_info'))
async def hangman_info(call: CallbackQuery):
    text_info = "Hangman Game is a fun and engaging word-guessing game where you need to guess the hidden word by suggesting letters. Every incorrect guess leads to loosing a life which consists of 6 lives in total.\n\nThere are 3 difficulty level of word which are\n'Easy'-words that are easy to guess and short\n'Medium'-words that are a bit difficult to guess but still manageable\n'Hard'-words that are longer than two lower levels and a bit difficult to guess."
    await call.message.edit_text(text=text_info,reply_markup=choose_action_hangman())

@router.callback_query(F.data.startswith('hard'))
async def hard_hangman(call: CallbackQuery, state: FSMContext):
    word = generate_random_word('hard')
    guessed_word = '_'*len(word)
    await state.update_data(secret_word=word, guessed_word=guessed_word, wrong_guesses=[], attempts=6)
    await call.message.edit_text(f"🎮 Hangman Started!\nWord: {guessed_word}\nLetters: {len(word)}\nGuess a letter:")
    await state.set_state(HangmanState.secret_word)

@router.callback_query(F.data.startswith('medium'))
async def hard_hangman(call: CallbackQuery, state: FSMContext):
    word = generate_random_word('medium')
    guessed_word = '_'*len(word)
    await state.update_data(secret_word=word, guessed_word=guessed_word, wrong_guesses=[], attempts=6)
    await call.message.edit_text(f"🎮 Hangman Started!\nWord: {guessed_word}\nLetters: {len(word)}\nGuess a letter:")
    await state.set_state(HangmanState.secret_word)

@router.callback_query(F.data.startswith('easy'))
async def easy_hangman(call: CallbackQuery, state: FSMContext):
    word = generate_random_word('easy')
    guessed_word = "_" * len(word)

    await state.update_data(secret_word=word, guessed_word=guessed_word, wrong_guesses=[], attempts=6)
    await call.message.edit_text(f"🎮 Hangman Started!\nWord: {guessed_word}\nLetters: {len(word)}\nGuess a letter:")
    await state.set_state(HangmanState.secret_word)

@router.message(HangmanState.secret_word)
async def guess_letter(message: Message, state: FSMContext):
    data = await state.get_data()
    secret_word = data["secret_word"]
    guessed_word = list(data["guessed_word"])
    wrong_guesses = data["wrong_guesses"]
    attempts = data["attempts"]
    guess = message.text.lower()

    # Prevent duplicate guesses
    if guess in guessed_word or guess in wrong_guesses:
        await message.answer("❗ You already guessed that letter! Try again.")
        return

    # Check if the guess is correct
    if guess in secret_word:
        for i, letter in enumerate(secret_word):
            if letter == guess:
                guessed_word[i] = guess
        await state.update_data(guessed_word="".join(guessed_word))

        if "_" not in guessed_word:  # Check if won
            await message.answer(f"🎉 Congratulations! You guessed the word: {secret_word}")
            return
    else:
        wrong_guesses.append(guess)
        attempts -= 1
        await state.update_data(wrong_guesses=wrong_guesses, attempts=attempts)

        if attempts == 0:  # Game over
            await message.answer(f"💀 Game Over! The word was: {secret_word}")
            return

    # Update user
    await message.answer(
        f"Word: {''.join(guessed_word)}\nLetters: {len(secret_word)}\n❌ Wrong guesses: {', '.join(wrong_guesses)}\n❤️ Attempts left: {attempts}"
    )

#Rock, Paper and Scissor game
@router.callback_query(F.data.startswith('go'))
async def rps(call: CallbackQuery):
    await call.message.edit_text(text='What do you choose? Rock Paper or Scissors',reply_markup=choose_rock_paper_scissor())

@router.callback_query(F.data.startswith('rock'))
async def rock(call: CallbackQuery):
    await call.message.answer(text=check_rps(0))

@router.callback_query(F.data.startswith('paper'))
async def rock(call: CallbackQuery):
    await call.message.answer(text=check_rps(1))

@router.callback_query(F.data.startswith('scissors'))
async def rock(call: CallbackQuery):
    await call.message.answer(text=check_rps(2))

@router.callback_query(F.data.startswith('rps_info'))
async def rps_info(call: CallbackQuery):
    await call.message.edit_text(text='''Rock-Paper-Scissors: A Brief Explanation
Rock-Paper-Scissors is a simple hand game played between two players. 

The rules are:
✊ Rock beats ✂️ Scissors (Rock crushes Scissors)
✋ Paper beats ✊ Rock (Paper covers Rock)
✂️ Scissors beats ✋ Paper (Scissors cut Paper)
If both players choose the same, it’s a tie 🤝''',reply_markup=choose_action_rps())

# Quiz Game


@router.callback_query(F.data.startswith('initiate'))
async def quiz_category(call: CallbackQuery):
    global SCORE
    SCORE = 0
    await call.message.answer(text='Choose a category of questions',reply_markup=choose_categories_quiz())

@router.callback_query(F.data.startswith('next_page'))
async def next_page_quiz(call: CallbackQuery):
    data = call.data.split(':')

    if len(data) != 5:  # Ensure data has all required parts
        return await call.answer("Error", show_alert=True)

    _, start, limit, page, total_pages = data
    start, limit, page, total_pages = map(int, [start, limit, page, total_pages])

    await call.message.edit_reply_markup(
        reply_markup=choose_categories_quiz(
            start=start + 9,
            limit=limit+9,
            current_page=page +1,
        )
    )

@router.callback_query(F.data.startswith('prev_page'))
async def prev_page(call: CallbackQuery):
    data = call.data
    __, start, finish, page = data.split(':')

    await call.message.edit_reply_markup(
        reply_markup=choose_categories_quiz(
            start=int(start) - 9,
            limit=int(finish) - 9,
            current_page=int(page) - 1,
        )
    )

@router.callback_query(F.data.startswith('category'))
async def quiz_difficulty(call: CallbackQuery, state: FSMContext):
    data = call.data.split('+')

    __, nam_cat, id_cat = data
    await state.update_data(category_name=nam_cat, category_id=id_cat)
    await call.message.edit_text(text='Choose a difficulty level of questions', reply_markup=choose_difficulty_quiz())

@router.callback_query(F.data.startswith('level'))
async def quiz_type(call: CallbackQuery, state: FSMContext):
    data = call.data
    __,level = data.split(':')
    await state.update_data(difficulty=level)
    await call.message.edit_text(text='Choose a type of questions',
                                 reply_markup=choose_type_quiz())

@router.callback_query(F.data.startswith('type'))
async def quiz_amount(call: CallbackQuery, state: FSMContext):
    data = call.data
    __,type_q = data.split(':')

    await call.message.edit_text(text='Write an amount of questions you need', reply_markup=None)
    await state.update_data(type_q=type_q)
    await state.set_state(QuizState.amount)

@router.message(QuizState.amount)
async def amount_quiz(message: Message, state: FSMContext):
    state_date = await state.get_data()
    category_name = state_date.get('category_name')
    category_id = state_date.get('category_id')
    difficulty = state_date.get('difficulty')
    type_q = state_date.get('type_q')
    num_questions = message.text

    questions = request_questions(
        num_questions=num_questions,
        category=category_id,
        difficulty=difficulty,
        q_type=type_q
    )
    user_id = users_repo.get_user(chat_id=message.from_user.id)
    quiz_repo.delete_quiz(user_id=user_id[0])
    for question in questions:
        question_text = question['question']
        correct_answer = question['correct_answer']
        incorrect_answers = question['incorrect_answers']

        question_text = unescape(question_text)
        correct_answer = unescape(correct_answer)
        incorrect_answers = [unescape(incorrect_answer) for incorrect_answer in incorrect_answers]

        all_answers = incorrect_answers + [correct_answer]
        random.shuffle(all_answers)
        quiz_repo.add_question(question_text,','.join(all_answers),correct_answer,user_id[0])


    await message.answer(text=f"Category: {category_name}\nDifficulty: {difficulty}\nAmount of questions: {num_questions}\n\nIf you're ready to start press 'Ready' button",reply_markup=ready_quiz())

@router.callback_query(F.data.startswith('ready'))
async def check_answers(call: CallbackQuery):
    user_id = users_repo.get_user(chat_id=call.from_user.id)
    quiz = quiz_repo.get_quiz(user_id=user_id[0])
    question = quiz[0][0]
    all_answers = quiz[0][1].split(',')
    correct_answer = quiz[0][2]

    await call.message.answer(text=f"{question}",
                              reply_markup=answer_questions(answers=all_answers, current=0, total=len(quiz)))

@router.callback_query(F.data.startswith('answer'))
async def check_answers(call: CallbackQuery):
    global SCORE
    data = call.data.split(':')
    _, user_answer, current, total= data
    user_id = users_repo.get_user(chat_id=call.from_user.id)
    quiz = quiz_repo.get_quiz(user_id=user_id[0])
    correct = quiz[int(current)][2]

    if user_answer == correct:
        SCORE += 1
        await call.message.answer(text=f"✅ You've chosen the correct answer! The correct answer is: {correct}")
    else:
        await call.message.answer(text=f"❗ You've chosen the wrong answer. The correct answer was: {correct}")

    if int(current)+1 != int(total):
        question = quiz[int(current)+1][0]
        all_answers = quiz[int(current)+1][1].split(',')
        correct_answer = quiz[int(current)+1][2]

        await call.message.answer(text=f"{question}", reply_markup=answer_questions(all_answers,current=int(current)+1,total=total))

    elif int(current) +1 == int(total):
        await call.message.reply(text=f'You have found {SCORE} questions out of {total}')

@router.callback_query(F.data.startswith('data_quiz'))
async def rps_info(call: CallbackQuery):
    await call.message.edit_text(text='''Welcome to the Quiz Game!
This is a fun and challenging quiz where you'll answer multiple-choice questions from various categories. You'll need to choose the correct answer from a list of options.
The game consists of different rounds, each with a specific difficulty level, category, and type of questions. Test your knowledge and see how many questions you can answer correctly!
Good luck and have fun! 🎉''', reply_markup=choose_action_quiz())

# Guess a number game

@router.callback_query(F.data.startswith('launch'))
async def guess_number(call: CallbackQuery, state: FSMContext):
    secret_number = random.randint(1,100)
    await state.update_data(secret_number=secret_number)
    await state.set_state(GuessNumState.number)
    await call.message.answer("I have chosen a number between 1 and 100. Try to guess it!")

@router.message(GuessNumState.number)
async def user_answer(message: Message, state: FSMContext):
    state_data = await state.get_data()
    secret_number = state_data.get('secret_number')
    try:
        guess = int(message.text)
    except ValueError:
        await message.answer("Please enter a valid number.")
        return
    if guess < secret_number:
        await message.answer("Too low! Try again.")
    elif guess > secret_number:
        await message.answer("Too high! Try again.")
    else:
        await message.answer("🎉 Congratulations! You guessed the number correctly.If you want to play again press the button 'Guess a number'")


@router.callback_query(F.data.startswith('number_info'))
async def number_info(call: CallbackQuery):
    await call.message.edit_text(text='The "Guess the Number" game is a simple interactive game where the bot selects a random number between 1 and 100. The user tries to guess the number by entering their guesses in the chat. The bot provides hints, saying whether the guess is too low or too high, guiding the player towards the correct answer. Once the correct number is guessed, the bot congratulates the player and offers to restart the game.',
                                 reply_markup=choose_action_number())


# Scramble a Word game

@router.callback_query(F.data.startswith('commence'))
async def scramble_word_difficulty(call: CallbackQuery):
    await call.message.edit_text(text="Choose a difficulty of a word 'Easy', 'Medium' or 'Hard'",reply_markup=choose_level_scramble())

@router.callback_query(F.data.startswith('difficulty'))
async def set_scramble_word(call: CallbackQuery, state: FSMContext):
    data = call.data
    _, level = data.split(":")
    word = generate_random_word(level)
    scrambled_word = "".join(random.sample(word, len(word)))
    await state.update_data(word=word)
    await state.set_state(WordScrambleState.word)
    await call.message.answer(f"Guess the word: **{scrambled_word}**")

@router.message(WordScrambleState.word)
async def check_answer(message: Message, state: FSMContext):
    state_data = await state.get_data()
    original_word = state_data.get('word')
    if message.text.lower() == original_word:
        await message.answer(f"🎉 Correct! The word was **{original_word}**. Press 'Scramble a Word' button to try again!")
        await state.clear()
    else:
        await message.answer("❌ Wrong! Try again.")

@router.callback_query(F.data.startswith('scramble_info'))
async def number_info(call: CallbackQuery):
    await call.message.edit_text(text="Guess the original word from the scrambled letters! Type your answer, and I'll tell you if you're right. 🎯🔠", reply_markup=choose_action_scramble_word())
