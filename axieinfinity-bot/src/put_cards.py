import time
import cv2 as cv
import numpy as np
import os
from ppadb.client import Client as AdbClient

os.system('adb start-server')

HOST = "127.0.0.1"
PORT = 5037
client = AdbClient(host=HOST, port=PORT)

def detect_on_image(needle_img_path, haystack_img_path, threshold=0.5):
    # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
    haystack_img = cv.imread(haystack_img_path, cv.IMREAD_UNCHANGED)
    needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
    # Save the dimensions of the needle image
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    # There are 6 methods to choose from:
    # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(haystack_img, needle_img, method)

    # Get the all the positions from the match result that exceed our threshold
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    # print(locations)

    # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
    # locations by using groupRectangles().
    # First we need to create the list of [x, y, w, h] rectangles
    rectangles = []

    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        # Add every box to the list twice in order to retain single (non-overlapping) boxes
        rectangles.append(rect)
        rectangles.append(rect)
    # Apply group rectangles.
    # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
    # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
    # in the result. I've set eps to 0.5, which is:
    # "Relative difference between sides of the rectangles to merge them into a group."
    rectangles = cv.groupRectangles(
        rectangles, groupThreshold=1, eps=0.5)[0]
    # print(rectangles)

    return rectangles

def put_cards(rectangles, device):
    for index, rectangle in enumerate(rectangles):
        position_x = rectangle[0]
        position_y = rectangle[1]

        command = 'input touchscreen swipe ' + \
            str(position_x+50) + ' ' + str(position_y+50) + ' ' + \
            str(position_x+50) + ' ' + str(position_y+50-300)

        device.shell(command)

        if index == len(rectangles)-1:
            device.input_tap(1450, 510)

while True:
    try:
        class Modes:
            ADVENTURE = (1125, 625)
            ARENA = (1315, 515)
        # ========DEFINE MODE HERE========
        IMAGE_PATH = 'screenshot.png'
        button_position = Modes.ADVENTURE
        # ================================

        devices = client.devices()

        if len(devices) > 0:
            device = devices[0]

            if device:
                time.sleep(1)

                image = device.screencap()

                with open(IMAGE_PATH, 'wb') as f:
                    f.write(image)

                cards = detect_on_image(
                    'assets/card.png', IMAGE_PATH)

                cardsCount = len(cards)

                if cardsCount > 0:
                    print('detected cards ' + str(cardsCount))
                    put_cards(cards, device)
                    time.sleep(12)
                else:
                    print('no have cards')
                    (position_x, position_y) = button_position
                    device.input_tap(position_x, position_y)
        else:
            print('===no cell connected===')
    except:
        print('===error===')
