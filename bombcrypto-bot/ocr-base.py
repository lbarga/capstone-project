import cv2 as cv
import numpy as np

screen_path = 'samples/current-screen.jpg'
find_path = 'samples/slider-robot.png'

screen_img = cv.imread(screen_path, cv.IMREAD_UNCHANGED)
screen_img = cv.cvtColor(screen_img, cv.COLOR_BGR2GRAY)

need_img = cv.imread(find_path, cv.IMREAD_UNCHANGED)
need_img = cv.cvtColor(need_img, cv.COLOR_BGR2GRAY)

method = cv.TM_CCOEFF_NORMED

result = cv.matchTemplate(screen_img, need_img, method)

locations = np.where(result >= 0.75)

locations = list(zip(*locations[::-1]))

rectangles = []

needle_w = need_img.shape[1]
needle_h = need_img.shape[0]

for loc in locations:
    rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
    rectangles.append(rect)
    rectangles.append(rect)

rectangles = cv.groupRectangles(
        rectangles, groupThreshold=1, eps=0.5)[0]

# print(rectangles)

verify_button_position = rectangles[0]

position_x = verify_button_position[0]
position_y = verify_button_position[1]

# print(position_x, position_y + 20)

screen_copy = screen_img.copy()

for (x, y, w, h) in rectangles:
    cv.rectangle(screen_copy, (x, y), (x + w, y + h), (0, 255, 0), 10)

cv.imshow('screen', screen_copy)

cv.waitKey(0)