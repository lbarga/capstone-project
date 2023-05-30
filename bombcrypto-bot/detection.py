import cv2 as cv
import numpy as np



class Object(object):
    pass

def detect_image_location(object_path, threshold = 0.75, screen_path = 'samples/current-screen.jpg'):
    screen_img = cv.imread(screen_path, cv.IMREAD_UNCHANGED)
    screen_img_gray = cv.cvtColor(screen_img, cv.COLOR_BGR2GRAY)

    need_img = cv.imread(object_path, cv.IMREAD_UNCHANGED)
    need_img_gray = cv.cvtColor(need_img, cv.COLOR_BGR2GRAY)

    method = cv.TM_CCOEFF_NORMED

    result = cv.matchTemplate(screen_img_gray, need_img_gray, method)

    locations = np.where(result >= threshold)

    locations = list(zip(*locations[::-1]))

    rectangles = []

    needle_w = need_img_gray.shape[1]
    needle_h = need_img_gray.shape[0]

    if len(locations):
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

        object = Object()
        object.exist = True
        object.position = rectangles[0]

        return object
    else:
        object = Object()
        object.exist = False
        object.position = rectangles

        return object


def detect_all_image_location(object_path, threshold = 0.75, screen_path = 'samples/current-screen.jpg'):
    screen_img = cv.imread(screen_path, cv.IMREAD_UNCHANGED)
    screen_img_gray = cv.cvtColor(screen_img, cv.COLOR_BGR2GRAY)

    need_img = cv.imread(object_path, cv.IMREAD_UNCHANGED)
    need_img_gray = cv.cvtColor(need_img, cv.COLOR_BGR2GRAY)

    method = cv.TM_CCOEFF_NORMED

    result = cv.matchTemplate(screen_img_gray, need_img_gray, method)

    locations = np.where(result >= threshold)

    locations = list(zip(*locations[::-1]))

    rectangles = []

    needle_w = need_img_gray.shape[1]
    needle_h = need_img_gray.shape[0]

    if len(locations):
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

        # cv.imshow('screen', screen_copy)
        # cv.waitKey(0)

        object = Object()
        object.exist = True
        object.position = rectangles

        return object
    else:
        object = Object()
        object.exist = False
        object.position = rectangles

        return object
