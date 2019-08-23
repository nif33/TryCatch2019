"""
Tetris game using Pygame Library
Used for Intermediate Programming Workshop at Try/CATCH 2019.
Objective was to complete the main function using the comments provided.
https://trycatch.cs.sfu.ca/
Adapted from freeCodeCamp.org
"""

import pygame
import random

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 800
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [[".....",
      ".....",
      "..00.",
      ".00..",
      "....."],
     [".....",
      "..0..",
      "..00.",
      "...0.",
      "....."]]

Z = [[".....",
      ".....",
      ".00..",
      "..00.",
      "....."],
     [".....",
      "..0..",
      ".00..",
      ".0...",
      "....."]]

I = [["..0..",
      "..0..",
      "..0..",
      "..0..",
      "....."],
     [".....",
      "0000.",
      ".....",
      ".....",
      "....."]]

O = [[".....",
      ".....",
      ".00..",
      ".00..",
      "....."]]

J = [[".....",
      ".0...",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..00.",
      "..0..",
      "..0..",
      "....."],
     [".....",
      ".....",
      ".000.",
      "...0.",
      "....."],
     [".....",
      "..0..",
      "..0..",
      ".00..",
      "....."]]

L = [[".....",
      "...0.",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..0..",
      "..0..",
      "..00.",
      "....."],
     [".....",
      ".....",
      ".000.",
      ".0...",
      "....."],
     [".....",
      ".00..",
      "..0..",
      "..0..",
      "....."]]

T = [[".....",
      "..0..",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..0..",
      "..00.",
      "..0..",
      "....."],
     [".....",
      ".....",
      ".000.",
      "..0..",
      "....."],
     [".....",
      "..0..",
      ".00..",
      "..0..",
      "....."]]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3


def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

# This function returns a random shape
def get_shape():
    global shapes, shape_colors
    return Piece(5, 0, random.choice(shapes))

# this draws the start text and game over text
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines


def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one

    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape", 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy- 30))


def draw_window(surface):
    surface.fill((0,0,0))
    # Tetris Title
    font = pygame.font.SysFont("comicsans", 60)
    label = font.render("TETRIS", 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)

    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    pygame.display.update()


def main():
    #1 declare a global variable called grid
    global grid

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    #2A we need two variables, one called current_piece and one called next_piece. Set both of these to a random shape using one of the above functions
    current_piece = get_shape()
    next_piece = get_shape()

    #2B we need a Boolean variable to tell us whether we need to change our piece or not. Think: at the start of the program, is it False or True?
    #Protip: remember to capitalize False and True in Python, or use 0 and 1
    change_piece = False
    
    #3 make a boolean variable called run which will tell us how long to run a while loop. Will this be True or False at the beginning?
    run = True

    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        #4 we need a variable called fall_speed to tell us how fast the piece should fall. Set this to any number between 0 and 1 for now, and adjust as needed later
        fall_speed = 0.27

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed: # every couple of seconds, this will be true and the piece will move down by one
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get(): # an event is a key press
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN: # if a key is pressed down
                #5A if the event.key (the key pressed) is equal to pygame.K_LEFT, subtract one to current_piece.x (the x value of the current piece)
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    #7 see below
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                #5B now do the elif (else if in other languages) for a right key
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    #7 see below
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                #5C write an elif for if the key is up. This time we want to rotate shape.
                #Protip: We used current_piece.x to access the x attribute of current_piece, current piece also has an attribute called rotation
                #Hint: You will need to use the modulus symbol (%)
                elif event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    #7 see below
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                #6 if the key is down, move the shape down by one
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    #7 see below
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                #7 Wait! The shapes will just keep moving because they don't know when to stop! Use the valid_space() function give, if a piece is not in a valid space after the movement that just happened, reverse that movement to undo it (if we moved right, move left now)
                #Protip: In Python, not represents "not". In other languages you may have seen ! as "not"

                #8 You're on your own for this one, what happens when the user presses space? Code the "hard drop" (piece immediately goes down as far as it can go)
                if event.key == pygame.K_SPACE:
                  while valid_space(current_piece, grid):
                      current_piece.y += 1
                  current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece: # this must match the variable you declared above
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            #9 we changed the piece! Update your variables, what has current_piece, next_piece, and change_piece (boolean) become?
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            #10 we need to call this four times to check for multiple clear rows, put it in a loop that runs 4 times
            #Protip: Unfamiliar with Python? Sometimes you have to learn new languages at work, it is helpful to the look at the language library in the useful links
            clear_rows(grid, locked_positions)

        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        #11 After the piece movement, we need to check if user lost. Pass locked_positions to one of the functions provided above. If the user lost, change the boolean variable you declared earlier called run
        if check_lost(locked_positions):
            run = False

    draw_text_middle("Game Over", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle("Press any key to begin.", 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")

main_menu()  # start game