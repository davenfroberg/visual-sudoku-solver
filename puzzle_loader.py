import pytesseract
import cv2
import numpy as np
import copy

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

       #offset = int(self.height / 18) #approx "center" of the cell, doesn't have to be exact at all, just somewhere away from the edge of the cell
        offset = int(self.width / 88)

        prev = self.board_image[1,offset]

        #dup = copy.copy(self.board_image)
        
        i = 1
        while i <= self.height:
            #dup[i,offset] = [0, 255, 0]
            #cv2.imshow("dup", dup)
            #cv2.waitKey(0)
            if (top == -1 and not self.compare(prev, self.board_image[i, offset])):
                #print("Found top border at: " + str(i))
                top = i
                i+=offset
            elif (not self.compare(prev, self.board_image[i,offset])):
                #print("Found bottom border at: " + str(i))
                bottom = i-1
                break
            prev = self.board_image[i,offset]
            i+=1

        prev = self.board_image[offset,1]
        i = 1
        while i <= self.width:
            #dup[offset,i] = [0, 255, 0]
            #cv2.imshow("dup", dup)
            #cv2.waitKey(0)
            if (left == -1 and not self.compare(prev, self.board_image[offset,i])):
                #print("Found left border at: " + str(i))
                left = i
                i+=offset
            elif (not self.compare(prev, self.board_image[offset,i])):
                #print("Found right border at: " + str(i))
                right = i-1
                break
            prev = self.board_image[offset,i]
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
                #cv2.imshow("image", image)
                #cv2.waitKey(0)
                count+=1
                pre_processed = self.pre_process(image)
                #cv2.imshow("pre_processed", pre_processed)
                #cv2.waitKey(0)

                cell = pytesseract.image_to_string(pre_processed, lang='osd', config="-c tessedit_char_whitelist=123456789 --psm 10")
                if (len(cell) == 0):
                    row.append(0)
                else:
                    value = int(cell.strip())
                
                    #this is my current, SUPER non-elegant solution to the OCR incorrectly detecting a 1 as a 7, will fix OCR Later
                    #this is the only thing needing to be fixed
                    if (value == 7):
                        cv2.imshow("Clarification Needed", pre_processed)
                        cv2.waitKey(0)
                        value = int(input("What number is this: "))
                    
                    print(str(value))
                    row.append(value)
                    
            board.append(row)
       
        print("Puzzle loaded!")
        return board

#pre-process image of number for OCR
    def pre_process(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening
        return invert