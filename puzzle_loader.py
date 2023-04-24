import pytesseract
import cv2
import numpy as np

class Puzzle_Loader: 
    CELL_CUTOFF_PERCENTAGE = 0.05 # percentage of cell size that should be cut off from top and left sides of cell image to prevent borders from being in image

    def __init__(self):
        self.board_image = np.zeros((1,1,3), np.uint8)
        self.cell_height = 0
        self.cell_width = 0
        self.top_left_corner = (0,0)
        self.width = 0
        self.height = 0

    def compare(self, first, second):
        if (len(first) != len(second)):
            return False
        for i in range(len(first)):
            if (first[i] != second[i]):
                return False
        return True
    
    def crop_board(self, img):
        self.width = img.shape[1]
        self.height = img.shape[0]
        top_border = 0
        bottom_border = 0
        right_border = 0
        left_border = 0

        for i in range(self.height):
            if not self.compare(img[i, int(self.width/2)], [255,255,255]):
                #print("Found top border at: " + str(i))
                top_border = i
                break

        for i in reversed(range(self.height)):
            if not self.compare(img[i, int(self.width/2)], [255,255,255]):
                #print("Found bottom border at: " + str(i))
                bottom_border = i
                break

        for i in range(self.width):
            if not self.compare(img[int(self.height/2), i], [255,255,255]):
                #print("Found left border at: " + str(i))
                left_border = i
                break

        for i in reversed(range(self.width)):
            if not self.compare(img[int(self.height/2), i], [255,255,255]):
                #print("Found right border at: " + str(i))
                right_border = i
                break

        return img[top_border:bottom_border, left_border:right_border]

    def get_cell_info(self):
        top = -1
        bottom = -1
        left = -1
        right = -1
        prev = self.board_image[0,5]
        i = 1
        while i <= self.height:
            if (top == -1 and not self.compare(prev, self.board_image[i, 5])):
                top = i
                i+=1
            elif (not self.compare(prev, self.board_image[i,5])):
                bottom = i-1
                break
            prev = self.board_image[i,5]
            i+=1

        prev = self.board_image[5,0]
        i = 1
        while i <= self.width:
            if (left == -1 and not self.compare(prev, self.board_image[5,i])):
                left = i
                i+=1
            elif (not self.compare(prev, self.board_image[5,i])):
                right = i-1
                break
            prev = self.board_image[5,i]
            i+=1

        self.cell_height = bottom - top
        self.cell_width = right - left
        self.top_left_corner = (top, left)

    def get_all_cells_as_images(self):
        cutoff_pixels = int(self.cell_height * Puzzle_Loader.CELL_CUTOFF_PERCENTAGE)
        board = []
        cell_count = 0
        row_top= self.top_left_corner[0]
        row_left = self.top_left_corner[1]
        for i in range(row_top, self.height, self.cell_height + 2):
            row = []
            for j in range(row_left, self.width, self.cell_width + 2):
                cell = self.board_image[(i + cutoff_pixels):(i + self.cell_height), (j + cutoff_pixels):(j + self.cell_width)]
                row.append(cell)
                cell_count += 1
                if (cell_count % 9 == 0):
                   break
            board.append(row)
            if (cell_count == 81):
                break
        
        return board

    def load_puzzle(self, puzzle_name):
        print("Loading puzzle from image! Please wait...")
        self.board_image = self.crop_board(cv2.imread(puzzle_name))
        self.get_cell_info()
        cell_images = self.get_all_cells_as_images()
        board = []
        count = 0
        for image_row in cell_images:
            row = []
            for image in image_row:
                count+=1
                pre_processed = self.pre_process(image)
                cell = pytesseract.image_to_string(pre_processed, lang='osd', config="-c tessedit_char_whitelist=0123456789 --psm 10")
                if (len(cell) == 0):
                    row.append("0")
                else:
                    row.append(cell.strip())
            board.append(row)
       
        print("Puzzle loaded!")
        return board

    def pre_process(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening
        return invert