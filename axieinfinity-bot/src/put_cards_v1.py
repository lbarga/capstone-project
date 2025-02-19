import cv2 as cv
import numpy as np
import os
from PIL import Image
import pytesseract
from ppadb.client import Client as AdbClient
import os
import shutil
import time

host = "127.0.0.1"
port = 5037
image_path = 'screenshot.png'

client = AdbClient(host=host, port=port)

devices = client.devices()

device = devices[0]

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
# os.chdir(os.path.dirname(os.path.abspath(__file__)))


count = 1

def findClickPositions(needle_img_path, haystack_img_path, threshold=0.5, debug_mode=None):
    

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
    #print(locations)

    # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
    # locations by using groupRectangles().
    # First we need to create the list of [x, y, w, h] rectangles
    rectangles = []

    if len(locations) == 0:
        # ADVENTURE - START_BUTTON
        # device.input_tap(1125, 625)

        # HOME - ARENA_BUTTON
        device.input_tap(1315, 515)
    
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
    rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
    #print(rectangles)

    points = []
    if len(rectangles):
        #print('Found needle.')

        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        # Loop over all the rectangles
        for index,(x, y, w, h) in enumerate(rectangles):
            # Determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # Save the points
            points.append((center_x, center_y))

            # Put card
            command = 'input touchscreen swipe ' + str(x+50) + ' ' + str(y+50) + ' ' + str(x+50) + ' ' + str(y+50-300)
            device.shell(command)
            
            if index == len(rectangles)-1:
                device.input_tap(1450, 510)

            if debug_mode == 'rectangles':
                # Determine the box position
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                
                # Draw the box
                cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                             lineType=line_type, thickness=2)
            elif debug_mode == 'points':
                # Draw the center point
                cv.drawMarker(haystack_img, (center_x, center_y), 
                              color=marker_color, markerType=marker_type, 
                              markerSize=40, thickness=2)

        if debug_mode:
            # cv.imshow('Matches', haystack_img)
            # cv.waitKey()
            cv.imwrite('assets/result_click_point.jpg', haystack_img)

    return points


# points = findClickPositions('alert.jpeg', 'verify.jpeg', debug_mode='rectangles')
# print(points)


while True:
    image = device.screencap()

    with open(image_path, 'wb') as f:
        f.write(image)

    points = findClickPositions('assets/card.png', 'screenshot.png', debug_mode='rectangles')
    print(points)
    time.sleep(15)
