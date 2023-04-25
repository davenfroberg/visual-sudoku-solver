from puzzle_loader import Puzzle_Loader
class Cell:
    def __init__(self, box_id):
        self.box_id = box_id
        self.number = 0
        self.possible = [True] * 10
    
    def cant_be(self, number):
        self.possible[number] = False
   
    def can_be(self, number):
        return self.possible[number]
    
    def __repr__(self):
        return str(self.number)
    
#troubleshooting method that displays the board according to the __repr__ method in Cell class
def display_board():
    for cell in board:
        print(cell)

def create_board():
    sub_board = []
    for y in range(3):
        row = []
        for x in range(3):
            row.append(Cell(1))
        for x in range(3):
            row.append(Cell(2))
        for x in range (3):
            row.append(Cell(3))
        
        sub_board.append(row)
    for y in range(3):
        row = []
        for x in range(3):
            row.append(Cell(4))
        for x in range(3):
            row.append(Cell(5))
        for x in range (3):
            row.append(Cell(6))
        
        sub_board.append(row)
    for y in range(3):
        row = []
        for x in range(3):
            row.append(Cell(7))
        for x in range(3):
            row.append(Cell(8))
        for x in range (3):
            row.append(Cell(9))
        
        sub_board.append(row)
    
    return sub_board

def load_board():
    for y in range(0,9):
        for x in range(0,9):
            solve(y,x,puzzle[y][x])


#displays the board with all of the inputted numbers
def display_board():
    for row in board:
        for cell in row:
            print(str(cell) + " ", end='')
        print()

#input (write) a solved number into the puzzle, eliminating it as a possible number for appropriate cells
def solve(row, column, number):
    if number != 0:
        board[row][column].number = number
       
        for i in range (1,10):
            if (i != number):
                board[row][column].cant_be(i)
        
        for i in range (0,9):
            if(i != row):
                board[i][column].cant_be(number)
        
        for i in range (0,9):
            if (i != column):
                board[row][i].cant_be(number)
        
        for i in range(0,9):
            for j in range(0,9):
                if (board[i][j].box_id == board[row][column].box_id and board[i][j].number != number):
                    board[i][j].cant_be(number)

#O(N^2) seems super slow for this but for now im gonna leave it
#check to see if the board is solved (not necessarily solved correctly, but that's redundant as the logic in the sovling algorithm is robust)
def solved():
    for row in board:
        for cell in row:
            if cell.number == 0:
                return False
    
    return True

#return the number of possible numbers a cell can be
def total_possible(cell):
    possible = 0
    for n in range (1,10):
        if cell.can_be(n):
            possible += 1
    
    return possible

#return the first possible (ascending from 1-9) number a cell can be
def find_first_possible(cell):
    for n in range(1,10):
        if cell.can_be(n):
            return n
    
    return 0

#checks for cells that only have one possible number
def logic_one():
    changes = 0
    for row in range(0,9):
        for column in range(0,9):
            cell = board[row][column]
            if total_possible(cell) == 1 and cell.number == 0:
                solve(row, column, find_first_possible(cell))
                changes += 1
   
    return changes


loader = Puzzle_Loader()
puzzle = loader.load_puzzle("puzzle.png")

#access board with [row(y)][column(x)]
board = create_board()
load_board()

display_board()

changes = -1
while not solved():
    while changes != 0:
        changes = 0
        changes += logic_one()
        #changes += logic_two()
        #changes += logic_three()
        #changes += logic_four_box()
        #changes += logic_four_row()
        #changes += logic_four_column()
    if not solved():
        print("Was unable to solve! Try implementing a guessing alogrithm instead!")
        break
    else:
        print("Solved the sudoku successfuly!")
        break