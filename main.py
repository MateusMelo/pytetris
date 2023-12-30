# Example file showing a circle moving on screen
import pygame
# from random import choice
from math import floor

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

DROP_PIECE = pygame.USEREVENT + 1
SPAWN_PIECE = pygame.USEREVENT + 2
SpawnPiece = pygame.event.Event(SPAWN_PIECE, attr1='SpawnPiece')

pygame.time.set_timer(DROP_PIECE, 1000)

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
        self.current_piece_collided = False

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
    
    def get_next_row_state(self):
        piece_next_row = []
        for col in self.current_piece[len(self.current_piece)-1]:
            if (has_index(self.grid, len(self.current_piece))):
                piece_next_row.append(self.grid[len(self.current_piece)][col])
        return piece_next_row
    
    def clear_last_piece_position(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if (row < len(self.current_piece)):
                    if (col < len(self.current_piece[row])):
                        self.grid[row][self.current_piece[row][col]] = 0

    def advance_one_column(self):
        self.current_piece = [[]] + self.current_piece

    def drop_current_piece(self):
        if (self.current_piece_collided is not True):
            self.clear_last_piece_position()
            self.advance_one_column()

        if (len(self.current_piece) >= self.cols or self.current_piece_collided is True):
            pygame.event.post(SpawnPiece)
            self.current_piece_collided = False

        for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if (row < len(self.current_piece)):
                        if (col < len(self.current_piece[row])):
                            if (self.grid[row][self.current_piece[row][col]] != 1):
                                self.grid[row][self.current_piece[row][col]] = 1
        
        next_row_cels = self.get_next_row_state()
        for cel in next_row_cels:
            if cel == 1:
                self.current_piece_collided = True

    def move_current_piece_left(self):
        if (self.current_piece_collided is not True):
            self.clear_last_piece_position()
            for row in range(len(self.current_piece)):
                for col in range(len(self.current_piece[row])):
                    self.current_piece[row][col] -= 1

        for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if (row < len(self.current_piece)):
                        if (col < len(self.current_piece[row])):
                            if (self.grid[row][self.current_piece[row][col]] != 1):
                                self.grid[row][self.current_piece[row][col]] = 1


    def move_current_piece_right(self):
        if (self.current_piece_collided is not True):
            self.clear_last_piece_position()
            for row in range(len(self.current_piece)):
                for col in range(len(self.current_piece[row])):
                    self.current_piece[row][col] += 1

        for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if (row < len(self.current_piece)):
                        if (col < len(self.current_piece[row])):
                            if (self.grid[row][self.current_piece[row][col]] != 1):
                                self.grid[row][self.current_piece[row][col]] = 1
    
grid = Grid()
middle = floor(len(grid.grid) / 2)

class Piece:
    def __init__(self):
        self.current_piece = [[middle-1, middle], [middle-1, middle]]
        self.current_row = 0

    def spawn(self):
        return self.current_piece
        # cols = 9
        # rows = 9
        # grid_state = [[0] * rows for _ in range(cols)]
        # for row in range(len(grid_state)):
        #         for col in range(len(grid_state[row])):
        #             if (row < len(self.current_piece)):
        #                 if (col < len(self.current_piece[row])):
        #                     grid_state[row][self.current_piece[row][col]] = 1
        return grid_state

    def give(self):
        return self.current_piece
        
    def move_left():
        pass # Move piece one position to left
    def move_right():
        pass # Move piece one position to right
    def move_down(self):
        pass 

    def spin():
        pass # Spin the piece in clockwise
                    

piece = Piece()

# seq = [i for i in range(len(grid.grid))]
# col = choice(seq)
# row = choice(seq)

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                grid.move_current_piece_left()
            if event.key == pygame.K_RIGHT:
                grid.move_current_piece_right()
        if event.type == SPAWN_PIECE:
            grid.set_current_piece(piece.give())
        if event.type == DROP_PIECE:
            grid.drop_current_piece()
        if event.type == pygame.QUIT:
            pygame.quit()            

    screen.fill((0, 0, 0))

    grid.draw()

    pygame.display.update()
    clock.tick(120)