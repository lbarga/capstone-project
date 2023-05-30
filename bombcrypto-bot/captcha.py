import cv2
import cv2 as cv
import numpy as np
from screen import *
from detection import *
import pyautogui
from mouse import *

def findPuzzlePieces(result, piece_img, threshold=0.5):
    piece_w = piece_img.shape[1]
    piece_h = piece_img.shape[0]
    yloc, xloc = np.where(result >= threshold)


    r= []
    for (piece_x, piece_y) in zip(xloc, yloc):
        r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])
        r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])


    r, weights = cv2.groupRectangles(r, 1, 0.2)

    if len(r) < 2:
        return findPuzzlePieces(result, piece_img,threshold-0.01)

    if len(r) == 2:
        return r

    if len(r) > 2:
        # print('overshoot by %d' % len(r))


        return r

def get_slider_button():
    return detect_image_location('samples/slider-button.png')





def get_pieces_position(t = 150):
    px, py, _, _ = get_captcha_popup().position

    w = 380
    h = 200

    x_offset = -90
    y_offset = 60

    x = px + x_offset
    y = py + y_offset

    current_screen = get_current_screen()

    cropped = current_screen[y: y + h, x: x + w]
    blurred = cv2.GaussianBlur(cropped, (3, 3), 0)
    edges = cv2.Canny(blurred, threshold1=t / 2, threshold2=t, L2gradient=True)

    piece_img = cv.imread('samples/piece.png', cv.IMREAD_UNCHANGED)
    piece_img_gray = cv2.cvtColor(piece_img, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(edges, piece_img_gray, cv2.TM_CCORR_NORMED)

    puzzle_pieces = findPuzzlePieces(result, piece_img_gray)

    if puzzle_pieces is None:
        return None

    absolute_puzzle_pieces = []
    for i, puzzle_piece in enumerate(puzzle_pieces):
        px, py, pw, ph = puzzle_piece
        absolute_puzzle_pieces.append([x + px, y + py, pw, ph])

    absolute_puzzle_pieces = np.array(absolute_puzzle_pieces)

    return absolute_puzzle_pieces

def getLeftPiece(puzzle_pieces):
    xs = [row[0] for row in puzzle_pieces]
    index_of_left_rectangle = xs.index(min(xs))

    left_piece = puzzle_pieces[index_of_left_rectangle]
    return left_piece

def getRightPiece(puzzle_pieces):
    xs = [row[0] for row in puzzle_pieces]
    index_of_right_rectangle = xs.index(max(xs))

    right_piece = puzzle_pieces[index_of_right_rectangle]
    return right_piece

def get_captcha_popup():
    return detect_image_location('samples/slider-robot.png')

def solve_captcha():
    captcha_popup = get_captcha_popup()

    if not captcha_popup.exist:
        # print("Don't show captcha")
        return

    pieces_start_position = get_pieces_position()

    if pieces_start_position is None:
        return 'pieces_start_position fail'

    slider_button_start_position = get_slider_button()

    if not slider_button_start_position.exist:
        return 'slider_button_start_position fail'

    x,y,_,_ = slider_button_start_position.position
    mouse_moveTo([x,y])
    mouse_down()
    mouse_moveTo([x+300,y])

    upgrade_current_screen()

    pieces_end_position = get_pieces_position()

    if pieces_end_position is None:
        return 'pieces_end_position fail'

    slider_button_end_position = get_slider_button()

    if not slider_button_end_position.exist:
        return 'slider_button_end_position fail'

    piece_start, _, _, _ = getLeftPiece(pieces_start_position)
    piece_end, _, _, _ = getRightPiece(pieces_end_position)
    piece_middle, _, _, _ = getRightPiece(pieces_start_position)
    slider_start, _, _, _ = slider_button_start_position.position
    slider_end, _, _, _ = slider_button_end_position.position

    piece_domain = piece_end - piece_start
    middle_piece_in_percent = (piece_middle - piece_start) / piece_domain

    slider_domain = slider_end - slider_start
    slider_awnser = slider_start + (middle_piece_in_percent * slider_domain)

    mouse_moveTo([slider_awnser, y])
    mouse_up()


upgrade_current_screen()
solve_captcha()