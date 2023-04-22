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
        return str(self.possible[4])
    
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


#access board by [row][column]
board = create_board()

create_board()

solve (1,2,4)
display_board()

