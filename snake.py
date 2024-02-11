import shutil
import os
from time import sleep
import keyboard
import random

BOARD_SIZE_X = 24
BOARD_SIZE_Y = 14

class SnakeCell:
    
    def __init__(self, position_x, position_y, direction, shape):
        self.position_x = position_x
        self.position_y = position_y 
        self.direction = direction
        self.shape = shape


class Snake:
    
    def __init__(self, cells):
        self.cells = cells
        self.board = [[]]*BOARD_SIZE_Y


    def print_board(self):
        columns = shutil.get_terminal_size().columns
        os.system('cls')
        for line in self.board:
            line_string = ''.join(line)
            print(line_string.center(columns))


    def create_empty_board(self):
        self.board[0] = [' ']
        self.board[1] = ['   ~Snake~   ']
        self.board[2] = [' ']
        self.board[3] = ['╔'] + ['═']*(BOARD_SIZE_X - 2) + ['╗']
        for i in range(4, BOARD_SIZE_Y - 1):
            self.board[i] = ['║'] +[' ']*(BOARD_SIZE_X - 2) + ['║']
        self.board[BOARD_SIZE_Y - 1] = ['╚'] + ['═']*(BOARD_SIZE_X - 2) + ['╝']


    def add_snake(self, state):
        snake_cells = self.cells if state == 'alive' else self.cells[:-1]
        
        for cell in snake_cells:
            self.board[cell.position_y][cell.position_x] = cell.shape


    def generate_treat(self):
        good_treat = False
        while not good_treat:
            treat_x = random.randint(4, BOARD_SIZE_Y - 2)
            treat_y = random.randint(1, BOARD_SIZE_X - 3)
            good_treat = True
            for cell in snake.cells:
                if cell.position_x == treat_y and cell.position_y == treat_x:
                    good_treat = False
        return [treat_x, treat_y]

    
    def add_treat(self, treat):
        treat_x, treat_y = treat
        self.board[treat_x][treat_y] = '*'


    def treat_is_there(self):
        for line in self.board:
            for item in line:
                if item == '*':
                    return True
        return False


    def move_snake(self, treat_there):
        mod_horizontal = lambda a : (a - 1) % (BOARD_SIZE_X - 2) + 1
        mod_vertical = lambda a : (a - 4) % (BOARD_SIZE_Y - 5) + 4

        head = self.cells[-1]
        tail = self.cells[0]

        if head.direction == 'U':
            new_position_x = head.position_x
            new_position_y = mod_vertical(head.position_y - 1)
            new_shape = '│'
        
        if head.direction == 'D':
            new_position_x = head.position_x
            new_position_y = mod_vertical(head.position_y + 1)
            new_shape = '│'
        
        if head.direction == 'R':
            new_position_y = head.position_y
            first_position_x = mod_horizontal(head.position_x + 1)
            first_shape = '─'
            self.cells.append(SnakeCell(first_position_x, head.position_y, head.direction, first_shape))
            new_position_x = mod_horizontal(first_position_x + 1)
            new_shape = '─'
        
        if head.direction == 'L':
            new_position_y = head.position_y
            first_position_x = mod_horizontal(head.position_x - 1)
            first_shape = '─'
            self.cells.append(SnakeCell(first_position_x, head.position_y, head.direction, first_shape))
            new_position_x = mod_horizontal(first_position_x - 1)
            new_shape = '─'

        self.cells.append(SnakeCell(new_position_x, new_position_y, head.direction, new_shape))

        if treat_there:
            if tail.shape == '─':
                self.cells = self.cells[2:]
            else:
                self.cells = self.cells[1:]


    def keyboard_callback(self, event, treat_there):
        mod_horizontal = lambda a : (a - 1) % (BOARD_SIZE_X - 2) + 1
        mod_vertical = lambda a : (a - 4) % (BOARD_SIZE_Y - 5) + 4

        head = self.cells[-1]
        tail = self.cells[0]
        
        if head.direction == 'U' and (event == 'right' or event == 'left'):
            new_position_y = mod_vertical(head.position_y - 1)
            
            if event == 'right':
                self.cells.append(SnakeCell(head.position_x, new_position_y, 'R', '┌'))
            elif event == 'left':
                self.cells.append(SnakeCell(head.position_x, new_position_y, 'L', '┐'))
            
            if treat_there:
                if tail.shape == '─':
                    self.cells = self.cells[2:]
                else:
                    self.cells = self.cells[1:]

        if head.direction == 'D' and (event == 'right' or event == 'left'):
            new_position_y = mod_vertical(head.position_y + 1)
            
            if event == 'right':
                self.cells.append(SnakeCell(head.position_x, new_position_y, 'R', '└'))
            elif event == 'left':
                self.cells.append(SnakeCell(head.position_x, new_position_y, 'L', '┘'))
            
            if treat_there:
                if tail.shape == '─':
                    self.cells = self.cells[2:]
                else:
                    self.cells = self.cells[1:]
        
        if head.direction == 'R' and (event == 'up' or event == 'down'):
            new_position_x = mod_horizontal(head.position_x + 1)
            
            if event == 'up':
                self.cells.append(SnakeCell(new_position_x, head.position_y, 'U', '┘'))
            elif event == 'down':
                self.cells.append(SnakeCell(new_position_x, head.position_y, 'D', '┐'))
            
            if treat_there:
                if tail.shape == '─':
                    self.cells = self.cells[2:]
                else:
                    self.cells = self.cells[1:]

        if head.direction == 'L' and (event == 'up' or event == 'down'):
            new_position_x = mod_horizontal(head.position_x - 1)
            
            if event == 'up':
                self.cells.append(SnakeCell(new_position_x, head.position_y, 'U', '└'))
            elif event == 'down':
                self.cells.append(SnakeCell(new_position_x, head.position_y, 'D', '┌'))
            
            if treat_there:
                if tail.shape == '─':
                    self.cells = self.cells[2:]
                else:
                    self.cells = self.cells[1:]


    def is_alive(self): 
        mod_horizontal = lambda a : (a - 1) % (BOARD_SIZE_X - 2) + 1
        mod_vertical = lambda a : (a - 4) % (BOARD_SIZE_Y - 5) + 4
              
        snake_cells = [[self.cells[i].position_x, self.cells[i].position_y] for i in range(len(self.cells))]
        snake_alive = True
        for i in range(len(snake_cells)):
            x, y = snake_cells[i]
            for j in range(i+1, len(snake_cells)):
                u, v = snake_cells[j]
                if x == u and y == v:
                    snake_alive = False

        head = self.cells[-1]
        tail = self.cells[0]

        if head.shape == '─' and tail.shape ==  '─' and head.position_y == tail.position_y:
            if head.position_x == mod_horizontal(tail.position_x + 1) or head.position_x == mod_horizontal(tail.position_x - 1):
                snake_alive = False

        if head.shape == '│' and tail.shape ==  '│' and head.position_x == tail.position_x:
            if head.position_y == mod_vertical(tail.position_y + 1) or head.position_y == mod_vertical(tail.position_y - 1):
                snake_alive = False
        
        return snake_alive



if __name__ == "__main__":

    snake = Snake(starting_snake)
    
    snake_alive = True
    treat_there = False

    keyboard.add_hotkey('right arrow', lambda: snake.keyboard_callback('right', treat_there))
    keyboard.add_hotkey('left arrow', lambda: snake.keyboard_callback('left', treat_there))
    keyboard.add_hotkey('up arrow', lambda: snake.keyboard_callback('up', treat_there))
    keyboard.add_hotkey('down arrow', lambda: snake.keyboard_callback('down', treat_there))

    starting_snake = [SnakeCell(i, 7, 'R', '─') for i in range(2, 8)]
    speed = 0
    acceleration = 0.02
    max_speed = 20
    
    while snake_alive:
        snake.create_empty_board()
        if not treat_there:
            treat = snake.generate_treat()
            speed += 1
        snake.add_treat(treat)
        if snake.is_alive():
            snake.add_snake('alive')
        else:
            snake.add_snake('dead')
        snake.print_board()
        sleep(0.5 - min(speed, max_speed)*acceleration)
        treat_there = snake.treat_is_there()
        snake.move_snake(treat_there)
        snake_alive = snake.is_alive()
