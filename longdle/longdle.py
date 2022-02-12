from pathlib import Path
import random
import pygame

LETTER_DEFAULT = 0
LETTER_INCLUDED = 1
LETTER_ACCEPTED = 2
LETTER_WRONG = 3

background_color = 'gray40'
box_text_color, info_text_color = 'black', 'white'
box_sizes = (64, 64)
box_line_thickness = 3
letter_gap, line_gap = 3, 20
box_font_size, button_font_size = 32, 16
button_width, button_height = 120, 30

word_length = 5
guess_amount = 6
window_x = box_sizes[0]*word_length + letter_gap*(word_length-1) + 100
window_y = box_sizes[1]*guess_amount + line_gap*(guess_amount-1) + 100
window_sizes = (window_x, window_y)
solution_window_width = window_x-100
solution_window_height = (window_y/2)-100

def reset_game():
    global solution_word, guesses, current_guess, letter_statuses_lists, displaying_solution, game_suspended
    solution_word = random.choice(possible_words)
    guesses = ['' for guess in range(guess_amount)]
    current_guess = 0
    letter_statuses_lists = [[LETTER_DEFAULT for letter in range(word_length)] for guess in range(guess_amount)]
    displaying_solution = False
    game_suspended = False

def draw_letter_box(letter, status):
    box_surface = pygame.Surface(box_sizes)
    box_x, box_y = box_sizes
    box_surface.fill(box_text_color)
    inner_box_rect = pygame.rect.Rect(box_line_thickness, box_line_thickness, box_x-2*box_line_thickness, box_y-2*box_line_thickness)
    if status == LETTER_DEFAULT:
        color = 'darkgray'
    elif status == LETTER_INCLUDED:
        color = 'yellow3'
    elif status == LETTER_ACCEPTED:
        color = 'green3'
    elif status == LETTER_WRONG:
        color = 'red'
    pygame.draw.rect(box_surface, color, inner_box_rect)
    font = pygame.font.Font(pygame.font.get_default_font(), box_font_size)
    text_x, text_y = font.size(letter)
    box_surface.blit(font.render(letter, True, box_text_color), (box_x/2 - text_x/2, box_y/2 - text_y/2))
    return box_surface

def draw_word(word, letter_statuses):
    box_x, box_y = box_sizes
    word_surface = pygame.Surface((box_x*word_length+letter_gap*word_length, box_y))
    word_surface.fill(background_color)
    for letter_index in range(word_length):
        if letter_index < len(word):
            letter = word[letter_index]
        else:
            letter = ''
        word_surface.blit(draw_letter_box(letter, letter_statuses[letter_index]), ((box_x+letter_gap)*letter_index, 0))
    return word_surface

def draw_game_area():
    game_surface = pygame.Surface(window_sizes)
    game_surface.fill(background_color)
    box_x, box_y = box_sizes
    size = box_x*word_length + letter_gap*(word_length-1)
    for guess_index in range(guess_amount):
        current_word = guesses[guess_index]
        if not game_suspended and guess_index == current_guess and len(current_word) < word_length:
            current_word += '_'
        game_surface.blit(draw_word(current_word, letter_statuses_lists[guess_index]), (window_x/2-size/2, 40+(box_y+line_gap)*guess_index))
    return game_surface

def draw_button(label):
    button_surface = pygame.Surface((button_width, button_height))
    button_surface.fill("gray25")
    font = pygame.font.Font(pygame.font.get_default_font(), button_font_size)
    text_x, text_y = font.size(label)
    button_surface.blit(font.render(label, True, info_text_color), (button_width/2 - text_x/2, button_height/2 - text_y/2))
    return button_surface

def draw_solution():
    info_line_gap = 25
    info_top_text_font_size = 32
    info_bot_text_font_size = info_top_text_font_size*2
    popup_surface = pygame.Surface((solution_window_width, solution_window_height), pygame.SRCALPHA)
    background_surface = pygame.Surface((solution_window_width, solution_window_height))
    background_surface.fill('gray20')
    background_surface.set_alpha(230)
    background_surface = background_surface.convert_alpha()
    popup_surface.blit(background_surface, (0, 0))
    top_font = pygame.font.Font(pygame.font.get_default_font(), info_top_text_font_size)
    bot_font = pygame.font.Font(pygame.font.get_default_font(), info_bot_text_font_size)
    top_text = 'solution:'
    top_text_x, top_text_y = top_font.size(top_text)
    bot_text_x, bot_text_y = bot_font.size(solution_word)
    text_block_y = top_text_y + bot_text_y + info_line_gap
    popup_surface.blit(top_font.render(top_text, True, info_text_color), (solution_window_width/2-top_text_x/2, solution_window_height/2-text_block_y/2))
    popup_surface.blit(bot_font.render(solution_word, True, info_text_color), (solution_window_width/2-bot_text_x/2, solution_window_height/2+text_block_y/2-bot_text_y))
    return popup_surface

def draw():
    display_surface.fill(background_color)
    display_surface.blit(draw_game_area(), (0, 0))
    display_surface.blit(draw_button('Restart'), (0, window_y-button_height))
    display_surface.blit(draw_button('Solution'), (window_x-button_width, window_y-button_height))
    if displaying_solution:
        display_surface.blit(draw_solution(), (window_x/2-solution_window_width/2, window_y/2-solution_window_height/2))
    pygame.display.flip()

pygame.init()
random.seed()
pygame.display.set_caption('Longdle')
display_surface = pygame.display.set_mode(window_sizes)
script_location = Path(__file__).absolute().parent
with open(script_location / 'words_alpha.txt') as word_file:
    english_words = set(word_file.read().split())
with open(script_location / f'{word_length}_letter_words.txt') as input_file:
    possible_words = [line.strip().upper() for line in input_file.readlines()]
reset_game()
draw()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if not game_suspended:
            if e.type == pygame.TEXTINPUT:
                if len(guesses[current_guess]) < word_length:
                    guesses[current_guess] = guesses[current_guess] + e.text.upper()
                draw()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if len(guesses[current_guess]) == word_length and guesses[current_guess].lower() in english_words:
                        remaining_letters = solution_word
                        for i, (g, s) in enumerate(zip(guesses[current_guess], solution_word)):
                            if g == s:
                                letter_statuses_lists[current_guess][i] = LETTER_ACCEPTED
                                remaining_letters = remaining_letters[:i] + remaining_letters[i+1:]
                        for i, g in enumerate(guesses[current_guess]):
                            if g in remaining_letters and letter_statuses_lists[current_guess][i] != LETTER_ACCEPTED:
                                letter_statuses_lists[current_guess][i] = LETTER_INCLUDED
                        if letter_statuses_lists[current_guess] == [1 for letter in solution_word]:
                            game_suspended == True
                        current_guess = current_guess + 1
                    else:
                        letter_statuses_lists[current_guess] = [LETTER_WRONG for l in range(word_length)]
                    draw()
                if e.key == pygame.K_BACKSPACE:
                    letter_statuses_lists[current_guess] = [LETTER_DEFAULT for l in range(word_length)]
                    guesses[current_guess] = guesses[current_guess][:len(guesses[current_guess])-1]
                    draw()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == pygame.BUTTON_LEFT:
            if e.pos[1] >= window_y-button_height:
                if e.pos[0] < button_width:
                    reset_game()
                    draw()
                elif e.pos[0] > window_x-button_width:
                    displaying_solution = (not displaying_solution)
                    game_suspended = (not game_suspended)
                    draw()