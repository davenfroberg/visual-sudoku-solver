from puzzle_loader import Puzzle_Loader
from puzzle_inputter import Puzzle_Inputter

import time
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
    
class Guess:
    def __init__(self, current_board, first_x, first_y, number):
        sub_board = []
        for y in range(9):
            row = []
            for x in range(9):
                current_cell = current_board[y][x]
                new_cell = Cell(current_cell.box_id)
                new_cell.number = current_cell.number
                for n in range (1,10):
                    if not current_cell.can_be(n):
                        new_cell.cant_be(n)
                row.append(new_cell)
            sub_board.append(row)

        self.board = sub_board
        self.guess_num = number
        self.guess_x = first_x
        self.guess_y = first_y

#load the puzzle from a file
def load_puzzle_file(name):
    puzzle = []
    try:
        with open(name + '.txt') as f:
                for line in f:
                    row = []
                    line = line.strip()
                    for char in line:
                        if (char == " "):
                            continue
                        row.append(int(char))
                    puzzle.append(row)
    except FileNotFoundError:
        with open('default.txt') as f:
                for line in f:
                    row = []
                    line = line.strip()
                    for char in line:
                        if (char == " "):
                            continue
                        row.append(int(char))
                    puzzle.append(row)
    return puzzle


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

#input the numbers from the loaded puzzle into the board
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

#check to see if the board is solved (not necessarily solved correctly, but that's redundant as the logic in the sovling algorithm is robust)
def solved():
    for row in board:
        for cell in row:
            if cell.number == 0:
                return False
    
    return True

# this is incredibly inefficient but it only runs once at the very end of the program so the inefficiency can be justified
# check to see if the board is actually solved correctly and has no logical errors
def check_correct():
    for y in range(9):
        for x in range(9):
            for a in range(9):
                if (a != x and board[y][a].number == board[y][x].number):
                    return False
                elif (a != y and board[a][x].number == board[y][x].number):
                    return False
                
            for b in range(9):
                for a in range(9):
                    if board[b][a].box_id == board[y][x].box_id and (a != x or b != y) and board[b][a].number == board[y][x].number:
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

#returns the second possible (ascending from 1-9) number a cell can be
def find_second_possible(cell):
    first_found = False
    for n in range(1,10):
        if not first_found and cell.can_be(n):
            first_found = True
        elif first_found and cell.can_be(n):
            return n
    
    return 0

#returns the amount of possible numbers a cell has
def total_possible(cell):
    possible = 0
    for n in range(1,10):
        if cell.can_be(n):
            possible += 1

    return possible

# returns the coords (x,y) of the first cell pos that has no solved number in it (0), if all are solved, then return (-1, -1)
def first_empty():
    for y in range(9):
        for x in range(9):
            if board[y][x].number == 0:
                return (x, y)
    return (-1, -1)

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

#checks for cells that have a possible number that no other cells in its column/row have possible
def logic_two():
    changes = 0
    for y in range(9):
        for x in range(9):
            solveable = True
            for n in range(1,10):
                if board[y][x].can_be(n):
                    for a in range(9):
                        if a == x:
                            continue
                        if(board[y][a].can_be(n)):
                            solveable = False
                            break
                        if a == 8:
                            if board[y][x].number == n:
                                break
                            solve(y, x, n)
                            changes += 1
                    if not solveable:
                        for a in range(9):
                            if a == y:
                                continue
                            if board[a][x].can_be(n):
                                solveable = False
                                break
                            if a == 8:
                                if board[y][x].number == n:
                                    break
                                solve(y, x, n)
                                changes += 1
    return changes

#checks for cells that have a possible number that no other cells in its box can have
def logic_three():
    changes = 0

    for current_id in range(1,10):
        for n in range(1,10):
            counter = 0
            solved = False
            for y in range(9):
                for x in range(9):
                    if board[y][x].number == n and board[y][x].box_id == current_id:
                        solved = True
                    if board[y][x].box_id == current_id:
                        if (board[y][x].can_be(n)):
                            counter += 1
            
            if counter == 1 and not solved:
                for y in range(9):
                    for x in range(9):
                        if board[y][x].box_id == current_id:
                            if board[y][x].can_be(n):
                                solve(y, x, n)
                                changes += 1
    return changes

#checks for two unsolved cells in the same box that have the same only two possible numbers and setting all of the other cells in the box to have those two numbers be not possible
def logic_four_box():
    changes = 0
    current_box = 0
    first_possible = 0
    second_possible = 0
    possibilities = 0

    for y in range(9):
        for x in range(9):
            cell = board[y][x]
            current_box = board[y][x].box_id
            first_possible = find_first_possible(cell)
            second_possible = find_second_possible(cell)
            possibilities = 0
            if total_possible(cell) == 2:
                for b in range(9):
                    for a in range(9):
                        cell = board[b][a]
                        if cell.box_id == current_box and total_possible(cell) == 2 and find_first_possible(cell) == first_possible and find_second_possible(cell) == second_possible and (a != x or b != y):
                            possibilities += 1
                        
                if possibilities == 1:
                    for b in range(9):
                        for a in range(9):
                            cell = board[b][a]
                            if (cell.can_be(first_possible) or cell.can_be(second_possible)) and (find_first_possible(cell) != first_possible or find_second_possible(cell) != second_possible) and cell.box_id == current_box:
                                cell.cant_be(first_possible)
                                cell.cant_be(second_possible)
                                changes += 1
    return changes

