import pygame
import numpy as np
import json

WIDTH =  450
HEIGHT = 550
DIMENSION = 9  # Sudoku is 9x9
CELL_WIDTH = WIDTH/DIMENSION

BLACK = (0,0,0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
RED = (255,0,0)
GREY = (211,211,211)
GREEN = (0, 255, 0)

class Sudoku:
    
    def __init__(self):
        """Inits the board of the sudoku by reading it from a txt file."""
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.board = np.array(self.board)
        self.board_initial = self.board.copy()
        
    def insert_move(self, val, row, col):
        """Inserts a move into the board."""
        if self.board[row, col] == 0:  # there is an empty space
            self.board[row, col] = val
    
    def delete_move(self, row, col):
        """Deletes the move from the board."""
        if self.board_initial[row, col] == 0:
            self.board[row, col] = 0
    
    def valid_move(self, val, row, col):
        """Checks if the move is valid."""
        if row < DIMENSION and col < DIMENSION:
            square = self.get_square(row, col)  # Check 3x3 square
            horizontal_line = self.board[row, :]  # Check row
            vertical_line = self.board[:, col]  # Check column
            if val in square or val in horizontal_line or val in vertical_line:
                return False
            else:
                return True   
            
    def get_square(self, row, col):
        """Gets the corresponding square of numbers to the given row and column."""
        start_row = (row//3)*3
        start_col = (col//3)*3
        return self.board[start_row:start_row+3, start_col:start_col+3] 

    def done(self):
        """Writes the current board to a txt file."""
        self.board = self.board.tolist()
        with open("Sudoku.txt", "w") as f:
            json.dump(self.board, f)
        self.board = np.array(self.board)
    
    def reset(self):
        """Resets the sudoku to the initial state."""
        self.board = self.board_initial.copy()


class Drawer:
    
    def __init__(self, screen):
        """Inits the drawer class."""
        self.screen = screen
    
    def draw_board(self, sudoku, pos_x, pos_y):
        """Draws the entire sudoku."""
        self.screen.fill(WHITE)
        self.draw_lines(BLACK, 10)
        self.draw_numbers(sudoku)
        x, y = self.mouse_to_cell(pos_x, pos_y)
        if pos_y < HEIGHT-100:
            self.highlight_cell(x, y)       
        # done button "pressed"
        elif pos_y > 475 and pos_y < 475+CELL_WIDTH and pos_x > 6*CELL_WIDTH: 
            sudoku.done()
        # reset button "pressed"
        elif pos_y > 475 and pos_y < 475+CELL_WIDTH and pos_x > 0*CELL_WIDTH and pos_x < 3*CELL_WIDTH: 
            sudoku.reset()
        pygame.display.update()
        
    def draw_lines(self, color, num_lines):
        """Draws all lines on the screen."""
        start = (0,0)
        end = (0,HEIGHT-100)
        for i in range(num_lines):
            if i % 3 == 0:
                pygame.draw.line(self.screen, color, start, end, 3)
            else:
                pygame.draw.line(self.screen, color, start, end, 1)
            start = self.adjust_tuple(start, 0, WIDTH/(num_lines-1))
            end = self.adjust_tuple(end, 0, WIDTH/(num_lines-1))
        
        start = (0,0)
        end = (WIDTH, 0)
        for i in range(num_lines):
            if i % 3 == 0:
                pygame.draw.line(self.screen, color, start, end, 3)
            else:
                pygame.draw.line(self.screen, color, start, end, 1)
            start = self.adjust_tuple(start, 1, WIDTH/(num_lines-1))
            end = self.adjust_tuple(end, 1, WIDTH/(num_lines-1))

        self.draw_button(start_x=(0*CELL_WIDTH), start_y=477, text="Reset", margin=5)
        self.draw_button(start_x=6*CELL_WIDTH, start_y=477, text="Done", margin=0)

    def draw_button(self, start_x, start_y, text, margin):
        """Draws a "button" to the game board."""
        pygame.draw.rect(self.screen, RED, (start_x, start_y, CELL_WIDTH*3-margin, CELL_WIDTH))
        pygame.draw.rect(self.screen, BLACK, (start_x, start_y, CELL_WIDTH*3-margin, CELL_WIDTH),3)
        myfont = pygame.font.SysFont(None, 72)
        textsurface = myfont.render(text, False, BLACK)
        pos = (start_x, start_y)
        self.screen.blit(textsurface, pos)
        
    def draw_numbers(self, sudoku):
        """Displays the numbers of the sudoku."""
        myfont = pygame.font.SysFont(None, 80)
        y = 0
        for r in range(len(sudoku.board)):
            x = 0
            for c in range(len(sudoku.board[r,:])):
                if sudoku.board[r,c] != 0:
                    if sudoku.board[r,c] == sudoku.board_initial[r,c]:
                        number = str(sudoku.board[r,c])
                        textsurface = myfont.render(number, False, BLACK)
                        pos = (x+9,y+2)
                        self.screen.blit(textsurface, pos)
                    else:
                        number = str(sudoku.board[r,c])
                        textsurface = myfont.render(number, False, BLUE)
                        pos = (x+9,y+2)
                        self.screen.blit(textsurface, pos)
                x += WIDTH/len(sudoku.board)
            y += WIDTH/len(sudoku.board)
            
    def highlight_cell(self, x, y):
        """Highlights the cell the user is on."""
        start_x = x*CELL_WIDTH
        start_y = y*CELL_WIDTH
        if start_y < HEIGHT-100:
            pygame.draw.rect(self.screen, RED, (start_x, start_y, CELL_WIDTH, CELL_WIDTH),3)
    
    def wrong_move(self, row, column, clock):
        """Displays a red cross in case of a wrong move."""
        if row < DIMENSION and column < DIMENSION:
            myfont = pygame.font.SysFont(None, 80)
            textsurface = myfont.render("X", False, RED)
            pos = (column*CELL_WIDTH+7,row*CELL_WIDTH+2)  # add small margin to make it center
            self.screen.blit(textsurface, pos)
            pygame.display.update()
            clock.tick(1)   
        
    @staticmethod    
    def mouse_to_cell(pos_x, pos_y):
        """Static method to convert the mouse position to a position on the board."""
        x = pos_x // CELL_WIDTH
        y = pos_y // CELL_WIDTH
        return int(x), int(y)
    
    @staticmethod
    def adjust_tuple(x, index, increment):
        """Static method to increment a tuple."""
        x = list(x)
        x[index] += increment
        return tuple(x)
    
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Sudoku')
    clock = pygame.time.Clock()
    screen.fill(WHITE)
        
    sudoku = Sudoku()
    drawer = Drawer(screen)

    done = False
    pos_x = pos_y = 0
    x = y = 0
    key = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill(WHITE)
                (pos_x, pos_y) = pygame.mouse.get_pos()   
                x, y = drawer.mouse_to_cell(pos_x, pos_y)               
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if sudoku.valid_move(key, y, x):
                    sudoku.insert_move(key, y, x)
                    key = 0
                elif not sudoku.valid_move(key, y, x) and key > 0:
                    drawer.wrong_move(y,x, clock)
                if event.key == pygame.K_DELETE:
                    sudoku.delete_move(y, x)
                    key = 0
                if event.key == pygame.K_UP:
                    pos_y -= CELL_WIDTH
                    if pos_y < 0:
                        pos_y = 0
                    key = 0
                if event.key == pygame.K_DOWN:
                    pos_y += CELL_WIDTH
                    if pos_y > WIDTH:
                        pos_y = WIDTH-1
                    key = 0
                if event.key == pygame.K_LEFT:
                    pos_x -= CELL_WIDTH
                    if pos_x < 0:
                        pos_x = 0
                    key = 0
                if event.key == pygame.K_RIGHT:
                    pos_x += CELL_WIDTH
                    if pos_x > WIDTH:
                        pos_x = WIDTH-1
                    key = 0
                x, y = drawer.mouse_to_cell(pos_x, pos_y) 
      
        drawer.draw_board(sudoku, pos_x, pos_y)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    
if __name__ == '__main__':
    main()