from pyautogui import press

class Puzzle_Inputter:
    def __init__(self):
        pass

    def input_solution(self, board):
        for y in range(0, 9, 2):
            for x1 in range(0, 9):
                press(str(board[y][x1].number))
                press('right')
            if y == 8:
                break
            press('down')
            for x2 in reversed(range(0,9)):
                press(str(board[y+1][x2].number))
                press('left')
            press('down')

            
