import getpass

def ask_attempt_amount():
    valid_input = False
    while valid_input == False:
        attempt_amount = input('Enter amount of guess attempts: ')
        if len(attempt_amount) >= 1 and attempt_amount.isnumeric():
            valid_input = True
        else:
            print('Invalid input!', end=' ')
    return int(attempt_amount)

def ask_guess():
    valid_input = False
    while valid_input == False:
        guess = input('Enter a guess: ')
        if len(guess) == 1 and guess.isalpha():
            valid_input = True
        else:
            print('Invalid input!', end=' ')
    guess = guess.upper()
    return guess

def print_secret(secret: str, good_guesses, bad_guesses):
    print()
    for char in secret:
        if char in good_guesses:
            print(f'{char}', end=' ')
        elif char.isspace():
            print(f' ', end=' ')
        else:
            print('_', end=' ')
    if len(bad_guesses) == 1:
        print(f'| failed guess: {bad_guesses} ({len(bad_guesses)}/{max_attempts_amount})')
    elif len(bad_guesses) > 1:
        print(f'| failed guesses: {bad_guesses} ({len(bad_guesses)}/{max_attempts_amount})')
    print()

valid_input = False
while valid_input == False:
    secret = getpass.getpass('Enter word to be guessed (input hidden): ',)
    if len(secret) >= 1:
        valid_input = True
        for char in secret:
            if not (char.isalpha() or char.isspace()):
                valid_input = False
    if valid_input == False:
        print('Invalid input!', end=' ', flush=True)
secret = secret.upper()

max_attempts_amount = ask_attempt_amount()

bad_guesses = []
good_guesses = []
game_won, game_lost = False, False
print_secret(secret, good_guesses, bad_guesses)
while game_won == False and game_lost == False:
    guess = ask_guess()
    if guess in secret:
        if guess not in good_guesses:
            good_guesses.append(guess)
            game_won = True
            for char in secret:
                if char not in good_guesses and not char.isspace():
                    game_won = False
    else:
        bad_guesses.append(guess)
        if len(bad_guesses) >= max_attempts_amount:
            game_lost = True
    print_secret(secret, good_guesses, bad_guesses)

if game_won:
    print(f"That's right, the secret was '{secret}'.")
    print('Game over, you won! :)')
else:
    print(f"Oops, you've run out of attempts. (the secret was '{secret}')")
    print('Game over, you lost! :(')