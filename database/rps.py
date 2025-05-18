import random

def check_rps(user_input):
    rps=['Rock','Paper','Scissors']
    comp_chose = random.randint(0,2)
    if user_input == comp_chose:
        return f"Your opponent chose '{rps[comp_chose]}'\nIt is draw. Better luck nexxt time."
    elif (user_input == 0 and comp_chose == 2) or \
            (user_input == 1 and comp_chose == 0) or \
            (user_input == 2 and comp_chose == 1):
        return f"Your opponent chose '{rps[comp_chose]}'\nYou won! Congratulations!"
    else:
        return f"Your opponent chose '{rps[comp_chose]}'\nYou lose. Better luck nexxt time."