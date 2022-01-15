import pygame

background_color = 'white'
seperator_color = 'black'
shape_default_color = seperator_color
shape_win_color = 'forestgreen'
shape_lost_color = 'firebrick3'
square_default_color = background_color
square_hover_color = 'gray'
square_click_color = 'darkgray'

square_size = 124
sep_size = 16
shape_inset = 16
x_thickness = 16
o_thickness = x_thickness-4
border_size = 32
info_height = 32

marked_x, marked_o = [], []
mark_lists = [marked_x, marked_o]
turn_of_x = True
game_over = False
needs_redraw = True
winning_line = []

def draw_shape(shape, color):
    shape_surface = pygame.Surface((square_size-shape_inset*2, square_size-shape_inset*2))
    shape_surface.set_colorkey('purple')
    shape_surface.fill('purple')
    max_x = shape_surface.get_width()
    max_y = shape_surface.get_height()
    if shape == 'x':
        pygame.draw.line(shape_surface, color, (0, 0), (max_x, max_y), x_thickness)
        pygame.draw.line(shape_surface, color, (0, max_y), (max_x, 0), x_thickness)
    elif shape == 'o':
        pygame.draw.circle(shape_surface, color, (max_x/2, max_y/2), max_x/2, o_thickness)
    return shape_surface

def draw_square(shape, color, shape_color):
    square_surface = pygame.Surface((square_size, square_size))
    square_surface.fill(color)
    if shape == 'x' or shape == 'o':
        square_surface.blit(draw_shape(shape, shape_color), (shape_inset, shape_inset))
    return square_surface

def draw_game_area(event=None):
    game_side_length = 3*square_size + 2*sep_size
    game_surface = pygame.Surface((game_side_length, game_side_length))
    game_surface.fill(seperator_color)
    global game_over, turn_of_x
    if game_over and event and event.type == pygame.MOUSEBUTTONUP:
        marked_x.clear()
        marked_o.clear()
        winning_line.clear()
        event = None
        turn_of_x = True
        game_over = False
    for y in range(3):
        for x in range(3):
            square_coords = x*(square_size+sep_size), y*(square_size+sep_size)
            square_coll_coords = (square_coords[0]+border_size, square_coords[1]+border_size)
            square_coll_rect = pygame.Rect(square_coll_coords, (square_size, square_size))
            if (x, y) not in marked_x and (x, y) not in marked_o:
                shape = ''
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if len(winning_line) < 3 and square_coll_rect.collidepoint(mouse_x, mouse_y):
                    if pygame.mouse.get_pressed(3)[0]:
                        square_color = square_click_color
                    else:    
                        square_color = square_hover_color
                    if event:
                        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP:
                            if turn_of_x == True:
                                marked_x.append((x, y))
                                turn_of_x = False
                            else:
                                marked_o.append((x, y))
                                turn_of_x = True
                            check_game_over()
                else:
                    square_color = square_default_color
            if (x, y) in marked_x:
                shape = 'x'
                square_color = square_default_color
            if (x, y) in marked_o:
                shape = 'o'
                square_color = square_default_color
            if game_over and len(winning_line) >= 3 and (x, y) in winning_line:
                shape_color = shape_win_color
            elif game_over and len(winning_line) == 0:
                shape_color = shape_lost_color
            else:
                shape_color = shape_default_color
            game_surface.blit(draw_square(shape, square_color, shape_color), square_coords)
    return game_surface

def end_game():
    global game_over, needs_redraw
    game_over = True
    needs_redraw = True

def get_horizontal_line(coords):
    return [(0, coords[1]), (1, coords[1]), (2, coords[1])]
def get_vertical_line(coords):
    return [(coords[0], 0), (coords[0], 1), (coords[0], 2)]
def get_diagonal_slash_line(coords):
    line = [(0, 0), (1, 1), (2, 2)]
    if coords in line: return line
    else: return []
def get_diagonal_backslash_line(coords):
    line = [(2, 0), (1, 1), (0, 2)]
    if coords in line: return line
    else: return []

def check_game_over():
    if game_over or len(marked_x)+len(marked_o) < 3:
        return
    line_getters = [get_horizontal_line, get_vertical_line, get_diagonal_slash_line, get_diagonal_backslash_line]
    if len(winning_line) < 3:
        for mark_list in mark_lists:
            for list_entry in mark_list:
                for get_line in line_getters:
                    for line_entry in get_line(list_entry):
                        if line_entry in mark_list:
                            winning_line.append(line_entry)
                    if len(winning_line) >= 3:
                        end_game()
                        return
                    else:
                        winning_line.clear()
    if len(winning_line) < 3 and len(marked_x)+len(marked_o) >= 9:
        end_game()

pygame.init()
window_side_length = 3*square_size + 2*sep_size + 2*border_size
pygame.display.set_caption('Tic Tac Toe')
display_surface = pygame.display.set_mode((window_side_length, window_side_length))
while True:
    if needs_redraw:
        display_surface.fill(background_color)
        display_surface.blit(draw_game_area(), (border_size, border_size))
        pygame.display.flip()
        needs_redraw = False
    for e in pygame.event.get():
        match(e.type):
            case pygame.QUIT:
                exit()
            case pygame.MOUSEBUTTONDOWN | pygame.MOUSEBUTTONUP | pygame.MOUSEMOTION:
                display_surface.fill(background_color)
                display_surface.blit(draw_game_area(e), (border_size, border_size))
                if game_over:
                    pygame.display.set_caption('Tic Tac Toe   (click to restart)')
                elif turn_of_x:
                    pygame.display.set_caption('Tic Tac Toe   (X to turn)')
                else:
                    pygame.display.set_caption('Tic Tac Toe   (O to turn)')
                pygame.display.flip()