#checks for two unsolved cells in the same row that have the same only two possible numbers and setting all of the other cells in the row to have those two numbers be not possible
def logic_four_row():
    changes = 0
    first_possible = 0
    second_possible = 0
    possible = False

    for y in range(9):
        for x in range(9):
            cell = board[y][x]
            first_possible = find_first_possible(cell)
            second_possible = find_second_possible(cell)
            possible = False

            if total_possible(cell) == 2:
                for x2 in range(9):
                    cell = board[y][x2]
                    if total_possible(cell) == 2 and find_first_possible(cell) == first_possible and find_second_possible(cell) == second_possible and x2 != x:
                        possible = True
                if (possible):
                    for x2 in range(9):
                        cell = board[y][x2]
                        if (cell.can_be(first_possible) or cell.can_be(second_possible)) and find_first_possible(cell) != first_possible and find_second_possible(cell) != second_possible:
                            cell.cant_be(first_possible)
                            cell.cant_be(second_possible)
                            changes += 1
            
    return changes

#checks for two unsolved cells in the same column that have the same only two possible numbers and setting all of the other cells in the column to have those two numbers be not possible
def logic_four_column():
    changes = 0
    first_possible = 0
    second_possible = 0
    possible = False

    for y in range(9):
        for x in range(9):
            cell = board[y][x]
            first_possible = find_first_possible(cell)
            second_possible = find_second_possible(cell)
            possible = False

            if total_possible(cell) == 2:
                for y2 in range(9):
                    cell = board[y2][x]
                    if total_possible(cell) == 2 and find_first_possible(cell) == first_possible and find_second_possible(cell) == second_possible and y2 != y:
                        possible = True
                if (possible):
                    for y2 in range(9):
                        cell = board[y2][x]
                        if (cell.can_be(first_possible) or cell.can_be(second_possible)) and find_first_possible(cell) != first_possible and find_second_possible(cell) != second_possible:
                            cell.cant_be(first_possible)
                            cell.cant_be(second_possible)
                            changes += 1
            
    return changes

# reverts the board to the state before the most recent guess and set the cell that was guessed on to not have the guessed number be possible
def revert(state_counter):
    temp_board = board_states[state_counter].board
    for y in range(9):
        for x in range(9):
            temp_cell = temp_board[y][x]
            board[y][x] = Cell(temp_cell.box_id)
            board[y][x].number = temp_cell.number
            for n in range(1, 10):
                if not temp_cell.can_be(n):
                    board[y][x].cant_be(n)

    board_state = board_states[state_counter]
    board[board_state.guess_y][board_state.guess_x].cant_be(board_state.guess_num)
    return state_counter - 1

puzzle = [[]]
board_states = []
state_counter = -1

setting = input("Would you like to load the puzzle from an image (1) or file (2)?: ")
if (setting == "1") :
    loader = Puzzle_Loader()
    puzzle = loader.load_puzzle("puzzle.png")
else:
    name = input("Input the name of the puzzle: ")
    puzzle = load_puzzle_file(name)

#access board with [row(y)][column(x)]
board = create_board()
load_board()

display_board()

changes = -1
while not solved():
    while changes != 0:
        changes = 0
        changes += logic_one()
        changes += logic_two()
        changes += logic_three()
        changes += logic_four_box()
        changes += logic_four_row()
        changes += logic_four_column()
    
    #guessing algorithm
    if not solved():
        first_empty_cell = first_empty()
        first_x = first_empty_cell[0]
        first_y = first_empty_cell[1]
        
        while (total_possible(board[first_y][first_x]) == 0):
            state_counter = revert(state_counter)
        
        state_counter += 1

        first_possible = find_first_possible(board[first_y][first_x])
        if state_counter < len(board_states) and len(board_states) != 0:
            board_states[state_counter] = Guess(board, first_x, first_y, first_possible)
        else:
            board_states.append(Guess(board, first_x, first_y, first_possible))

        solve(first_y, first_x, first_possible)

display_board()

if check_correct():
    print("The Sudoku has been solved successfully!")
else:
    print ("ERROR: Sudoku has not been solved correctly") #this should NEVER happen if the logic algorithms are correct

time.sleep(2)
puzzle_inputter = Puzzle_Inputter()
puzzle_inputter.input_solution(board) #comment out this line if you don't want the answers to be inputted automatically