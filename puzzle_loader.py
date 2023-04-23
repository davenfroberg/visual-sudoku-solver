from PIL import Image

class Puzzle_Loader: 
    
    def __init__(self):
        self.board_image = Image.new("1", (1,1))
        self.cell_height = 0
        self.cell_width = 0
        self.top_left_corner = (0,0)

    def crop_board(self, img):
        width = img.width
        height = img.height
        top_border = 0
        bottom_border = 0
        right_border = 0
        left_border = 0

        for i in range(height):
            if (img.getpixel((width/2, i)) != (255,255,255,255)):
                #print("Found top border at: " + str(i))
                top_border = i
                break

        for i in reversed(range(height)):
            if (img.getpixel((width/2, i)) != (255,255,255,255)):
                #print("Found bottom border at: " + str(i))
                bottom_border = i
                break

        for i in range(width):
            if (img.getpixel((i, height/2)) != (255,255,255,255)):
                #print("Found left border at: " + str(i))
                left_border = i
                break

        for i in reversed(range(width)):
            if (img.getpixel((i, height/2)) != (255,255,255,255)):
                #print("Found right border at: " + str(i))
                right_border = i
                break

        board = img.crop((left_border, top_border, right_border, bottom_border))

        return board

    def get_cell_info(self):
        top = -1
        bottom = -1
        left = -1
        right = -1
        prev = self.board_image.getpixel((5, 0))
        for i in range(1, self.board_image.height):
            if (top == -1 and prev != self.board_image.getpixel((5,i))):
                top = i
                i+= 2
            elif (prev != self.board_image.getpixel((5,i))):
                bottom = i-1
                break
            prev = self.board_image.getpixel((5,i))
        
        prev = self.board_image.getpixel((0, 5))
        for i in range(1, self.board_image.width):
            if (left == -1 and prev != self.board_image.getpixel((i,5))):
                left = i
                i+=2
            elif (prev != self.board_image.getpixel((i,5))):
                right = i-1
                break
            prev = self.board_image.getpixel((i,5))
        self.cell_height = bottom - top
        self.cell_width = right - left
        self.top_left_corner = (top, left)

    def get_all_cells_as_images(self):
        self.get_cell_info()
        board = []
        cell_count = 0
        row_top= self.top_left_corner[0]
        row_left = self.top_left_corner[1]
        for i in range(row_top, self.board_image.height, self.cell_height):
            row = []
            for j in range(row_left, self.board_image.width, self.cell_width):
                cell = self.board_image.crop((j, i, j + self.cell_width, i + self.cell_height))
                row.append(cell)
                cell_count += 1
                if (cell_count % 9 == 0):
                   break
            board.append(row)
            i+= self.cell_height
            if (cell_count == 81):
                break
        return board


    def load_puzzle(self, puzzle_name):
        self.board_image = self.crop_board(Image.open(puzzle_name))
        cell_images = self.get_all_cells_as_images()
        print("Puzzle loaded!")
        return [[]]