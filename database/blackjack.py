import random

blackjack_cards = [
    "A♥", "A♦", "A♣", "A♠",
    "2♥", "2♦", "2♣", "2♠",
    "3♥", "3♦", "3♣", "3♠",
    "4♥", "4♦", "4♣", "4♠",
    "5♥", "5♦", "5♣", "5♠",
    "6♥", "6♦", "6♣", "6♠",
    "7♥", "7♦", "7♣", "7♠",
    "8♥", "8♦", "8♣", "8♠",
    "9♥", "9♦", "9♣", "9♠",
    "10♥", "10♦", "10♣", "10♠",
    "J♥", "J♦", "J♣", "J♠",
    "Q♥", "Q♦", "Q♣", "Q♠",
    "K♥", "K♦", "K♣", "K♠"
]

def deal_card():
    card = random.choice(blackjack_cards)
    if card[0] in ["J", "Q", "K"]:
        card_value = 10
    elif card[:2] in ['10']:
        card_value = 10
    elif card[0] == "A":
        card_value = 11
    else:
        card_value = int(card[0])
    return card, card_value


def calculate_hand_value(hand):
    total_value = sum(hand)

    # If the hand is a Blackjack (2 cards, total value 21)
    if total_value == 21 and len(hand) == 2:
        return 0  # Special case for Blackjack

    # Adjust for Aces (if total_value > 21 and there's an Ace)
    while total_value > 21 and 11 in hand:
        hand.remove(11)
        hand.append(1)  # Convert Ace from 11 to 1
        total_value = sum(hand)

    return total_value


def compare_cards(comp_s, user_s):
    if comp_s == user_s:
        return 'Draw'
    elif comp_s == 0:
        return 'Lose, opponent has Blackjack'
    elif user_s == 0:
        return 'Win with Blackjack'
    elif user_s > 21:
        return 'You went over. You lose'
    elif comp_s > 21:
        return 'Opponent went over. You win'
    elif user_s > comp_s:
        return 'Win'
    elif comp_s > user_s:
        return 'Lose'