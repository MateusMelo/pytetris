# Example file showing a circle moving on screen
import pygame
from random import choice
from math import floor

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

DROP_PIECE = pygame.USEREVENT + 1
SPAWN_PIECE = pygame.USEREVENT + 2
SpawnPiece = pygame.event.Event(SPAWN_PIECE, attr1='SpawnPiece')

MIN_SPEED = .9
MAX_SPEED = .1
velocity_y = MIN_SPEED

def increase_speed():
    global velocity_y
    velocity_y -= .1
    if (velocity_y > MAX_SPEED):
        pygame.time.set_timer(DROP_PIECE, int(1000 * velocity_y))

def reset_speed():
    global velocity_y
    velocity_y = MIN_SPEED
    pygame.time.set_timer(DROP_PIECE, int(1000 * velocity_y))

increase_speed()

def has_index(l, i):
    try:
        return l[i]
    except:
        return None


class Grid:
    def __init__(self):
        self.cols = 9
        self.rows = 9
        self.grid = [[0] * self.rows for _ in range(self.cols)]
        self.current_piece = []
        self.current_piece_collided_down = False
        self.current_piece_collided_left = False
        self.current_piece_collided_right = False

    def draw(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                x = screen.get_width() / self.cols
                y = screen.get_height() / self.rows
                w = col * y
                h = row * x
                if (self.grid[row][col] == 1):
                    pygame.draw.rect(screen, pygame.Color("Red"), [w, h, x, y], 1)
                else:
                    pygame.draw.rect(screen, pygame.Color("Green"), [w, h, x, y], 1)
    
    def set_current_piece(self, piece):
        self.current_piece = piece
        for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if (row < len(self.current_piece)):
                        if (col < len(self.current_piece[row])):
                            self.grid[row][self.current_piece[row][col]] = 1
    
    def get_current_piece_cords(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if (row < len(self.current_piece)):
                    if (col < len(self.current_piece[row])):
                        return self.grid[row][self.current_piece[row][col]]
        return []
    
    def get_next_row_value(self):
        piece_next_row = []
        for col in self.current_piece[len(self.current_piece)-1]:
            if (has_index(self.grid, len(self.current_piece))):
                piece_next_row.append(self.grid[len(self.current_piece)][col])
        return piece_next_row
    
    def get_previous_column_index(self):
        piece_left_column = []
        for row in range(len(self.current_piece)):
            if (has_index(self.current_piece, row)):
                piece_left_column.append(self.current_piece[row][0])
        return piece_left_column
    
    def get_previous_column_value(self):
        piece_left_column = []
        for row in range(len(self.current_piece)):
            if (has_index(self.current_piece, row)):
                piece_left_column.append(self.grid[row][self.current_piece[row][0]-1])
        return piece_left_column
    
    def get_next_column_index(self):
        piece_right_column = []
        for row in range(len(self.current_piece)):
            if (has_index(self.current_piece, row)):
                piece_right_column.append(self.current_piece[row][len(self.current_piece[row])-1])
        return piece_right_column
    
    def clear_last_piece_position(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if (row < len(self.current_piece)):
                    if (col < len(self.current_piece[row])):
                        self.grid[row][self.current_piece[row][col]] = 0

    def advance_one_column(self):
        self.current_piece = [[]] + self.current_piece

    def drop_current_piece(self):
        if (self.current_piece_collided_down is not True):
            self.clear_last_piece_position()
            self.advance_one_column()

        if (len(self.current_piece) >= self.cols or self.current_piece_collided_down is True):
            pygame.event.post(SpawnPiece)
            self.current_piece_collided_down = False

        self.draw_current_piece()
        
        next_row_cels = self.get_next_row_value()
        for cel in next_row_cels:
            if cel == 1:
                self.current_piece_collided_down = True

    def draw_current_piece(self):
        for row in range(len(self.grid)):
                        for col in range(len(self.grid[row])):
                            if (row < len(self.current_piece)):
                                if (col < len(self.current_piece[row])):
                                    self.grid[row][self.current_piece[row][col]] = 1

    def move_current_piece_left(self):
        self.current_piece_collided_right = False

        for cel in self.get_previous_column_value():
            if cel == 1:
                self.current_piece_collided_left = True

        if (self.current_piece_collided_down is not True):
            self.clear_last_piece_position()
            for row in range(len(self.current_piece)):
                for col in range(len(self.current_piece[row])):
                    if self.current_piece[row][col] > 0 and self.current_piece[row][col] < len(self.grid) and self.current_piece_collided_left is not True:
                        self.current_piece[row][col] -= 1
        
        self.draw_current_piece()

        for cel in self.get_previous_column_index():
            if cel == 0:
                self.current_piece_collided_left = True
        
    def move_current_piece_right(self):
        self.current_piece_collided_left = False

        if (self.current_piece_collided_down is not True):
            self.clear_last_piece_position()
            for row in range(len(self.current_piece)):
                for col in range(len(self.current_piece[row])):
                    if self.current_piece[row][col] < len(self.grid[row]) and self.current_piece_collided_right is not True:
                        self.current_piece[row][col] += 1
        
        self.draw_current_piece()

        for cel in self.get_next_column_index():
            if cel == len(self.grid)-1:
                self.current_piece_collided_right = True
    
    def move_current_piece_down(self):
        self.drop_current_piece()

grid = Grid()
middle = floor(len(grid.grid) / 2)

class Piece:
    def __init__(self):
        self.pieces = [
            [[middle-2, middle-1, middle, middle+1]],
            [[middle], [middle, middle-1, middle+1]],
            [[middle, middle+1], [middle, middle-1]],
            [[middle-1, middle], [middle, middle+1]],
            [[middle+1], [middle-1, middle, middle+1]],
            [[middle-1, middle], [middle-1, middle]],
        ]
        self.seq = [i for i in range(len(self.pieces))]
    
    def give(self):
        return self.pieces[choice(self.seq)]
        
    def move_left():
        pass # Move piece one position to left
    def move_right():
        pass # Move piece one position to right
    def move_down(self):
        pass 

    def spin():
        pass # Spin the piece in clockwise

#
#                   # # # #
#
# piece = [[middle-2, middle-1, middle, middle+1]]

#                     #
#                   # # #
# piece = [[middle], [middle, middle-1, middle+1]]

#
#                        # #          
#                      # #
# piece = [[middle, middle+1], [middle, middle-1]]

#
#                      # #          
#                        # #
# piece = [[middle-1, middle], [middle, middle+1]]

#
#                           #
#                       # # #
# piece = [[middle+1], [middle-1, middle, middle+1]]

#
#                         # #
#                         # #
# piece = [[middle-1, middle], [middle-1, middle]]

grid.draw()

pygame.event.post(SpawnPiece)

# pygame.key.set_repeat(1000, 1000)

k_down_state = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                grid.move_current_piece_left()
            elif event.key == pygame.K_RIGHT:
                grid.move_current_piece_right()
            elif event.key == pygame.K_DOWN:
                k_down_state = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                reset_speed()
                k_down_state = False
        elif event.type == SPAWN_PIECE:
            piece = Piece()
            grid.set_current_piece(piece.give())
        elif event.type == DROP_PIECE:
            grid.drop_current_piece()

    if k_down_state:
        increase_speed()

    screen.fill((0, 0, 0))

    grid.draw()

    pygame.display.update()
    clock.tick(60)